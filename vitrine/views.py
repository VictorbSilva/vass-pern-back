from rest_framework import viewsets
from .models import Produto, Categoria
from .serializers import ProdutoSerializer, CategoriaSerializer


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        queryset = Produto.objects.select_related('categoria').filter(ativo=True)

        categoria_id = self.request.query_params.get('categoria', None)

        if categoria_id is not None:
            queryset = queryset.filter(categoria_id=categoria_id)

        busca = self.request.query_params.get('search', None)

        if busca is not None:
            queryset = queryset.filter(nome__unaccent__icontains=busca)

        return queryset