'''
Script que contiene las pruebas relacionadas
con las vistas del modulo inventario
'''
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from inventario.views import ProductoCrearView
from inventario.models import Producto, Categoria

class ProductoCrearViewTests(TestCase):
    '''
    Clase que contiene las pruebas
    relacionada con la vista que se encarga
    de crear un producto
    '''
    def setUp(self):
        '''
        Inicializa las variables necesarias para 
        realizar las pruebas
        '''
        for categoria in ["Ropa", "Zapato", "Accesorio"]:
            Categoria.objects.create(nombre=categoria)

        self.factory = APIRequestFactory()

    def test_crear_producto(self):
        '''
        Prueba que se crea un producto nuevo
        con exito
        '''
        data = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': (Categoria.objects.get(nombre="Ropa")).pk,
            'talla': 6,
        }
        request = self.factory.post('/inventario/crear/', data, format='json')
        response = ProductoCrearView.as_view()(request)
        self.assertEqual(response.status_code, 200)
