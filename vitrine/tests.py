from django.test import TestCase
from .models import Produto, Categoria

class ProdutoCategoriaTest(TestCase):
    def setUp(self):
        self.categoria_cabo = Categoria.objects.create(nome="cabo")

    def test_cria_produto_com_categoria(self):
        produto = Produto.objects.create(nome="cabo de vassoura", categoria=self.categoria_cabo, preco=500)
        self.assertEqual(produto.nome, "cabo de vassoura")
        self.assertEqual(produto.categoria.nome, "cabo")



# Create your tests here.
