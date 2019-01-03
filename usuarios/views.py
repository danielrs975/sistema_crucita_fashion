'''
Script que contendra las vistas para
esta aplicacion
'''
from django.shortcuts import render # pylint: disable=unused-import
from rest_framework import generics, permissions
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
from usuarios.permissions import EsSuperUsuarioOAdministrador, IsNotAuthenticated

# Create your views here.

class UsuarioCrearViewSuperUsuario(generics.CreateAPIView):
    """
    Vista que se encarga de la creacion de los
    usuarios para el sistema. Tipo de usuarios
    que pueden usar esta vista
        - SuperUsuario
        - Administrador
    Esta vista maneja la creacion de los usuarios
    que pertenezcan a los siguientes grupos:
        - Administrador
        - Vendedor
        - Cliente
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        EsSuperUsuarioOAdministrador,
    )

class UsuarioRegistroView(generics.CreateAPIView):
    """
    Vista que se encarga de manejar la creacion de
    los usuarios creados por los clientes que van
    a usar la api. Tipo de usuarios que pueden
    usar esta vista
        - Usuarios no autenticados
    Esta vista maneja la creacion de los usuarios
    que pertenezcan a estos grupos:
        - Cliente
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (
        IsNotAuthenticated,
    )
