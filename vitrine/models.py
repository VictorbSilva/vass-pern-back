from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.PROTECT, related_name='produtos')
    descricao = models.TextField(null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos', null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

