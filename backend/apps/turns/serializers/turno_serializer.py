from rest_framework import serializers
from ..models import Turno
from ..services import GestorTurnos


class TurnoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Turno"""
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    tiempo_espera_estimado = serializers.SerializerMethodField()
    posicion_cola = serializers.SerializerMethodField()
    
    class Meta:
        model = Turno
        fields = [
            'id', 'numero_turno', 'servicio', 'servicio_nombre', 
            'sucursal', 'sucursal_nombre', 'nombre_cliente', 'numero_cedula',
            'estado', 'estado_display', 'fecha_creacion', 
            'fecha_inicio_atencion', 'fecha_finalizacion',
            'tiempo_espera_estimado', 'posicion_cola'
        ]
        read_only_fields = ['numero_turno', 'fecha_creacion', 'servicio_nombre', 
                          'sucursal_nombre', 'estado_display', 'tiempo_espera_estimado', 'posicion_cola']
    
    def get_tiempo_espera_estimado(self, obj):
        """Calcula el tiempo de espera estimado en minutos"""
        if obj.estado != Turno.EstadoTurno.EN_ESPERA:
            return 0
        
        # Obtener turnos en espera del mismo servicio y sucursal
        turnos_en_espera = Turno.objects.filter(
            servicio=obj.servicio,
            sucursal=obj.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA,
            fecha_creacion__lte=obj.fecha_creacion
        ).count()
        
        # Tiempo estimado: 5 minutos por turno por delante
        return turnos_en_espera * 5
    
    def get_posicion_cola(self, obj):
        """Calcula la posición en la cola"""
        if obj.estado != Turno.EstadoTurno.EN_ESPERA:
            return 0
        
        # Contar turnos en espera del mismo servicio y sucursal que llegaron antes
        posicion = Turno.objects.filter(
            servicio=obj.servicio,
            sucursal=obj.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA,
            fecha_creacion__lt=obj.fecha_creacion
        ).count()
        
        return posicion + 1
