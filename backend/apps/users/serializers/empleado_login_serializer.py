from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from ..models import Empleado
from ..serializers import UsuarioSerializer, EmpleadoSerializer

class EmpleadoLoginSerializer(serializers.Serializer):
    """Serializador para el inicio de sesión de empleados"""
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Autenticar usando username directamente
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                'No se puede iniciar sesión con las credenciales proporcionadas.',
                code='authorization'
            )

        if not hasattr(user, 'perfil_empleado'):
            raise serializers.ValidationError(
                'Este usuario no tiene perfil de empleado.',
                code='authorization'
            )

        data['usuario'] = user
        data['empleado'] = user.perfil_empleado
        return data

    def to_representation(self, instance):
        """
        Método para controlar la respuesta serializada
        """
        return {
            'usuario': UsuarioSerializer(instance['usuario']).data,
            'empleado': EmpleadoSerializer(instance['empleado']).data
        }