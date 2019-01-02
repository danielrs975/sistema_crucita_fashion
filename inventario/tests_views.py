'''
Script que contiene las pruebas relacionadas
con las vistas del modulo inventario
'''
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from inventario.views import ProductoCrearView
from inventario.models import Producto, Categoria
from inventario.serializers import ProductoSerializer

class ProductoCrearViewTests(APITestCase):
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

    def test_crear_producto(self):
        '''
        Prueba que se crea un producto nuevo
        con exito
        '''
        url = reverse_lazy('inventario:crear')
        data = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': (Categoria.objects.get(nombre="Ropa")).pk,
            'talla': "M",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Producto.objects.get().codigo, "1")

    def test_crear_producto_error(self):
        '''
        Prueba que no se crea un producto
        si los datos presentan un error
        '''
        url = reverse_lazy('inventario:crear')
        data = {
            'codigo': "1",
            'cantidad': 1,
            'costo': -1,
            'categoria': (Categoria.objects.get(nombre="Ropa")).pk,
            'talla': "M",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

class ProductoDetallesViewTest(APITestCase):
    '''
    Clase que prueba la vista que muestra
    los detalles de un producto
    '''
    def setUp(self):
        '''
        Inicializa la base de datos con algunos 
        productos para realizar las pruebas
        '''
        for categoria in ["Ropa", "Zapato", "Accesorio"]:
            Categoria.objects.create(nombre=categoria)
        
        Producto.objects.create(
            codigo="2",
            cantidad=1,
            costo=1,
            categoria=Categoria.objects.get(nombre="Ropa"),
            talla="M"
        )
        Producto.objects.create(
            codigo="3",
            cantidad=2,
            costo=3,
            categoria=Categoria.objects.get(nombre="Accesorio")
        )
    
    def test_mostrar_detalles_de_un_producto(self):
        '''
        Prueba que muestra los detalles de un producto
        con exito
        '''
        url = reverse_lazy('inventario:editar', args=((Producto.objects.get(codigo="2")).pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_mostrar_detalles_de_un_producto_que_no_existe(self):
        '''
        Prueba que si un producto no existe 
        arroja un error 404 Not Found
        '''
        url = reverse_lazy('inventario:editar', args=(5,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.data)
    
    def test_actualizar_detalles_de_un_producto(self):
        '''
        Prueba que actualiza bien los detalles de un producto
        '''
        producto_editar = Producto.objects.get(codigo="2")
        url = reverse_lazy('inventario:editar', args=(producto_editar.pk,))
        data = {
            'codigo': producto_editar.codigo,
            'cantidad': 1,
            'costo': 3,
            'categoria': (Categoria.objects.get(nombre="Ropa")).pk,
            'talla': "M",
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        producto_editado = Producto.objects.get(codigo="2")
        self.assertEqual(producto_editado.costo, data['costo'], msg="No se actualizo correctamente le producto")

    def test_eliminar_producto_que_existe(self):
        '''
        Prueba que elimina un producto con
        exito
        '''
        producto_eliminar = Producto.objects.get(codigo="2")
        url = reverse_lazy('inventario:editar', args=(producto_eliminar.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg="No se elimino correctamente el producto")

    def test_eliminar_producto_que_no_existe(self):
        '''
        Prueba que muestra un error si el 
        producto a eliminar no existe
        '''
        url = reverse_lazy('inventario:editar', args=(8,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.data)

class ProductoBuscarViewTest(APITestCase):
    '''
    Clase que contiene las pruebas relacionadas
    a la vista encargada de la busqueda
    '''
    def setUp(self):
        '''
        Pobla la base de datos con informacion
        para hacer las pruebas
        '''
        for categoria in ["Ropa", "Zapato", "Accesorio"]:
            Categoria.objects.create(nombre=categoria)
        
        Producto.objects.create(
            codigo="2",
            cantidad=1,
            costo=1,
            categoria=Categoria.objects.get(nombre="Ropa"),
            talla="M"
        )
        Producto.objects.create(
            codigo="3",
            cantidad=2,
            costo=3,
            categoria=Categoria.objects.get(nombre="Accesorio")
        )
        self.mensaje_query = "La query hecha por .filter y por el request no son iguales"
    
    def test_busqueda_con_codigo_valido(self):
        '''
        Prueba que contiene un busqueda por codigo 
        en la base de datos
        '''
        url = reverse_lazy("inventario:buscar")
        url = url + "?codigo=2"
        response = self.client.get(url)
        resultado_esperado = [
            ProductoSerializer(producto).data for producto in Producto.objects.filter(codigo="2")
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, resultado_esperado, msg=self.mensaje_query)

    def test_busqueda_con_categoria_valida(self):
        '''
        Prueba que la busqueda con una categoria 
        valida retorna una lista de los productos
        en esa categoria
        '''
        categoria = Categoria.objects.get(nombre="Ropa")
        url = reverse_lazy("inventario:buscar")
        url = url + "?categoria=" + str(categoria.pk)
        response = self.client.get(url)
        resultado_esperado = [
            ProductoSerializer(producto).data for producto in Producto.objects.filter(categoria=categoria)
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, resultado_esperado, msg=self.mensaje_query)

    def test_busqueda_con_varios_campos(self):
        '''
        Prueba la busqueda con varios campos
        '''
        categoria = Categoria.objects.get(nombre="Ropa")
        url = reverse_lazy("inventario:buscar")
        url = url + "?categoria=" + str(categoria.pk) + "&talla=M"
        response = self.client.get(url)
        resultado_esperado = [
            ProductoSerializer(producto).data for producto in Producto.objects.filter(categoria=categoria, talla="M")
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, resultado_esperado, msg=self.mensaje_query)

    def test_busqueda_con_campo_invalido(self):
        '''
        Prueba realizar una busqueda con uno 
        de los atributos invalido
        '''
        url = reverse_lazy("inventario:buscar")
        url = url + "?costo=-1"
        response = self.client.get(url)
        resultado_esperado = []
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, resultado_esperado, msg=self.mensaje_query)
