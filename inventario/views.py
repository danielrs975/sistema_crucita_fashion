'''
Script que contendra las vistas de este
modulo
'''
from django.shortcuts import render # pylint: disable=unused-import
from django.http import Http404
from rest_framework import generics
from inventario.models import Producto
from inventario.serializers import ProductoSerializer

# Create your views here.
class ProductoCrearView(generics.CreateAPIView):
    '''
    Vista que se encarga de la creacion de un
    nuevo producto para anadir al sistema
    '''
    serializer_class = ProductoSerializer

class ProductoDetallesView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Vista que permite modificar, ver o eliminar
    la informacion de un producto dentro del sistema
    '''
    serializer_class = ProductoSerializer

class ProductoBuscarView(generics.ListAPIView):
    '''
    Vista que permite buscar uno o varios productos
    en el sistema
    '''
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer