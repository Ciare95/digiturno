from rest_framework import serializers
from ..models import Turno


class TurnoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Turno"""
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Turno
        fields = [
            'id', 'numero_turno', 'servicio', 'servicio_nombre', 
            'sucursal', 'sucursal_nombre', 'nombre_cliente', 'numero_cedula',
            'estado', 'estado_display', 'fecha_creacion', 
            'fecha_inicio_atencion', 'fecha_finalizacion'
        ]
        read_only_fields = ['numero_turno', 'fecha_creacion', 'servicio_nombre', 
                          'sucursal_nombre', 'estado_display']
