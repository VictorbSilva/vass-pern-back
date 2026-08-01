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

        categoria_id = self.request.query_params.get('categoria', '').strip()

        # isdecimal, nao isdigit: "²".isdigit() e True, mas int("²") estoura.
        if categoria_id.isdecimal():
            queryset = queryset.filter(categoria_id=int(categoria_id))

        busca = self.request.query_params.get('search', '').strip()

        if busca:
            queryset = queryset.filter(nome__unaccent__icontains=busca)

        return queryset