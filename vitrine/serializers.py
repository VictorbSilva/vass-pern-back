from rest_framework import serializers
from vitrine.models import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

def create_produto(validated_data):
    produto = Produto.objects.create(**validated_data)
    return produto


def update_produto(self, instance, validated_data):
        instance.preco = validated_data.get('preco', instance.preco)
        instance.save()
        return instance