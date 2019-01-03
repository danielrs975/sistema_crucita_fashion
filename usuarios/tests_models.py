"""
Script que contiene las pruebas de los
modelos de esta aplicacion
"""
from django.test import TestCase
from django.contrib.auth.models import Group
from .models import Usuario

class UsuarioTests(TestCase):
    """
    Clase que contiene las pruebas hechas al
    modelo de Usuario
    """
    def setUp(self):
        """
        Metodo que agrega datos iniciales
        a la base de datos para comenzar las
        pruebas
        """
        for grupo in ["SuperUsuario", "Administrador", "Vendedor", "Cliente"]:
            Group.objects.create(name=grupo)

    def test_crear_usuario(self):
        """
        Se realiza la prueba de crear un
        usuario
        """
        usuario = Usuario(
            first_name="Daniel",
            last_name="Rodriguez",
            username="danielrs",
            email="danielrs9705@gmail.com",
            grupo=Group.objects.get(name="Administrador")
        )
        usuario.save()
        self.assertEqual(usuario, Usuario.objects.get(username="danielrs"),
                         msg="No agrego al usuario correctamente")
