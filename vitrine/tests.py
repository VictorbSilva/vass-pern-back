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
