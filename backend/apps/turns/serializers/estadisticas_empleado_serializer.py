from rest_framework import serializers

class EstadisticasEmpleadoSerializer(serializers.Serializer):
    """Serializador para las estadísticas de un empleado"""
    turnos_atendidos_hoy = serializers.IntegerField()
    turnos_atendidos_semana = serializers.IntegerField()
    turnos_atendidos_mes = serializers.IntegerField()
    tiempo_promedio_atencion = serializers.DurationField()
    calificacion_promedio = serializers.FloatField()
    turnos_transferidos = serializers.IntegerField()
    cantidad_calificaciones = serializers.IntegerField()
    distribucion_calificaciones = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Distribución de calificaciones (1-5 estrellas)"
    )