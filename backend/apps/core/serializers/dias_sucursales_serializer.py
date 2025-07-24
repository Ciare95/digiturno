from rest_framework import serializers
from ..models import DiaSucursal

class DiaSucursalSerializer(serializers.ModelSerializer):
    """Serializer para el modelo DiaSucursal"""
    class Meta:
        model = DiaSucursal
        fields = ['id', 'sucursal', 'dia_semana', 'hora_apertura', 'hora_cierre', 'activo']
        read_only_fields = ['id']
    