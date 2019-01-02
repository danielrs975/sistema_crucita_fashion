'''
Script donde estan los serializers para este
modulo
'''
from rest_framework import serializers
from .models import Producto, Categoria, TALLA_ROPA, TALLA_ZAPATOS

class ProductoSerializer(serializers.ModelSerializer):
    '''
    Clase que representa el serializer de los productos
    dentro del inventario
    '''
    def is_valid(self):
        '''
        Se sobreescribe el metodo is_valid para poder
        escribir la validacion de la talla en caso de que
        sea de zapatos o de ropa
        '''
        producto_valido = super().is_valid()
        categoria = Categoria.objects.get(pk=self.data['categoria'])
        talla = None

        if 'talla' in self.data.keys():
            talla = self.data['talla']

        if categoria.nombre == "Ropa":
            if not talla in TALLA_ROPA:
                return False
        elif categoria.nombre == "Zapato":
            if not talla in TALLA_ZAPATOS:
                return False
        else:
            if talla != None:
                return False

        return producto_valido

    class Meta:
        model = Producto
        fields = ('codigo', 'cantidad', 'costo', 'categoria', 'talla')