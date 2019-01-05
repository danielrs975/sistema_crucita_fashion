"""
Script que contiene los serializers
para el modelo Usuario
"""
from rest_framework import serializers
from .models import Usuario, Group

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

    def create(self, validated_data):
        """
        Este metodo sobreescribe el create original
        para agregar como informacion del atributo
        repeat_password
        """
        usuario_registrado = Usuario.objects.create(**validated_data)
        usuario_registrado.repeat_password = validated_data['password']
        usuario_registrado.set_password(validated_data['password'])
        usuario_registrado.save()
        return usuario_registrado

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

class RegistroSerializer(serializers.ModelSerializer):
    """
    Clase que contiene el serializer que sera usado
    para el registro
    """
    def validate(self, data):
        """
        Valida que la clave y el campo donde
        se repite la clave sean iguales
        """
        clave = data['password']
        clave_repetida = data['repeat_password']
        if clave != clave_repetida:
            raise serializers.ValidationError("Las claves no son iguales")
        return data

    def validate_grupo(self, grupo): # pylint: disable=no-self-use
        """
        Validator para el campo grupo: valida
        que el unico grupo al cual puede pertenecerse
        si usa el registro es cliente
        """
        message = "Este serializer no admite la escogencia de un grupo"
        if grupo is not None and grupo.name in ["SuperUsuario", "Administrador", "Vendedor"]:
            raise serializers.ValidationError(message)
        return grupo

    def create(self, validated_data):
        """
        Este metodo sobreescribe el create original
        para agregar como informacion el grupo donde
        pertenece el usuario que va a ser Cliente
        """
        usuario_registrado = Usuario.objects.create(**validated_data)
        usuario_registrado.grupo = Group.objects.get(name="Cliente")
        usuario_registrado.set_password(validated_data['password'])
        usuario_registrado.save()
        return usuario_registrado

    class Meta:
        model = Usuario
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'grupo',
            'password',
            'repeat_password'
        )
