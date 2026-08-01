import io
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Produto, Categoria

MEDIA_TEMPORARIA = tempfile.mkdtemp()

ORIENTACAO_EXIF = 274


def criar_jpeg(largura, altura, orientacao=None):
    imagem = Image.new('RGB', (largura, altura), (200, 120, 60))
    opcoes = {}
    if orientacao is not None:
        exif = Image.Exif()
        exif[ORIENTACAO_EXIF] = orientacao
        opcoes['exif'] = exif

    buffer = io.BytesIO()
    imagem.save(buffer, format='JPEG', **opcoes)
    return SimpleUploadedFile('foto.jpg', buffer.getvalue(), 'image/jpeg')

class ProdutoCategoriaTest(TestCase):
    def setUp(self):
        self.categoria_cabo = Categoria.objects.create(nome="cabo")

    def test_cria_produto_com_categoria(self):
        produto = Produto.objects.create(nome="cabo de vassoura", categoria=self.categoria_cabo, preco=500)
        self.assertEqual(produto.nome, "cabo de vassoura")
        self.assertEqual(produto.categoria.nome, "cabo")


@override_settings(
    MEDIA_ROOT=MEDIA_TEMPORARIA,
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class ConversaoImagemTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TEMPORARIA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.categoria = Categoria.objects.create(nome="vassouras")

    def test_corrige_rotacao_exif(self):
        produto = Produto.objects.create(
            nome="vassoura piacava",
            categoria=self.categoria,
            preco=30,
            imagem=criar_jpeg(100, 200, orientacao=6),
        )

        with produto.imagem.open('rb') as arquivo:
            imagem = Image.open(arquivo)
            self.assertEqual(imagem.format, 'WEBP')
            self.assertEqual(imagem.size, (200, 100))

    def test_novo_save_nao_reconverte_imagem(self):
        produto = Produto.objects.create(
            nome="rodo aluminio",
            categoria=self.categoria,
            preco=40,
            imagem=criar_jpeg(800, 600),
        )
        nome_original = produto.imagem.name
        with produto.imagem.open('rb') as arquivo:
            bytes_originais = arquivo.read()

        produto.preco = 45
        produto.save()

        salvo = Produto.objects.get(pk=produto.pk)
        self.assertEqual(salvo.imagem.name, nome_original)
        with salvo.imagem.open('rb') as arquivo:
            self.assertEqual(arquivo.read(), bytes_originais)

    def test_produto_sem_imagem_salva_normalmente(self):
        produto = Produto.objects.create(
            nome="cabo de madeira",
            categoria=self.categoria,
            preco=15,
        )

        self.assertFalse(produto.imagem)

    def test_remover_imagem_no_admin_salva_normalmente(self):
        produto = Produto.objects.create(
            nome="pa de lixo",
            categoria=self.categoria,
            preco=20,
            imagem=criar_jpeg(800, 600),
        )

        produto.imagem = ''
        produto.save()

        self.assertFalse(Produto.objects.get(pk=produto.pk).imagem)


class ProdutoQueryParamsTest(TestCase):
    def setUp(self):
        self.vassouras = Categoria.objects.create(nome='vassouras')
        self.cabos = Categoria.objects.create(nome='cabos')

        Produto.objects.create(nome='vassoura piaçava', categoria=self.vassouras, preco=30)
        Produto.objects.create(nome='vassoura de pelo', categoria=self.vassouras, preco=25)
        Produto.objects.create(nome='cabo de madeira', categoria=self.cabos, preco=15)

        self.url = reverse('produto-list')

    def nomes(self, resposta):
        return {item['nome'] for item in resposta.json()}

    def test_ignora_categoria_nao_numerica(self):
        resposta = self.client.get(self.url, {'categoria': 'abc'})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json()), 3)

    def test_ignora_categoria_vazia(self):
        resposta = self.client.get(self.url, {'categoria': ''})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json()), 3)

    def test_filtra_por_categoria_valida(self):
        resposta = self.client.get(self.url, {'categoria': self.cabos.id})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(self.nomes(resposta), {'cabo de madeira'})

    def test_categoria_inexistente_devolve_lista_vazia(self):
        resposta = self.client.get(self.url, {'categoria': 9999})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json(), [])

    def test_ignora_busca_vazia(self):
        resposta = self.client.get(self.url, {'search': ''})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json()), 3)

    def test_ignora_busca_so_com_espacos(self):
        resposta = self.client.get(self.url, {'search': '   '})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json()), 3)

    def test_busca_sem_acento_encontra_nome_com_acento(self):
        resposta = self.client.get(self.url, {'search': 'piacava'})

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(self.nomes(resposta), {'vassoura piaçava'})

    def test_nao_lista_produto_inativo(self):
        Produto.objects.create(nome='rodo aposentado', categoria=self.cabos, preco=10, ativo=False)

        resposta = self.client.get(self.url)

        self.assertNotIn('rodo aposentado', self.nomes(resposta))


class OrdenacaoTest(TestCase):
    def test_produtos_vem_ordenados_por_nome(self):
        categoria = Categoria.objects.create(nome='geral')
        for nome in ['rodo', 'balde', 'vassoura']:
            Produto.objects.create(nome=nome, categoria=categoria, preco=10)

        resposta = self.client.get(reverse('produto-list'))

        self.assertEqual(
            [item['nome'] for item in resposta.json()],
            ['balde', 'rodo', 'vassoura'],
        )

    def test_categorias_vem_ordenadas_por_nome(self):
        for nome in ['vassouras', 'baldes', 'cabos']:
            Categoria.objects.create(nome=nome)

        resposta = self.client.get(reverse('categoria-list'))

        self.assertEqual(
            [item['nome'] for item in resposta.json()],
            ['baldes', 'cabos', 'vassouras'],
        )


SENHA_VALIDA = 'senha-de-teste-longa-123'


@override_settings(
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class BloqueioLoginAdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            username='dono',
            email='dono@exemplo.com',
            password=SENHA_VALIDA,
        )
        self.url = reverse('admin:login')

    def test_login_valido_continua_funcionando(self):
        cliente = Client()

        resposta = cliente.post(self.url, {'username': 'dono', 'password': SENHA_VALIDA})

        self.assertEqual(resposta.status_code, 302)

    def test_bloqueia_apos_limite_de_tentativas(self):
        cliente = Client()
        for _ in range(settings.AXES_FAILURE_LIMIT):
            cliente.post(self.url, {'username': 'dono', 'password': 'errada'})

        resposta = cliente.post(self.url, {'username': 'dono', 'password': SENHA_VALIDA})

        self.assertEqual(resposta.status_code, 429)
