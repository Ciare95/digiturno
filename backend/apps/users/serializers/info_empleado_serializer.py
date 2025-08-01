from rest_framework import serializers
from ..models import Empleado

class InfoEmpleadoSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()
    codigo_empleado = serializers.CharField()
    ventanilla_asignada = serializers.CharField()
    estado_conexion = serializers.BooleanField()

    class Meta:
        model = Empleado
        fields = ['nombre', 'codigo_empleado', 'ventanilla_asignada', 'estado_conexion']

    def get_nombre(self, obj):
        if obj.usuario.first_name and obj.usuario.last_name:
            return f"{obj.usuario.first_name} {obj.usuario.last_name}"
        return obj.usuario.username
