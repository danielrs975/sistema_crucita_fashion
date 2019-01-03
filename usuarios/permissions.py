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
        if grupo.name in ["SuperUsuario", "Administrador"]:
            return True
        return False