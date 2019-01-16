'''
Script que contendra las vistas de este
modulo
'''
from django.shortcuts import render # pylint: disable=unused-import
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from inventario.models import Producto
from inventario.serializers import ProductoSerializer
from inventario.permissions import IsStaff

# Create your views here.
class ProductoCrearView(generics.CreateAPIView):
    '''
    Vista que se encarga de la creacion de un
    nuevo producto para anadir al sistema
    '''
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsStaff,
    ) 

class ProductoDetallesView(generics.RetrieveUpdateDestroyAPIView): # pylint: disable=too-many-ancestors
    '''
    Vista que permite modificar, ver o eliminar
    la informacion de un producto dentro del sistema
    '''
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsStaff,
    )

class ProductoBuscarView(generics.ListAPIView):
    '''
    Vista que permite buscar uno o varios productos
    en el sistema
    '''
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('codigo', 'cantidad', 'costo', 'categoria')
