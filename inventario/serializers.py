'''
Script donde estan los serializers para este
modulo
'''
from rest_framework import serializers
from .models import Producto, Categoria, TALLA_ROPA, TALLA_ZAPATOS

class CategoriaSerializer(serializers.ModelSerializer):
    '''
    Clase que representa el serializer de las categorias
    en la cuales esta contenida cada unos de los productos
    '''
    class Meta:
        model = Categoria
        fields = "__all__"

class ProductoSerializer(serializers.ModelSerializer):
    '''
    Clase que representa el serializer de los productos
    dentro del inventario
    '''
    def is_valid(self): # pylint: disable=arguments-differ
        '''
        Se sobreescribe el metodo is_valid para poder
        escribir la validacion de la talla en caso de que
        sea de zapatos o de ropa
        '''
        producto_valido = super().is_valid()
        categoria = Categoria.objects.get(pk=self.data['categoria'])
        talla = None

        # Area de verificacion de la talla
        if 'talla' in self.data.keys():
            talla = self.data['talla']

        if categoria.nombre == "Ropa":
            if not talla in TALLA_ROPA:
                return False
        elif categoria.nombre == "Zapato":
            if not talla in TALLA_ZAPATOS:
                return False
        else:
            if talla is not None:
                return False

        return producto_valido

    def validate_costo(self, costo): # pylint: disable=no-self-use
        '''
        Metodo que valida el costo de un
        Producto. Se ejecuta automaticamente con is_valid
        '''
        # Area de verificacion del costo
        if isinstance(costo, str):
            raise serializers.ValidationError("El costo introducido es un string")

        if costo <= 0:
            raise serializers.ValidationError("El costo no puede ser negativo")

    class Meta:
        model = Producto
        fields = ('codigo', 'cantidad', 'costo', 'categoria', 'talla')
