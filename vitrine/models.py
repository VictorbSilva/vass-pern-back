from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome