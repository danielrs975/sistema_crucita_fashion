'''
Script que contiene las pruebas relacionadas
con las vistas del modulo inventario
'''
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from inventario.models import Producto, Categoria
from inventario.serializers import ProductoSerializer

class ProductoCrearViewTests(APITestCase):
    '''
    Clase que contiene las pruebas
    relacionada con la vista que se encarga
    de crear un producto
    '''
    fixtures = ['groups.json', 'usuarios.json']

    def setUp(self):
        '''
        Inicializa las variables necesarias para
        realizar las pruebas
        '''
        for categoria in ["Ropa", "Zapato", "Accesorio"]:
            Categoria.objects.create(nombre=categoria)

        self.data = {
            'codigo': "1",
            'cantidad': 1,
            'costo': 1,
            'categoria': (Categoria.objects.get(nombre="Ropa")).pk,
            'talla': "M",
        }

    def test_crear_producto(self):
        '''
        Prueba que se crea un producto nuevo
        con exito
        '''
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy('inventario:crear')
        self.client.post(login, data={"username": "danielrs", "password": "danielrs19972705"})
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
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy('inventario:crear')
        self.client.post(login, data={"username": "danielrs", "password": "danielrs19972705"})
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

    def test_verifica_que_el_usuario_esta_autenticado(self):
        """
        Prueba que si el usuario esta autenticado lo
        dejara ver la vista
        """
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy('inventario:crear')
        self.client.post(login, data={"username": "crucita", "password": "crucita64"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         msg=response.data)

    def test_usuario_no_autenticado_entra_a_la_vista(self):
        """
        Prueba que un usuario no autenticado no
        puede entrar a la vista
        """
        url = reverse_lazy('inventario:crear')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_administrador_entra_a_la_vista(self):
        """
        Prueba que si un administrador trata de entrar
        a la vista se le permite
        """
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy('inventario:crear')
        self.client.post(login, data={"username": "crucita", "password": "crucita64"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         msg=response.data)

    def test_vendedor_entra_a_la_vista(self):
        """
        Prueba que si un vendedor trata de entrar a la
        vista se le permite
        """
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy('inventario:crear')
        self.client.post(login, data={"username": "dwest06", "password": "jaja123"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         msg=response.data)

    def test_cliente_entra_a_la_vista(self):
        """
        Prueba que si un cliente trata de entrar a la vista
        se le niega la entrada
        """
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy('inventario:crear')
        self.client.post(login, data={"username": "rafaelrs", "password": "jaja123"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)


class ProductoDetallesViewTest(APITestCase):
    '''
    Clase que prueba la vista que muestra
    los detalles de un producto
    '''
    fixtures = ['groups.json', 'usuarios.json']
    def setUp(self):
        '''
        Inicializa la base de datos con algunos
        productos para realizar las pruebas
        '''
        for categoria in ["Ropa", "Zapato", "Accesorio"]:
            Categoria.objects.create(nombre=categoria)

        Producto.objects.create(
            codigo="2",
            cantidad=4,
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

    def test_no_esta_autenticado(self):
        """
        Prueba que al usuario no autenticado no se le
        permite acceso a la vista
        """
        url = reverse_lazy('inventario:editar', args=((Producto.objects.get(codigo="2")).pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_esta_autenticado_como_staff(self):
        """
        Prueba que el usuario autenticado y es del staff
        se le permite entrar a la vista
        """
        usuario_staff = {
            "danielrs": "danielrs19972705", # SuperUsuario
            "crucita": "crucita64", # Administrador
            "dwest06": "jaja123" # Vendedor
        }
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy('inventario:editar', args=((Producto.objects.get(codigo="2")).pk,))
        for usuario in usuario_staff:
            self.client.post(login, data={"username": usuario, "password": usuario_staff[usuario]})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_esta_autenticado_como_cliente(self):
        """
        Prueba que un usuario autenticado como
        cliente no puede acceder a esta vista
        """
        login = reverse_lazy("usuarios:login")
        url = reverse_lazy('inventario:editar', args=((Producto.objects.get(codigo="2")).pk,))
        self.client.post(login, data={"username": "rafaelrs", "password": "jaja123"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_mostrar_detalles_de_un_producto(self):
        '''
        Prueba que muestra los detalles de un producto
        con exito
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "crucita", "password": "crucita64"})
        url = reverse_lazy('inventario:editar', args=((Producto.objects.get(codigo="2")).pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_mostrar_detalles_de_un_producto_que_no_existe(self):
        '''
        Prueba que si un producto no existe
        arroja un error 404 Not Found
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "crucita", "password": "crucita64"})
        url = reverse_lazy('inventario:editar', args=(5,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.data)

    def test_actualizar_detalles_de_un_producto(self):
        '''
        Prueba que actualiza bien los detalles de un producto
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "crucita", "password": "crucita64"})
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
        self.assertEqual(producto_editado.costo, data['costo'],
                         msg="No se actualizo correctamente le producto")

    def test_eliminar_producto_que_existe(self):
        '''
        Prueba que elimina un producto con
        exito
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "crucita", "password": "crucita64"})
        producto_eliminar = Producto.objects.get(codigo="2")
        url = reverse_lazy('inventario:editar', args=(producto_eliminar.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         msg="No se elimino correctamente el producto")

    def test_eliminar_producto_que_no_existe(self):
        '''
        Prueba que muestra un error si el
        producto a eliminar no existe
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "crucita", "password": "crucita64"})
        url = reverse_lazy('inventario:editar', args=(8,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.data)

class ProductoBuscarViewTest(APITestCase):
    '''
    Clase que contiene las pruebas relacionadas
    a la vista encargada de la busqueda
    '''
    fixtures = ['groups.json', 'usuarios.json']

    def setUp(self):
        '''
        Pobla la base de datos con informacion
        para hacer las pruebas
        '''
        for categoria in ["Ropa", "Zapato", "Accesorio"]:
            Categoria.objects.create(nombre=categoria)

        Producto.objects.create(
            codigo="2",
            cantidad=2,
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

    def test_usuario_no_autenticado_no_puede_acceder_a_la_vista(self):
        """
        Prueba que un usuario no autenticado no puede
        buscar
        """
        url = reverse_lazy("inventario:buscar")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_usuario_staff_accede_a_la_vista(self):
        """
        Prueba que si un usuario pertenece al staff trata
        de acceder a la vista se le permite
        """
        usuario_staff = {
            "danielrs": "danielrs19972705", # SuperUsuario
            "crucita": "crucita64", # Administrador
            "dwest06": "jaja123" # Vendedor
        }
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy("inventario:buscar")
        for usuario in usuario_staff:
            self.client.post(login, data={"username": usuario, "password": usuario_staff[usuario]})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_cliente_no_puede_acceder_a_la_vista(self):
        """
        Prueba que el cliente no puede acceder a la
        vista de buscar
        """
        login = reverse_lazy('usuarios:login')
        url = reverse_lazy("inventario:buscar")
        self.client.post(login, data={"username": "rafaelrs", "password": "jaja123"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_busqueda_con_codigo_valido(self):
        '''
        Prueba que contiene un busqueda por codigo
        en la base de datos
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "danielrs", "password": "danielrs19972705"})
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
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "danielrs", "password": "danielrs19972705"})
        categoria = Categoria.objects.get(nombre="Ropa")
        url = reverse_lazy("inventario:buscar")
        url = url + "?categoria=" + str(categoria.pk)
        response = self.client.get(url)
        resultado_esperado = [
            ProductoSerializer(producto).data
            for producto in Producto.objects.filter(categoria=categoria)
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, resultado_esperado, msg=self.mensaje_query)

    def test_busqueda_con_varios_campos(self):
        '''
        Prueba la busqueda con varios campos
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "danielrs", "password": "danielrs19972705"})
        categoria = Categoria.objects.get(nombre="Ropa")
        url = reverse_lazy("inventario:buscar")
        url = url + "?categoria=" + str(categoria.pk) + "&talla=M"
        response = self.client.get(url)
        resultado_esperado = [
            ProductoSerializer(producto).data
            for producto in Producto.objects.filter(categoria=categoria, talla="M")
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, resultado_esperado, msg=self.mensaje_query)

    def test_busqueda_con_campo_invalido(self):
        '''
        Prueba realizar una busqueda con uno
        de los atributos invalido
        '''
        login = reverse_lazy('usuarios:login')
        self.client.post(login, data={"username": "danielrs", "password": "danielrs19972705"})
        url = reverse_lazy("inventario:buscar")
        url = url + "?costo=-1"
        response = self.client.get(url)
        resultado_esperado = []
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertEqual(response.data, resultado_esperado, msg=self.mensaje_query)
