"""
Modulo que contiene los permisos
para esta app
"""
from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    """
    Clase que verifica que un usuario es pertenece
    a la administracion de la tienda
    """
    def has_permission(self, request, view):
        """
        Verifica que el usuario que esta creando, viendo o
        buscando sea SuperUsuario, Administrador o Vendedor
        """
        usuario_loggeado = request.user
        grupo = usuario_loggeado.grupo.name
        return grupo in ["SuperUsuario", "Administrador", "Vendedor"]
