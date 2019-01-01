'''
Script que contendra los modelos para esta
aplicacion
'''
from django.db import models # pylint: disable=unused-import

# Create your models here.

class Categoria(models.Model):
    '''
    Creacion de la tabla categoria que 
    dividira los productos en distintos tipos
    '''
    nombre = models.CharField(unique=True, max_length=100)

class Producto(models.Model):
    '''
    Creacion de la tabla Producto, esta contendra
    todos los productos que esten disponibles
    '''
    codigo = models.CharField(unique=True, max_length=500)
    cantidad = models.PositiveIntegerField()
    costo = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    talla = models.CharField(null=True, max_length=100)
    foto = models.ImageField(null=True)
