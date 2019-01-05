"""
Script que contiene las pruebas
para las vistas de esta aplicacion
"""
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from usuarios.models import Usuario, Group, GRUPOS
from usuarios.serializers import RegistroSerializer
from usuarios import views

class LoginViewTest(APITestCase):
    """
    Clase que contiene las pruebas para
    la vista del login
    """
    def setUp(self):
        """
        Inicializa la base de datos con
        informacion para correr las pruebas
        """
        for grupo in GRUPOS:
            Group.objects.create(name=grupo)
        self.usuario_data = {
            "first_name": "Daniel",
            "last_name" : "Rodriguez",
            "username"  : "danielrs",
            "email"     : "danielrs9705@gmail.com",
            "password"  : "jaja123",
            "repeat_password": "jaja123",
            "grupo"     : Group.objects.get(name="Cliente").pk
        }
        registro_serializer = RegistroSerializer(data=self.usuario_data)
        registro_serializer.is_valid()
        registro_serializer.save()
        self.url = reverse_lazy("usuarios:login")

    def test_login_view(self):
        """
        Prueba que la vista funcione correctamente
        """
        views.LoginView.as_view()

    def test_login_valido(self):
        """
        Prueba que la vista del login
        funcione con informacion valida
        """
        data = {"username": "danielrs", "password":"jaja123"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
    
    def test_login_invalido(self):
        """
        Prueba que si el usuario y el
        password es invalido no se puede loggear
        """
        data = {"username": "danielrs", "password": "jaja1234"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

class UsuarioRegistroView(APITestCase):
    """
    Clase que contiene las pruebas de la
    vista de registro
    """
    def setUp(self):
        """
        Metodo que llena la base de datos
        con informacion para correr las pruebas
        """
        self.grupos = [
            Group.objects.create(name=grupo) for grupo in GRUPOS
        ]
        self.usuario_data = {
            "first_name": "Daniel",
            "last_name" : "Rodriguez",
            "email"     : "danielrs9705@gmail.com",
            "username"  : "danielrs",
            "grupo"     : self.grupos[3].pk,
            "password"  : "jaja123",
            "repeat_password": "jaja123"
        }
        self.usuario_data_2 = {
            "first_name": "Rafael",
            "last_name" : "Rodriguez",
            "email"     : "rafael@gmail.com",
            "username"  : "rafaelrs",
            "grupo"     : self.grupos[3].pk,
            "password"  : "jaja123",
            "repeat_password": "jaja123"
        }
        registro = RegistroSerializer(data=self.usuario_data_2)
        registro.is_valid()
        registro.save()
        self.url = reverse_lazy("usuarios:registro")

    def test_registro_usuario_no_autenticado(self):
        """
        Prueba que si un usuario no autenticado
        trata de usar la vista se le permite usarla
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         msg=response.data)
    
    def test_registro_usuario_autenticado(self):
        """
        Prueba que si un usuario autenticado trata
        de entrar a la vista de registro va a hacer rechazado
        """
        login = reverse_lazy("usuarios:login")
        self.client.post(login, data={"username": "rafaelrs", "password": "jaja123"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_registrar_usuario_valido(self):
        """
        Prueba que un usuario con informacion
        valida puede registrarse
        """
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_login_de_usuario_recien_registrado(self):
        """
        Prueba que un usuario con informacion valida recien
        registrado pueda loggearse
        """
        login = reverse_lazy("usuarios:login")
        data = self.usuario_data
        self.client.post(self.url, data=data, format='json')
        response = self.client.post(login, data={"username": "danielrs", "password": "jaja123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
