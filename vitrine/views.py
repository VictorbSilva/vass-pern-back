from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Produto
from .serializers import ProdutoSerializer
# Create your views here.

@csrf_exempt
def produto_list(request):
    if request.method == 'GET':
        produtos = Produto.objects.all()
        serializer = ProdutoSerializer(produtos, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProdutoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def produto_detail(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)
    except Produto.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProdutoSerializer(produto)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProdutoSerializer(produto, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        produto.delete()
        return HttpResponse(status=204)
    return HttpResponse(status=400)