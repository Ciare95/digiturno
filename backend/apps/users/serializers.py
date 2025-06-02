from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import Usuario, Empleado, Administrador

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

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializador para mostrar información del usuario"""
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'cedula']
        read_only_fields = ['id']

class EmpleadoSerializer(serializers.ModelSerializer):
    """Serializador para mostrar información del empleado"""
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Empleado
        fields = ['usuario', 'codigo_empleado', 'sucursal', 'ventanilla_asignada', 'estado_conexion']

class AdministradorSerializer(serializers.ModelSerializer):
    """Serializador para mostrar información del administrador"""
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Administrador
        fields = ['usuario', 'nivel_acceso', 'permisos', 'sucursal']

class InicioSesionEmpleadoSerializer(serializers.Serializer):
    """Serializador para el inicio de sesión de empleados"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    codigo_empleado = serializers.CharField(required=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        codigo_empleado = attrs.get('codigo_empleado')
        
        if username and password and codigo_empleado:
            # Autenticar al usuario
            usuario = authenticate(request=self.context.get('request'), username=username, password=password)
            
            if not usuario:
                msg = _('No se pudo iniciar sesión con las credenciales proporcionadas.')
                raise serializers.ValidationError(msg, code='authorization')
            
            # Verificar que el usuario es un empleado y tiene el código correcto
            try:
                empleado = Empleado.objects.get(usuario=usuario, codigo_empleado=codigo_empleado)
            except Empleado.DoesNotExist:
                msg = _('Este usuario no es un empleado o el código de empleado es incorrecto.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Debe incluir "username", "password" y "codigo_empleado".')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['usuario'] = usuario
        attrs['empleado'] = empleado
        return attrs

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
            
            # Verificar que el usuario es un administrador
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
