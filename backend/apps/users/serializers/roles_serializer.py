from rest_framework import serializers
from ..models import Usuario, Empleado, Administrador

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializador para mostrar información del usuario"""
    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre_completo', 'email', 'cedula', 'telefono', 'ultimo_acceso', 'is_staff', 'is_superuser']
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
