from rest_framework import serializers
from ..models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Servicio"""
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    
    class Meta:
        model = Servicio
        fields = [
            'id', 'nombre', 'codigo_servicio', 'sucursal', 
            'sucursal_nombre', 'tiempo_estimado_atencion',
            'color_identificacion', 'icono', 'activo'
        ]