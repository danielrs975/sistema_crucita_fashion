from rest_framework import serializers
from .models import Ventas

class VentasSerializer(serializers.ModelSerializer):
	'''
	Clase que representa el serializer de las Ventas
	'''
	def validate_costo_total(self, costo):
		'''
		Metodo para validar el costo total de la venta.
		Se ejecuta automaticamente
		'''

		if isinstance(costo, str):
            raise serializers.ValidationError("El costo introducido es un string")

        if costo <= 0:
            raise serializers.ValidationError("El costo no puede ser negativo")

        return costo

	class Meta:
		model = Ventas
		fields = "__al__"