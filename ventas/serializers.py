'''
Script de los serializers del modulo de ventas
'''
from rest_framework import serializers
from .models import Ventas

class VentasSerializer(serializers.ModelSerializer):
    '''
    Clase que representa el serializer de las Ventas
    '''
    class Meta:
        model = Ventas
        fields = ('producto', 'codigo', 'costo_total', 'fecha', 'hora')
