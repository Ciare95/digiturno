from rest_framework import serializers
from ..models import Turno


class TurnoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Turno"""
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    empleado_nombre = serializers.CharField(source='empleado.usuario.get_full_name', read_only=True, allow_null=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True, allow_null=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Turno
        fields = [
            'id', 'numero_turno', 'usuario', 'usuario_nombre', 'servicio', 
            'servicio_nombre', 'sucursal', 'sucursal_nombre', 'empleado',
            'empleado_nombre', 'estado', 'estado_display',
            'fecha_creacion', 'fecha_llamado', 'fecha_inicio_atencion', 'fecha_finalizacion',
            'tiempo_espera_estimado', 'es_agendado',
            'fecha_agendada', 'observaciones'
        ]
        read_only_fields = ['numero_turno', 'fecha_creacion', 'fecha_atencion', 
                          'fecha_finalizacion', 'empleado_nombre', 'usuario_nombre', 
                          'servicio_nombre', 'sucursal_nombre', 'estado_display']
