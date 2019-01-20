'''
Script que contendra los modelos de la base
de datos para las ventas
'''
from django.db import models # pylint: disable=unused-import
from inventario.models import Producto

# Create your models here.

class Ventas(models.Model):
    '''
    Tabla de Ventas, guarda los datos necesarios
    al momento de una venta
    '''
    producto = models.ManyToManyField(Producto)
    codigo = models.CharField(unique=True, max_length=500)
    costo_total = models.FloatField()
    fecha = models.DateField()
    hora = models.DateTimeField()
