'''
Script que contendra las vistas para
esta aplicacion
'''
from django.shortcuts import render # pylint: disable=unused-import
from rest_framework import generics, permissions
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
from usuarios.permissions import EsSuperUsuario

# Create your views here.

class UsuarioCrearViewSuperUsuario(generics.CreateAPIView):
    """
    Vista que se encarga de la creacion de los
    usuarios para el sistema. Tipo de usuarios
    que pueden usar esta vista
        - SuperUsuario
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        EsSuperUsuario,
    )
