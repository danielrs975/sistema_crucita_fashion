"""
Script que contiene las pruebas
relacionadas con los serializers de esta
aplicacion
"""
from django.test import TestCase
from .serializers import UsuarioSerializer, RegistroSerializer
from .models import Usuario, Group, GRUPOS

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
        for grupo in GRUPOS:
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
        mensaje_error_1 = "Agrego perfectamente a pesar de "
        mensaje_error_2 = "que existe un usuario registrado con ese email"
        mensaje_error = mensaje_error_1 + mensaje_error_2
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertFalse(usuario_serializer.is_valid(),
                         msg=mensaje_error)

    def test_grupo_inexistente(self):
        """
        Metodo que se encarga de la prueba que
        verifica que el grupo introducido es valido
        dado un grupo que no existe
        """
        data = self.usuario_data
        data['grupo'] = -1
        usuario_serializer = UsuarioSerializer(data=data)
        self.assertFalse(usuario_serializer.is_valid(),
                         msg="Agrego con exito a pesar de que el grupo no existe")

class RegistroSerializerTest(TestCase):
    """
    Clase que contiene las pruebas para
    el serializer de Registro
    """
    def setUp(self):
        """
        Llena la base de datos con informacion
        inicial para correr las pruebas
        """
        for grupo in GRUPOS:
            Group.objects.create(name=grupo)
        self.usuario_data = {
            "first_name": "Rafael",
            "last_name" : "Rodriguez",
            "email"     : "rafaelrs975@gmail.com",
            "username"  : "rafaelrs",
            "password"  : "jaja123"
        }
    
    def test_grupo_no_puede_ser_distinto_a_vendedor(self):
        """
        Prueba que si un usuario que va a registrarse
        tiene un grupo distinto a None o a cliente.
        Es rechazado
        """
        data = self.usuario_data
        data['grupo'] = Group.objects.get(name="Administrador")
        registro_serializer = RegistroSerializer(data=data)
        self.assertFalse(registro_serializer.is_valid(),
                         msg="Agrego con exito a pesar de que el grupo es Administrador")

    def test_grupo_es_cliente(self):
        """
        Prueba que si un usuario que va a a registrarse
        su grupo es cliente. Es aceptado
        """
        data = self.usuario_data
        data['cliente'] = Group.objects.get(name="Cliente")
        registro_serializer = RegistroSerializer(data=data)
        self.assertTrue(registro_serializer.is_valid(),
                        msg=registro_serializer.errors)

    def test_grupo_es_none(self):
        """
        Prueba que si un usuario que va a registrarse
        su grupo es None. Es agregado exitosamente
        """
        data = self.usuario_data
        registro_serializer = RegistroSerializer(data=data)
        self.assertTrue(registro_serializer.is_valid(), msg=registro_serializer.errors)
