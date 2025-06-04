from rest_framework import serializers
from apps.turns.models import Turno, CalificacionServicio
from apps.users.models import Usuario, Empleado
from apps.core.models import Servicio, Sucursal


class DashboardAdminSerializer(serializers.Serializer):
    """Serializador para el dashboard del administrador"""
    # Estadísticas generales
    total_usuarios = serializers.IntegerField()
    total_empleados = serializers.IntegerField()
    total_servicios_activos = serializers.IntegerField()
    total_sucursales_activas = serializers.IntegerField()
    
    # Estadísticas de turnos
    turnos_hoy = serializers.IntegerField()
    turnos_en_espera = serializers.IntegerField()
    turnos_en_atencion = serializers.IntegerField()
    turnos_finalizados = serializers.IntegerField()
    turnos_cancelados = serializers.IntegerField()
    tiempo_espera_promedio = serializers.DurationField()
    
    # Distribución por servicios
    servicios_mas_demandados = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()  # Changed from IntegerField to CharField
        )
    )
    
    # Calificaciones y satisfacción
    calificacion_promedio_general = serializers.FloatField()
    total_calificaciones = serializers.IntegerField()
    distribucion_calificaciones = serializers.DictField(
        child=serializers.IntegerField()
    )
    
    # Performance por sucursal
    rendimiento_sucursales = serializers.ListField(
        child=serializers.DictField(
            child=serializers.DictField()
        )
    )


class ReporteAvanzadoSerializer(serializers.Serializer):
    """Serializador para reportes avanzados del administrador"""
    # Estadísticas por rango de fechas
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
    
    # Métricas de turnos
    total_turnos = serializers.IntegerField()
    promedio_turnos_diario = serializers.FloatField()
    tiempo_espera_promedio = serializers.DurationField()
    tiempo_atencion_promedio = serializers.DurationField()
    
    # Métricas por servicio
    servicios = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    # Métricas por empleado
    empleados = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    # Métricas de satisfacción
    satisfaccion = serializers.DictField(
        child=serializers.FloatField()
    )
    
    # Tendencias
    tendencia_turnos = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    # Comparativa entre sucursales
    comparativa_sucursales = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )