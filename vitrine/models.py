from django.db import models

# Create your models here.

class Categoria(models.Model):
    nomeCategoria = models.CharField(max_length=200)
    descricaoCategoria = models.TextField()

    def __str__(self):
        return self.nomeCategoria

class Produto(models.Model):
    nomeProduto = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.CASCADE)
    descricaoProduto = models.TextField(null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagemProduto = models.ImageField(upload_to='produtos', null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nomeProduto

