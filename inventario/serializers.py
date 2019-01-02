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

    def validate(self, data):
        '''
        Metodo que valida la talla de un Producto
        dependiendo si es una Ropa o un Zapato
        '''
        categoria = data['categoria']
        talla = None

        if 'talla' in data.keys():
            talla = data['talla']

        # Area de verificacion de la talla
        if categoria.nombre == "Ropa":
            if not talla in TALLA_ROPA:
                raise serializers.ValidationError("La talla introducida no es valida para la ropa")
        elif categoria.nombre == "Zapato":
            if not talla in TALLA_ZAPATOS:
                raise serializers.ValidationError("La talla introducida no es valida para zapatos")
        else:
            if talla is not None:
                raise serializers.ValidationError("No aplica el campo talla para este producto")
        
        return data

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
        
        return costo

    class Meta:
        model = Producto
        fields = ('codigo', 'cantidad', 'costo', 'categoria', 'talla')
