from rest_framework import serializers
from ..models import ColaTurnos

class ColaTurnosSerializer(serializers.ModelSerializer):
    """Serializador para la cola de turnos"""
    turno_numero = serializers.CharField(source='turno.numero_turno', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    estado_turno = serializers.CharField(source='turno.get_estado_display', read_only=True)
    cliente_nombre = serializers.CharField(source='turno.nombre_cliente', read_only=True)
    
    class Meta:
        model = ColaTurnos
        fields = [
            'id', 'turno', 'turno_numero', 'servicio', 'servicio_nombre', 
            'posicion_cola', 'tiempo_espera_estimado', 'activo',
            'estado_turno', 'cliente_nombre'
        ]
        read_only_fields = ['turno_numero', 'servicio_nombre', 'estado_turno', 'cliente_nombre']
