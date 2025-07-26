from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from ..models import Usuario

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    """Serializador para el registro de nuevos usuarios"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'cedula', 'password', 'password2']
    
    def validate(self, attrs):
        # Validar que las contraseñas coincidan
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": _("Las contraseñas no coinciden.")})
        return attrs
    
    def create(self, validated_data):
        # Eliminar password2 del diccionario ya que no es un campo del modelo
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        
        # Crear el usuario
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(password)
        usuario.save()
        
        return usuario