from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class InicioSesionSerializer(serializers.Serializer):
    """Serializador para el inicio de sesión de usuarios"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # Autenticar al usuario
            usuario = authenticate(request=self.context.get('request'), username=username, password=password)
            
            if not usuario:
                msg = _('No se pudo iniciar sesión con las credenciales proporcionadas.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Debe incluir "username" y "password".')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['usuario'] = usuario
        return attrs