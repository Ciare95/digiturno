from rest_framework import serializers
from ..models import Usuario, Empleado
from apps.core.models.sucursal import Sucursal
from apps.core.models.servicio import Servicio

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
            first_name=validated_data.get('first_name', validated_data['username']),
            last_name=validated_data.get('last_name', ''),
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
