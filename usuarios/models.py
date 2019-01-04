'''
Script que contendra los modelos de la base
de datos para este modulo
'''
from django.db import models # pylint: disable=unused-import
from django.contrib.auth.models import AbstractUser, Group

GRUPOS = ["SuperUsuario", "Administrador", "Vendedor", "Cliente"]

# Create your models here.
class Usuario(AbstractUser):
    """
    Clase que manejara los usuarios del sistema
    crucita fashion. Existiran tres tipo de usuarios
        - SuperUsuario: Que tiene el control sobre todo
        el sistema, puede eliminar usuarios, crear usuarios,
        modificar usuarios. Tiene control total sobre los datos
        del inventario, ventas y apartados
        - Administrador: Este usuario puede eliminar usuarios y
        modificar el perfil de su propio usuario. Ademas puede crear,
        eliminar o modificar datos del inventario y de
        las ventas y los apartados.
        - Vendedor: Este usuario puede modificar su
        propio perfil. Ademas puede crear, eliminar,
        modificar datos de las ventas y los apartados
        - Cliente: Este usuario puede modificar
        su propio perfil, crear su propio usuario.
        Ademas puede crear, eliminar y modificar
        datos de sus apartados.
    """
    grupo = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
