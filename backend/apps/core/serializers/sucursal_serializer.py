from rest_framework import serializers
from ..models import Sucursal

class SucursalSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Sucursal"""
    
    class Meta:
        model = Sucursal
        fields = [
            'id', 'nombre', 'codigo_sucursal', 'direccion', 
            'telefono', 'ciudad', 'departamento', 'activa'
        ]