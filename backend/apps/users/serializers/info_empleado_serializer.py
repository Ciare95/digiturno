from rest_framework import serializers
from ..models import Empleado
from apps.core.models.servicio import Servicio

class ServicioEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'codigo_servicio']

class InfoEmpleadoSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    codigo_empleado = serializers.CharField()
    ventanilla_asignada = serializers.CharField()
    estado_conexion = serializers.BooleanField()
    sucursal_nombre = serializers.SerializerMethodField()
    servicios = ServicioEmpleadoSerializer(many=True, source='servicios.all')

    class Meta:
        model = Empleado
        fields = ['nombre', 'codigo_empleado', 'ventanilla_asignada', 'estado_conexion', 'sucursal_nombre', 'servicios']

    def get_nombre(self, obj):
        if obj.usuario.first_name and obj.usuario.last_name:
            return f"{obj.usuario.first_name} {obj.usuario.last_name}"
        return obj.usuario.username

    def get_sucursal_nombre(self, obj):
        return obj.sucursal.nombre if obj.sucursal else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Filtrar solo servicios activos
        if 'servicios' in data:
            data['servicios'] = [
                servicio for servicio in data['servicios']
                if servicio and instance.asignaciones_servicio.filter(servicio_id=servicio['id'], activo=True).exists()
            ]
        return data
