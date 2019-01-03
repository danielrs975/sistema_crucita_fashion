"""
Script que contiene las pruebas
para las vistas de esta aplicacion
"""
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from usuarios.models import Usuario, Group

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
