from rest_framework import serializers
from ..models import Configuracion

class ConfiguracionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Configuracion"""
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    
    class Meta:
        model = Configuracion
        fields = [
            'id', 'clave', 'valor', 'descripcion', 'categoria',
            'es_global', 'sucursal', 'sucursal_nombre',
            'fecha_creacion', 'fecha_actualizacion'
        ]