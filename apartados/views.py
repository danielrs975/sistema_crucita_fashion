'''
Script que contendra las vistas de este modulo
'''
from django.shortcuts import render # pylint: disable=unused-import
from rest_framwork import generics
from .models import Apartado
from .serializers import AparatadoSerializer
# Create your views here.

class ApartadoCrearView(generics.CreateAPIView):
	'''
	Clase de vista para crear un apartado
	'''
	query_set = Apartado.objects.all()
	serializer_class = AparatadoSerializer

class AparatadoBorrarView(generics.RetrieveDestroyAPIView):
	'''
	Clase de vista para ver y eliminar un apartado
	'''
	query_set = Apartado.objects.all()
	serializer_class = AparatadoSerializer

class ApartadoModificarView(generics.RetrieveUpdateAPIView):
	'''
	Clase de vista para ver y modificar un apartado
	'''
	query_set = Apartado.objects.all()
	serializer_class = AparatadoSerializer

class ApartadoBuscarView(generics.ListAPIView):
	'''
	Clase de vista para Buscar coleccion de 
	objetos de un apartado
	'''
	query_set = Apartado.objects.all()
	serializer_class = AparatadoSerializer
