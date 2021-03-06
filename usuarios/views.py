'''
Script que contendra las vistas para
esta aplicacion
'''
from django.shortcuts import render # pylint: disable=unused-import
from django.contrib.auth import authenticate, login
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer, RegistroSerializer, DetallesSerializer
from usuarios.permissions import (
    EsSuperUsuarioOAdministrador,
    IsNotAuthenticated,
    AdministradorNoModificaSuperUsuarios,
    UsuarioNoSeModificaAsiMismo,
    VendedorOnly,
    OwnerOnly,
)
from crucita_fashion.permissions import IsStaff

# Create your views here.

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
    serializer_class = RegistroSerializer
    permission_classes = (
        IsNotAuthenticated,
    )

class LoginView(views.APIView):
    """
    Vista que maneja el login de los usuarios
    al sistema
    """

    def post(self, request):
        """
        Sobreescribe la funcion del post
        para que pueda hacer el login en la api
        """
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class AdministracionCrearUsuariosView(generics.CreateAPIView):
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

class AdministracionUsuariosView(generics.RetrieveDestroyAPIView): # pylint: disable=too-many-ancestors
    """
    Vista que se encarga de ver los detalles
    de un usuario, poder eliminarlos.
    Tipos de usuario que pueden usar esta vista
        - SuperUsuario
        - Administrador
    Esta vista permite ver los detalles y
    eliminar los siguientes tipos de usuarios:
        - Vendedor
        - Cliente

    This view is in charge of show the
    details of a user, can delete it.
    Types of users that can use this view
        - SuperUsuario
        - Administrador
    This view is able to show the details and
    delete the follow types of users:
        - Vendedor
        - Cliente
    """
    queryset = Usuario.objects.all()
    serializer_class = DetallesSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        EsSuperUsuarioOAdministrador,
        AdministradorNoModificaSuperUsuarios,
        UsuarioNoSeModificaAsiMismo
    )

class VendedorUsuarioView(generics.RetrieveAPIView):
    """
    Clase que maneja la vista de los detalles
    de un usuario siendo vendedor
    """
    queryset = Usuario.objects.all()
    serializer_class = DetallesSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        VendedorOnly,
    )

class UsuarioBuscarView(generics.ListAPIView):
    """
    Vista que implementa la busqueda de algun
    usuario registrado en el sistema
    """
    queryset = Usuario.objects.all()
    serializer_class = DetallesSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('username', 'email', 'first_name', 'last_name', 'grupo',)
    permission_classes = (
        permissions.IsAuthenticated,
        IsStaff,
    )

class PerfilView(generics.RetrieveUpdateAPIView):
    """
    Clase que implementa la vista que permite
    al usuario actualizar la informacion de
    su perfil
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        OwnerOnly,
    )
