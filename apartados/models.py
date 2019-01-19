'''
Script que contendra los modelos de la
aplicacion de los apartados
'''
from django.db import models # pylint: disable=unused-import
from inventario.models import Productos
from usuarios.models import Usuario

# Create your models here.

class Aparatado(models.Model):
	'''
	Creacion de la tabla de apartados, aqui se guardan 
	los productos que cada usuario aparte
	'''
	usuario = models.ForeignKey('Usuario', on_delete=PROTECT)
	codigo = models.CharField(max_length=100, unique=True)
	producto = models.ManyToManyField('Productos')
	costo_total = models.FloatField()