from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from ..models import Administrador

class InicioSesionAdminSerializer(serializers.Serializer):
    """Serializador para el inicio de sesión de administradores"""
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

            # Si el usuario es superusuario, se le permite el acceso sin perfil de Administrador
            if usuario.is_superuser:
                # Crear un perfil de administrador temporal para la respuesta, si no existe
                admin, _ = Administrador.objects.get_or_create(
                    usuario=usuario,
                    defaults={'nivel_acceso': 'super_admin'}
                )
            else:
                # Verificar que el usuario tiene un perfil de administrador
                try:
                    admin = Administrador.objects.get(usuario=usuario)
                except Administrador.DoesNotExist:
                    msg = _('Este usuario no tiene permisos de administrador.')
                    raise serializers.ValidationError(msg, code='authorization')
        
        else:
            msg = _('Debe incluir "username" y "password".')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['usuario'] = usuario
        attrs['admin'] = admin
        return attrs