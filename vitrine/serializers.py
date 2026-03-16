from rest_framework import serializers
from vitrine.models import Produto, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']

class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = CategoriaSerializer(source='categoria', many=False, read_only=True)
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'categoria', 'categoria_nome', 'preco', 'imagem', 'ativo']



