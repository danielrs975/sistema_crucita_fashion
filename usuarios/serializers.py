"""
Script que contiene los serializers
para el modelo Usuario
"""
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Clase que contiene el serializer para el
    modelo de Usuario
    """

    def validate_grupo(self, grupo): # pylint: disable=no-self-use
        """
        Validator para el campo grupo: valida
        que si un usuario es SuperUsuario no exista
        otro SuperUsuario, es decir, solo hay un solo
        SuperUsuario en el sistema
        """
        if grupo.name == "SuperUsuario":
            if grupo.usuario_set.count() == 1:
                raise serializers.ValidationError("No puede haber mas SuperUsuarios")
        return grupo

    class Meta:
        model = Usuario
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'grupo',
            'password'
        )
