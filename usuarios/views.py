'''
Script que contendra las vistas para
esta aplicacion
'''
from django.shortcuts import render # pylint: disable=unused-import
from rest_framework import generics, permissions
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
from usuarios.permissions import (
    EsSuperUsuarioOAdministrador,
    IsNotAuthenticated,
    AdministradorNoModificaSuperUsuarios,
    UsuarioNoSeModificaAsiMismo)

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

class AdministracionUsuariosView(generics.RetrieveUpdateDestroyAPIView): # pylint: disable=too-many-ancestors
    """
    Vista que se encarga de ver los detalles
    de un usuario, poder eliminarlos y modificarlos.
    Tipos de usuario que pueden usar esta vista
        - SuperUsuario
        - Administrador
    Esta vista permite ver los detalles y
    eliminar los siguientes tipos de usuarios:
        - Vendedor
        - Cliente

    This view is in charge of show the
    details of a user, can delete it and modify it
    Types of users that can use this view
        - SuperUsuario
        - Administrador
    This view is able to show the details and
    delete the follow types of users:
        - Vendedor
        - Cliente
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        EsSuperUsuarioOAdministrador,
        AdministradorNoModificaSuperUsuarios,
        UsuarioNoSeModificaAsiMismo
    )
