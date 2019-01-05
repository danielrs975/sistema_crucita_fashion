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

class AdministradorNoModificaSuperUsuarios(permissions.BasePermission):
    """
    This class implement the following permission:
    Only the SuperUsuario can modify, see and
    delete its information

    Esta clase implementa el siguiente permiso:
    Solo el SuperUsuario puede modificar, ver y
    eliminar su propia informacion
    """

    def has_object_permission(self, request, view, obj):
        """
        This method verify that if the user is an
        Administrador, and try to modify, delete or
        see the details of the SuperUsuario or another
        administrator

        Este metodo verifica que si un usuario es
        un Administrador, y intenta modificar,
        eliminar o ver los detalles del SuperUsuario o
        de otro administrador
        """
        is_grupo_usuario_admin = request.user.grupo.name == "Administrador"
        is_grupo_obj_superuser = (obj.grupo.name == "SuperUsuario" or
                                  obj.grupo.name == "Administrador")
        if is_grupo_usuario_admin and is_grupo_obj_superuser:
            return False

        return True

class UsuarioNoSeModificaAsiMismo(permissions.BasePermission):
    """
    This class implement the following permission:
    Users can only modify users differents that its

    Esta clase implementa el siguiente permiso:
    Usuarios solo pueden modificar usuarios distintos
    de el
    """

    def has_object_permission(self, request, view, obj):
        """
        This method verify that a user cant modify its own
        information

        Este metodo verifica que un usuario no pueda modificar
        su propia informacion
        """
        usuario_request = request.user
        usuario_a_modificar = obj

        return usuario_request != usuario_a_modificar

class VendedorOnly(permissions.BasePermission):
    """
    Clase que implementa el permiso
    de que solo los vendedores pueden ver la vista
    en la cual esta este permiso
    """
    def has_permission(self, request, view):
        """
        Metodo que implementa el permiso
        de VendedorOnly
        """
        usuario = request.user
        return str(usuario.grupo) == "Vendedor"

    def has_object_permission(self, request, view, obj):
        """
        Metodo que verifica que los detalles
        de los usuarios que el vendedor puede ver
        solo sea del tipo Cliente
        """
        grupo = obj.grupo
        return str(grupo) == "Cliente"
