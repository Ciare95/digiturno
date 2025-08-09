from rest_framework import serializers
from ..models import CalificacionServicio

class CalificacionServicioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo CalificacionServicio"""
    turno_numero = serializers.CharField(source='turno.numero_turno', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    empleado_nombre = serializers.CharField(source='empleado.usuario.get_full_name', read_only=True, allow_null=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True, allow_null=True)
    fecha_calificacion_formateada = serializers.DateTimeField(source='fecha_calificacion', format='%d/%m/%Y %H:%M', read_only=True)
    
    class Meta:
        model = CalificacionServicio
        fields = [
            'id', 'turno', 'turno_numero', 'usuario', 'usuario_nombre', 'empleado', 'empleado_nombre',
            'servicio', 'servicio_nombre', 'sucursal', 'calificacion', 'comentario',
            'aspectos_evaluados', 'fecha_calificacion', 'fecha_calificacion_formateada'
        ]
        read_only_fields = ['usuario', 'fecha_calificacion', 'empleado_nombre', 'usuario_nombre', 'turno_numero', 'servicio_nombre', 'fecha_calificacion_formateada']
        extra_kwargs = {
            'sucursal': {'required': False}
        }
    
    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('La calificación debe estar entre 1 y 5')
        return value
    
    def validate_turno(self, value):
        if value.estado != 'finalizado':
            raise serializers.ValidationError('Solo se pueden calificar turnos finalizados.')
        
        # Verificar que el turno no haya sido calificado previamente
        if CalificacionServicio.objects.filter(turno=value).exists():
            raise serializers.ValidationError('Este turno ya ha sido calificado.')
        return value
    
    def create(self, validated_data):
        # Asignar el empleado del turno a la calificación si no se proporciona
        turno = validated_data.get('turno')
        if turno and turno.empleado and 'empleado' not in validated_data:
            validated_data['empleado'] = turno.empleado
        
        return super().create(validated_data)
