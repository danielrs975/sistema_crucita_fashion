"""
Script que contiene los permisos
que estan relacionado con los usuarios
"""
from rest_framework import permissions

class EsSuperUsuarioOAdministrador(permissions.BasePermission):
    """
    Permiso que solo permite a los superusuarios
    usar las vistas en las cuales esta esta 
    restriccion
    """

    def has_permission(self, request, view):
        """
        Metodo que verifica que el usuario
        que trata de acceder a la vista es
        SuperUsuario
        """
        usuario = request.user
        grupo = usuario.grupo
        return grupo.name in ["SuperUsuario", "Administrador"]
    
class IsNotAuthenticated(permissions.BasePermission):
    """
    This implement the following permission:
    Only not authenticated user can use the views
    that use this class

    Esto implementa el siguiente permiso:
    Solo los usuarios no autenticados pueden usar
    las vistas que usan esta clase
    """

    def has_permission(self, request, view):
        """
        This method verify that the user
        who uses the view is not authenticated

        Este metodo verifica que el usuario
        que usa la vista este no autenticado
        """
        usuario = request.user
        return str(usuario) == "AnonymousUser"
