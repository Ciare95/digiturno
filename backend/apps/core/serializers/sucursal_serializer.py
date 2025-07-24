from rest_framework import serializers
from ..models import Sucursal
from .servicio_serializer import ServicioSerializer

class SucursalSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Sucursal"""
    servicios = ServicioSerializer(many=True, read_only=True, source='servicio_set')
    
    class Meta:
        model = Sucursal
        fields = [
            'id', 'nombre', 'codigo_sucursal', 'direccion', 'descripcion',
            'telefono', 'ciudad', 'departamento', 'activa', 'servicios'
        ]