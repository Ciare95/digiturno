from rest_framework import serializers
from apps.turns.models import Turno, CalificacionServicio
from apps.users.models import Usuario, Empleado
from apps.core.models import Servicio, Sucursal


class DashboardAdminSerializer(serializers.Serializer):
    total_usuarios = serializers.IntegerField()
    total_empleados = serializers.IntegerField()
    total_servicios_activos = serializers.IntegerField()
    total_sucursales_activas = serializers.IntegerField()
    
    turnos_hoy = serializers.IntegerField()
    turnos_en_espera = serializers.IntegerField()
    turnos_en_atencion = serializers.IntegerField()
    turnos_finalizados = serializers.IntegerField()
    turnos_cancelados = serializers.IntegerField()
    tiempo_espera_promedio = serializers.DurationField()
    
    servicios_mas_demandados = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    calificacion_promedio_general = serializers.FloatField()
    total_calificaciones = serializers.IntegerField()
    distribucion_calificaciones = serializers.DictField(
        child=serializers.IntegerField()
    )

    rendimiento_sucursales = serializers.ListField(
        child=serializers.DictField(
            child=serializers.DictField()
        )
    )


class ReporteAvanzadoSerializer(serializers.Serializer):
    fecha_inicio = serializers.DateField(required=False)
    fecha_fin = serializers.DateField(required=False)

    class Meta:
        fields = ['fecha_inicio', 'fecha_fin']
