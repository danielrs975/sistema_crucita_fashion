'''
Script de los serializers del modulo
de apartados
'''
from rest_framwork import serializers
from .models import Apartado

class ApartadoSerializer(serializers.ModelSerializer):
	'''
	Clase que representa y maneja los serialzers 
	del modulo de apartados
	'''
	class Meta:
		model = Apartado
		fields = "__all__"
