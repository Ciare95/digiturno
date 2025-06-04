from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import Usuario, Empleado, Administrador
from apps.core.models import Sucursal, Servicio

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

class EmpleadoLoginSerializer(serializers.Serializer):
    """Serializador para el inicio de sesión de empleados"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Buscar el usuario por email
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('No se puede iniciar sesión con las credenciales proporcionadas.', code='authorization')

        # Autenticar usando username
        user_auth = authenticate(request=self.context.get('request'), username=user.username, password=password)
        if not user_auth:
            raise serializers.ValidationError('No se puede iniciar sesión con las credenciales proporcionadas.', code='authorization')

        if not hasattr(user_auth, 'perfil_empleado'):
            raise serializers.ValidationError('Este usuario no tiene perfil de empleado.', code='authorization')

        data['usuario'] = user_auth
        data['empleado'] = user_auth.perfil_empleado
        return data

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


class RegistroEmpleadoSerializer(serializers.ModelSerializer):
    """Serializador para el registro de nuevos empleados"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    codigo_empleado = serializers.CharField(required=True, max_length=20)
    sucursal_id = serializers.PrimaryKeyRelatedField(
        queryset=Sucursal.objects.all(),
        source='sucursal',
        required=True
    )
    servicios = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Servicio.objects.all(),
        required=False
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'codigo_empleado', 'sucursal_id', 'servicios', 'telefono', 'cedula'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_username(self, value):
        if Usuario.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    def validate_codigo_empleado(self, value):
        if Empleado.objects.filter(codigo_empleado=value).exists():
            raise serializers.ValidationError("Este código de empleado ya está en uso.")
        return value

    def create(self, validated_data):
        # Extraer datos específicos de empleado
        codigo_empleado = validated_data.pop('codigo_empleado')
        sucursal = validated_data.pop('sucursal')
        servicios = validated_data.pop('servicios', [])

        # Crear usuario
        user = Usuario(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telefono=validated_data.get('telefono', ''),
            cedula=validated_data.get('cedula', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        # Crear perfil de empleado
        empleado = Empleado.objects.create(
            usuario=user,
            codigo_empleado=codigo_empleado,
            sucursal=sucursal
        )
        if servicios:
            empleado.servicios.set(servicios)

        return user
