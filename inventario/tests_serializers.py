'''
Script que contendra las pruebas
para este modulo
'''
from django.test import TestCase # pylint: disable=unused-import
from .serializers import ProductoSerializer
from .models import Producto, Categoria

# Create your tests here.
class ProductoSerializerTest(TestCase):
    '''
    Clase que sirve para probar el serializer
    hecho para Producto
    '''
    def setUp(self):
        '''
        Metodo para inicializar la informacion necesaria
        para las pruebas
        '''
        for categoria in ["Ropa", "Zapato", "Accesorio"]:
            Categoria.objects.create(nombre=categoria)

        self.producto_1 = Producto(
            codigo="1",
            cantidad=1,
            costo=1,
            categoria=Categoria.objects.get(nombre="Ropa"),
            talla="M"
        )
        self.categoria_ropa = (Categoria.objects.get(nombre="Ropa")).pk
        self.categoria_zapato = (Categoria.objects.get(nombre="Zapato")).pk
        self.categoria_accesorio = (Categoria.objects.get(nombre="Accesorio")).pk

    def test_producto_serializer(self):
        '''
        Prueba que el serializer este contruyendo la informacion
        bien
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "M",
            'foto': None
        }
        producto_serializer = ProductoSerializer(self.producto_1)
        self.assertEqual(producto_serializer.data, producto, msg="Los dos productos no son iguales")

    def test_is_valid_codigo_es_char(self):
        '''
        Prueba de que el atributo codigo tiene que ser
        un string
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "M"
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertTrue(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_cantidad_negativo(self):
        '''
        Prueba con el atributo cantidad negativo.
        Deberia dar False
        '''
        producto = {
            'codigo': "1",
            'cantidad': -1,
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "M"
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_cantidad_otro_tipo_dato(self):
        '''
        Prueba con el atributo cantidad con otro tipo de
        dato. Deberia de dar False
        '''
        producto = {
            'codigo': "1",
            'cantidad': "ansjanoasnoif",
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "M"
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_cantidad_positiva(self):
        '''
        Prueba con el atributo cantidad con un entero
        positivo. Deberia dar True
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "M"
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertTrue(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_costo_otro_tipo_dato(self):
        '''
        Prueba con el atributo costo con otro tipo
        de dato que no es numerico. Deberia dar False
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': "asnoisanfoina",
            'categoria': self.categoria_ropa,
            'talla': "M"
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_costo_numero_negativo(self):
        '''
        Prueba con el atributo costo con un numero negativo
        . Deberia dar False
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': -1,
            'categoria': self.categoria_ropa,
            'talla': "M"
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_costo_numero_positivo(self):
        '''
        Prueba con el atributo costo con un numero positivo,
        Deberia dar True
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "M"
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertTrue(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_talla_ropa_none(self):
        '''
        Metodo que prueba el is_valid del serializer
        del producto
        '''
        producto_ropa = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa
        }
        producto_serializer = ProductoSerializer(data=producto_ropa)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_ropa_talla_invalida(self):
        '''
        Metodo que prueba el is_valid del serializer
        cuando la talle es negativa
        '''
        producto_ropa = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "nsaoinfiasonf"
        }
        producto_serializer = ProductoSerializer(data=producto_ropa)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_ropa_talla_valida(self):
        '''
        Metodo que corre el test con una talla
        valida
        '''
        producto_ropa = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa,
            'talla': "XS"
        }
        producto_serializer = ProductoSerializer(data=producto_ropa)
        self.assertTrue(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_zapato_talla_none(self):
        '''
        Metodo que corre la prueba con zapatos
        pero la talla es none
        '''
        producto_zapato = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_ropa
        }
        producto_serializer = ProductoSerializer(data=producto_zapato)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_zapato_talla_negativa(self):
        '''
        Prueba que la talla no pueda ser negativa
        '''
        producto_zapato = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_zapato,
            'talla': -1,
        }
        producto_serializer = ProductoSerializer(data=producto_zapato)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_zapato_talla_valida(self):
        '''
        Prueba que cuando la talla es valida
        devuelva true
        '''
        producto_zapato = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_zapato,
            'talla': 6,
        }
        producto_serializer = ProductoSerializer(data=producto_zapato)
        self.assertTrue(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_producto_con_talla(self):
        '''
        Prueba que is_valid devuelve false
        cuando el producto no es ni zapato ni ropa
        y tiene talla
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_accesorio,
            'talla': "3",
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertFalse(producto_serializer.is_valid(), msg=producto_serializer.errors)

    def test_is_valid_producto_sin_talla(self):
        '''
        Prueba que is_valid devuelve true si
        se le pasa un producto que no es ni zapato ni ropa
        y no tiene talla
        '''
        producto = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': self.categoria_accesorio
        }
        producto_serializer = ProductoSerializer(data=producto)
        self.assertTrue(producto_serializer.is_valid(), msg=producto_serializer.errors)
    