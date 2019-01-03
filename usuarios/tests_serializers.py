"""
Script que contiene las pruebas 
relacionadas con los serializers de esta
aplicacion
"""
from django.test import TestCase
from .serializers import UsuarioSerializer
from .models import Usuario, Group

class UsuarioSerializerTest(TestCase):
    """
    Clase que contiene las pruebas relacionadas
    con el UsuarioSerializer
    """
    def setUp(self):
        """
        Metodo que agrega informacion a la base de
        datos para hacer las pruebas
        """
        for grupo in ["SuperUsuario", "Administrador", "Vendedor", "Cliente"]:
            Group.objects.create(name=grupo)

        Usuario.objects.create(
            first_name="Daniel",
            last_name="Rodriguez",
            email="danielrs9705@gmail.com",
            username="danielrs",
            grupo=Group.objects.get(name="SuperUsuario"),
            password="123jaja"
        )
        self.usuario_data = {
            "first_name": "Rafael",
            "last_name": "Rodriguez",
            "email": "rafaelrs975@gmail.com",
            "username": "rafaelrs",
            "grupo": Group.objects.get(name="Administrador").pk,
            "password": "123jaja"
        }

    def test_crear_usuario_valido(self):
        """
        Metodo que se encarga de la prueba de 
        agregar un usuario valido
        """
        data = self.usuario_data
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertTrue(usuario_serializer.is_valid(), msg=usuario_serializer.errors)

    def test_crear_usuario_con_username_existente(self):
        """
        Metodo que se encarga de probar de que no se
        puede agregar un usuario con un username ya
        existente
        """
        data = {
            "first_name": "Rafael",
            "last_name": "Rodriguez",
            "email": "rafaelrs975@gmail.com",
            "username": "danielrs",
            "grupo": Group.objects.get(name="Administrador").pk,
            "password": "123jaja"
        }
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertFalse(usuario_serializer.is_valid(), msg=usuario_serializer.errors)

    def test_no_mas_de_un_superusuario(self):
        """
        Metodo que se encarga de la prueba que no
        puede haber mas de un superusuario en el 
        sistema
        """
        data = {
            "first_name": "Rafael",
            "last_name": "Rodriguez",
            "email": "rafaelrs975@gmail.com",
            "username": "rafaelrs",
            "grupo": Group.objects.get(name="SuperUsuario").pk,
            "password": "123jaja"
        }
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertFalse(usuario_serializer.is_valid(), msg=usuario_serializer.errors)

    def test_email_invalido(self):
        """
        Metodo que se encarga de la prueba que 
        verifica la validacion de que un email es
        valido
        """
        data = self.usuario_data
        data['email'] = "rafaelrs975gmail.com"
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertFalse(usuario_serializer.is_valid(), msg=usuario_serializer.errors)

    def test_email_valido(self):
        """
        Metodo que se encarga de la prueba que
        verifica la validacion de que un email es
        valido dado un formato correcto
        """
        data = self.usuario_data
        data['email'] = "hola@hotmail.com"
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertTrue(usuario_serializer.is_valid(), msg=usuario_serializer.errors)

    def test_email_unico(self):
        """
        Metodo que se encarga de la prueba que
        verifica la unicidad del email
        """
        data = self.usuario_data
        data['email'] = "danielrs9705@gmail.com"
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertFalse(usuario_serializer.is_valid(),
                         msg="Agrego perfectamente a pesar de que existe un usuario registrado con ese email")
