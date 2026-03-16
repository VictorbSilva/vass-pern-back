from django.contrib import admin
from .models import Produto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'preco', 'ativo', 'updated_at')
    list_filter = ('ativo', 'categoria')
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'ativo')
    list_per_page = 20