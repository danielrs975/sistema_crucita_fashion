"""
Script que contiene las pruebas
para las vistas de esta aplicacion
"""
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from usuarios.models import Usuario, Group, GRUPOS

class UsuarioCrearViewSuperUsuarioTest(APITestCase):
    """
    Clase que contiene las pruebas de
    la vista crear usuario
    """
    def setUp(self):
        """
        Agrega datos a la base de datos para
        poder realizar las pruebas
        """
        for grupo in ['SuperUsuario', 'Administrador', 'Vendedor', 'Cliente']:
            Group.objects.create(name=grupo)

        Usuario.objects.create(
            first_name="Daniel",
            last_name="Rodriguez",
            username="danielrs",
            email="danielrs9705@gmail.com",
            grupo=Group.objects.get(name="SuperUsuario"),
            password="jaja123"
        )
        Usuario.objects.create(
            first_name="David",
            last_name="Rodriguez",
            username="dwest06",
            email="david00dark@gmail.com",
            grupo=Group.objects.get(name="Administrador"),
            password="jaja123"
        )
        Usuario.objects.create(
            first_name="Cruz",
            last_name="Sanchez",
            username="crucita",
            email="crucita@gmail.com",
            grupo=Group.objects.get(name="Vendedor"),
            password="jaja123"
        )
        self.usuario_data = {
            "first_name": "Rafael",
            "last_name" : "Rodriguez",
            "username"  : "rafaelrs",
            "email"     : "hola@gmail.com",
            "grupo"     : Group.objects.get(name="Administrador").pk,
            "password"  : "jaja123"
        }
        self.url = reverse_lazy('usuarios:crear')


    def test_usuario_no_esta_autenticado(self):
        """
        Prueba de que si el usuario no esta
        autenticado no le permite usar la vista
        de crear
        """
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_usuario_esta_autenticado_es_administrador(self):
        """
        Prueba de que si el usuario esta autenticado
        se le permite usar la vista
        """
        self.client.force_login(Usuario.objects.get(username="dwest06"))
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_usuario_esta_autenticado_es_superusuario(self):
        """
        Prueba de que si el usuario es superusuario
        se le permite usar la vista
        """
        self.client.force_login(Usuario.objects.get(username="danielrs"))
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_usuario_no_es_superusuario_ni_administrador(self):
        """
        Prueba de que si el usuario no es superusuario
        no se le permite usar la vista
        """
        self.client.force_login(Usuario.objects.get(username="crucita"))
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

class UsuarioRegistroViewTest(APITestCase):
    """
    This class contains the tests for the
    UsuarioCrearView for no authenticated users

    Esta clase contiene las pruebas para la vista
    UsuarioCrearView para usuarios no autenticados
    """
    def setUp(self):
        """
        This method fill de database with information
        to use in the tests

        Este metodo llena la base de datos con
        informacion para usar en las pruebas
        """
        for grupo in ["SuperUsuario", "Administrador", "Vendedor", "Cliente"]:
            Group.objects.create(name=grupo)

        Usuario.objects.create(
            first_name="David",
            last_name="Rodriguez",
            username="dwest06",
            email="david00dark@gmail.com",
            grupo=Group.objects.get(name="Administrador"),
            password="jaja123"
        )
        self.usuario_data = {
            "first_name": "Rafael",
            "last_name" : "Rodriguez",
            "username"  : "rafaelrs",
            "email"     : "hola@gmail.com",
            "grupo"     : Group.objects.get(name="Administrador").pk,
            "password"  : "jaja123"
        }
        self.url = reverse_lazy("usuarios:registro")

    def test_vista_con_usuario_autenticado(self):
        """
        Test that if a user is authenticated and
        try to access the view, it is gonna be
        rejected

        Prueba que si un usuario esta autenticado
        y intenta acceder a la vista, sera rechazado
        """
        self.client.force_login(user=Usuario.objects.get(username="dwest06"))
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_vista_con_usuario_no_autenticado_registro(self):
        """
        Test that is a user is not authenticated and
        try to make a POST to the view, it succeed

        Prueba que si un usuario no esta autenticado
        y intenta registrarse en la vista, tendra
        exito
        """
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

