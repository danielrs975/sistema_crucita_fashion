'''
Script que contendra las vistas que manejara
la informacion que proveera este modulo
'''
from django.shortcuts import render # pylint: disable=unused-import
from rest_framework import generics
from .models import Ventas
from .serializers import VentasSerializer

# Create your views here.

class VentasCrearView(generics.CreateAPIView):
	'''
	Vista que se encarga de la creacion de una venta
	para ser anadida al sistema
	'''
	queryset = Ventas.objects.all()
	serializer_class = VentasSerializer

class VentasDetallesView(generics.RetrieveUpdateDestroyAPIView):
	'''
	Vista que se encarga de ver, modificar o eliminar una venta
	'''
	queryset = Ventas.objects.all()
	serializer_class = VentasSerializer

class VentasBuscarView(generics.ListAPIView):
	''' 
	Vista que se encarga de buscar y mostrar una Venta o una lista
	de ventas
	'''
	queryset = Ventas.objects.all()
	serializer_class = VentasSerializer
