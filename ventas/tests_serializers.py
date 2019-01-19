'''
Script para pruebas del serializer
del modulo de ventas
'''
from datetime import date
from django.test import TestCase # pylint: disable=unused-import
from django.utils import timezone
from inventario.models import Producto, Categoria # pylint: disable=unused-import
from .serializers import VentasSerializer
from .models import Ventas
from pprint import pprint

class VentaSerializerTest(TestCase):
    '''
    Clase para las pruebas de serializer de ventas
    '''
    fixtures = ['fixtures']

    def setUp(self):
        '''
        Metodo para iniciar los objetos prueba
        de la clase de pruebas
        '''
        self.fecha = date.today()
        self.hora = timezone.now()
        producto = Producto.objects.get(pk=1)
        self.venta = Ventas.objects.create(
            codigo='1a',
            costo_total=1,
            fecha=self.fecha,
            hora=self.hora,
        )
        self.venta.producto.add(producto)
        self.venta_json = {
            'codigo' : '1a',
            'costo_total': 1,
            'fecha': self.fecha,
            'hora' : self.hora,
        }

    def test_venta_serilizer(self):
        '''
        Prueba que devuelve true si la data suministrada la
        procesa bien
        '''
        venta_serializer = VentasSerializer(self.venta)
        self.assertEqual(venta_serializer.data, self.venta_json, msg="Ventas Distintas")

    def test_codigo_formato_incorrecto(self):
        '''
        Prueba que is_valid() devuelve false si se le pasa
        al codigo un tipo distinto a string
        '''
        venta1 = {
            'producto' : Producto.objects.get(pk=1),
            'codigo' : 1,
            'costo_total': 1,
            'fecha': date.today(),
            'hora' : timezone.now(),
        }
        venta_serializer = VentasSerializer(data=venta1)
        self.assertFalse(venta_serializer.is_valid(), msg=venta_serializer.errors)

    def test_fecha_formato_correcto(self):
        '''
        Prueba que is_valid() devuelve true si el formato
        de fecha es correcto
        '''
        venta_serializer = VentasSerializer(self.venta)
        self.assertTrue(venta_serializer.is_valid(), msg=venta_serializer.errors)

    def test_fecha_formato_incorrecto(self):
        '''
        Prueba que is_valid() devuelve false si el formato
        de fecha es incorrecto
        '''
        venta1 = {
            'producto' : Producto.objects.get(pk=1),
            'codigo' : '1a',
            'costo_total': 1,
            'fecha': '1 1 2018',
            'hora' : timezone.now(),
        }
        venta_serializer = VentasSerializer(data=venta1)
        self.assertFalse(venta_serializer.is_valid(), msg=venta_serializer.errors)

    def test_hora_formato_correcto(self):
        '''
        Prueba que is_valid() devuelve true si el formato
        de hora es correcto
        '''
        venta_serializer = VentasSerializer(data=self.venta)
        self.assertTrue(venta_serializer.is_valid(), msg=venta_serializer.errors)

    def test_hora_formato_incorrecto(self):
        '''
        Prueba que is_valid() devuelve false si el formato
        de hora es incorrecto
        '''
        venta1 = {
            'producto' : Producto.objects.get(pk=1),
            'codigo' : '1a',
            'costo_total': 1,
            'fecha': date.today(),
            'hora' : '1 1 2018 10 10 10',
        }
        venta_serializer = VentasSerializer(data=venta1)
        self.assertFalse(venta_serializer.is_valid(), msg=venta_serializer.errors)

    def test_costo_total_numero(self):
        '''
        Prueba con el atributo costo_total con otro tipo
        de dato diferente a un flotante que devuelve false
        '''
        venta1 = {
            'producto' : Producto.objects.get(pk=1),
            'codigo' : '1a',
            'costo_total': '1',
            'fecha': date.today(),
            'hora' : timezone.now(),
        }
        venta_serializer = VentasSerializer(data=venta1)
        self.assertFalse(venta_serializer.is_valid(), msg=venta_serializer.errors)