class UsuarioDetallesViewTest(APITestCase):
    """
    This class has the tests of the UsuarioDetalles
    view

    Esta clase tiene las pruebas de la vista
    UsuarioDetalles
    """
    def setUp(self):
        """
        This method fill the database with
        initial information for the tests

        Este metodo llena la base de datos con
        informacion para hacer las pruebas
        """
        for grupo in ["SuperUsuario", "Administrador", "Vendedor", "Cliente"]:
            Group.objects.create(name=grupo)
        self.usuario_superuser = Usuario.objects.create(
            first_name="Daniel",
            last_name="Rodriguez",
            username="danielrs",
            email="danielrs9705@gmail.com",
            grupo=Group.objects.get(name="SuperUsuario"),
            password="jaja123"
        )
        self.usuario_admin = Usuario.objects.create(
            first_name="David",
            last_name="Rodriguez",
            username="dwest06",
            email="david00dark@gmail.com",
            grupo=Group.objects.get(name="Administrador"),
            password="jaja123"
        )
        self.usuario_vendedor = Usuario.objects.create(
            first_name="Cruz",
            last_name="Sanchez",
            username="crucita",
            email="crucita@gmail.com",
            grupo=Group.objects.get(name="Vendedor"),
            password="jaja123"
        )
        self.url_usuario_1 = reverse_lazy("usuarios:detalles",
                                          args=(Usuario.objects.get(username="danielrs").pk,))
        self.url_usuario_2 = reverse_lazy("usuarios:detalles",
                                          args=(Usuario.objects.get(username="dwest06").pk,))
        self.url_usuario_3 = reverse_lazy("usuarios:detalles",
                                          args=(Usuario.objects.get(username="crucita").pk,))
        self.usuario_data = {
            "first_name": "Rafael",
            "last_name" : "Rodriguez",
            "username"  : "rafaelrs",
            "email"     : "hola@gmail.com",
            "grupo"     : Group.objects.get(name="Administrador").pk,
            "password"  : "jaja123"
        }

    def test_detalles_no_autenticado(self):
        """
        This method test that if an user not
        authenticated try to use the view is
        gonna get rejected

        Este metodo prueba que si un usuario no
        esta autenticado y trata de usar la vista
        entonces sera rechazado
        """
        response = self.client.get(self.url_usuario_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_detalles_autenticado_administrador(self):
        """
        This method test that if an user authenticated
        try to make a GET request, its succeed

        Este metodo prueba que si un usuario autenticado
        como administrador trata de hacer un GET, entonces
        lo logra
        """
        self.client.force_login(user=self.usuario_admin)
        response = self.client.get(self.url_usuario_3)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)


    def test_detalles_autenticado_superusuario(self):
        """
        This method test that if an user authenticated
        as a SuperUsuario try to make a GET request, its
        succeed

        Este metodo prueba que si un usuario autenticado
        como SuperUsuario trata de hacer un GET, entonces
        lo logra
        """
        self.client.force_login(user=self.usuario_superuser)
        response = self.client.get(self.url_usuario_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_detalles_autenticado_usuario_normal(self):
        """
        This method test that if an user authenticated
        as a normal user (Vendedor, Cliente) try to make
        a GET request, it's gonna be rejected

        Este metodo prueba que si un usuario autenticado
        como un usuario normal (Vendedor, Cliente) intenta
        hacer un GET, entonces es rechazado
        """
        self.client.force_login(user=self.usuario_vendedor)
        response = self.client.get(self.url_usuario_3)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_detalles_superusuario(self):
        """
        This method test that if an superuser try
        to access its own information, its fail

        Este metodo prueba que si un superusuario trata
        de acceder a su propia informacion, falla
        """
        self.client.force_login(user=self.usuario_superuser)
        response = self.client.get(self.url_usuario_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_update_administrador_modifica_superusuario(self):
        """
        This method test that if an user authenticated as
        an administrator try to make a PUT request to
        a SuperUser, it's gonna be rejected

        Este metodo prueba que si un usuario autenticado
        como un administrador intenta modificar a un
        SuperUsuario, va s ser rechazado
        """
        self.client.force_login(user=self.usuario_admin)
        data = self.usuario_data
        response = self.client.put(self.url_usuario_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_update_administrador_modifica_administrador(self):
        """
        This method test that if an administrator try to
        modify another administrator, its fails

        Este metodo prueba que si un administrador trata
        de modificar a otro administrador, falla
        """
        self.client.force_login(user=self.usuario_admin)
        data = self.usuario_data
        response = self.client.put(self.url_usuario_2, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_update_administrador_usuario_normal(self):
        """
        This method test that if an administrator try to
        modify a normal user then its succeed

        Este metodo prueba que si un administrador trata de
        modificar a un usuario normal entonces lo logra
        """
        self.client.force_login(user=self.usuario_admin)
        data = self.usuario_data
        response = self.client.put(self.url_usuario_3, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_update_superusuario_modifica_administrador(self):
        """
        This method test that if an superuser try to
        modify an administrator, its succeed

        Este prueba que si un superusuario intenta
        modificar a un administrador, lo va lograr
        """
        self.client.force_login(user=self.usuario_superuser)
        data = self.usuario_data
        response = self.client.put(self.url_usuario_2, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_update_superusuario_se_modifica_asi_mismo(self):
        """
        This method test that if an superuser try to
        modify its own information, its get rejected

        Este metodo prueba que si un superusuario trata
        de modificar si propia informacion, falla
        """
        self.client.force_login(user=self.usuario_superuser)
        data = self.usuario_data
        response = self.client.put(self.url_usuario_1, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_update_superusuario_modifica_usuario_normal(self):
        """
        This method test that if an superuser try to
        modify a normal user, its succeed

        Este metodo prueba que si un superusuario trata
        de modificar a un usuario normal, lo logra
        """
        self.client.force_login(user=self.usuario_superuser)
        data = self.usuario_data
        response = self.client.put(self.url_usuario_3, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_delete_administrador_superusuario(self):
        """
        This method test that if an administrador try to
        delete an superuser, its fail

        Este metodo prueba que si un administrador trata
        de eliminar a un superusuario falla
        """
        self.client.force_login(user=self.usuario_admin)
        response = self.client.delete(self.url_usuario_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_delete_administrador_administrador(self):
        """
        This method test that if an administrator try to
        delete another administrator, its fail

        Este metodo prueba que si un administrador trata de
        eliminar a otro administrador, falla
        """
        self.client.force_login(user=self.usuario_admin)
        response = self.client.delete(self.url_usuario_2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_delete_administrador_usuario_normal(self):
        """
        This method test that if an administrator try to
        delete a normal user, its succeed

        Este metodo prueba que si un administrador trata de
        eliminar a usuario normal, lo logra
        """
        self.client.force_login(user=self.usuario_admin)
        response = self.client.delete(self.url_usuario_3)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)

    def test_delete_superusuario_administrador(self):
        """
        This method test that if a superuser try to
        delete an administrator, its succeed

        Este metodo prueba que si un superusuario trata
        de eliminar a un administrador, lo logra
        """
        self.client.force_login(user=self.usuario_superuser)
        response = self.client.delete(self.url_usuario_2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)

    def test_delete_superusuario_usuario_normal(self):
        """
        This method test that if a superuser try to
        delete a normal user, its succeed

        Este metodo prueba que si un superusuario trata
        de eliminar a un usuario normal, lo logra
        """
        self.client.force_login(user=self.usuario_superuser)
        response = self.client.delete(self.url_usuario_3)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)

    def test_superusuario_delete_itself(self):
        """
        This method test that if a superuser try to
        delete itsel, its get rejected

        Este metodo prueba que si un superusuario se
        trata de eliminar asi mismo, falla
        """
        self.client.force_login(user=self.usuario_superuser)
        response = self.client.delete(self.url_usuario_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

class LoginTest(APITestCase):
    """
    Clase que contiene las pruebas de la
    vista del login
    """
    def setUp(self):
        """
        Llena la base de datos con informacion inicial
        para correr las pruebas
        """
        for grupo in GRUPOS:
            Group.objects.create(name=grupo)
        Usuario.objects.create(
            first_name="Daniel",
            last_name="Rodriguez",
            username="danielrs",
            grupo=Group.objects.get(name="Administrador"),
            password="jaja123"
        )
        self.usuario_login = {
            'username': "danielrs",
            'password': "jaja123"
        }
        self.url = reverse_lazy("usuarios:login")

    def test_login_con_informacion_valida(self):
        """
        Prueba que el login se realiza con exito
        si la informacion suministrada es correcta
        """
        data = self.usuario_login
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
