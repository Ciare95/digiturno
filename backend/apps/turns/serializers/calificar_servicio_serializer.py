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
            'servicio', 'servicio_nombre', 'calificacion', 'comentario',
            'aspectos_evaluados', 'fecha_calificacion', 'fecha_calificacion_formateada'
        ]
        read_only_fields = ['usuario', 'fecha_calificacion', 'empleado_nombre', 'usuario_nombre', 'turno_numero', 'servicio_nombre', 'fecha_calificacion_formateada']
    
    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('La calificación debe estar entre 1 y 5')
        return value
    
    def validate_turno(self, value):
        if value.estado != 'finalizado':
            raise serializers.ValidationError('Solo se pueden calificar turnos finalizados.')
        # Verificar que el turno no haya sido calificado previamente por este usuario
        if CalificacionServicio.objects.filter(turno=value, usuario=self.context['request'].user).exists():
            raise serializers.ValidationError('Este turno ya ha sido calificado por usted.')
        return value
    
    def validate(self, attrs):
        turno = attrs.get('turno')
        servicio = attrs.get('servicio')
        empleado = attrs.get('empleado')

        # Validar que el usuario que califica sea el mismo del turno (si el turno tiene usuario)
        if turno.usuario and self.context.get('request', {}).user and self.context['request'].user != turno.usuario:
            raise serializers.ValidationError('No puede calificar un turno que no le pertenece.')

        if turno and servicio and turno.servicio.id != servicio.id:
            raise serializers.ValidationError({'servicio': 'El servicio no corresponde al turno indicado.'})
        
        # El empleado en la calificación debe ser el mismo que atendió el turno.
        if turno and empleado and turno.empleado and turno.empleado.usuario.id != empleado.usuario.id:
            raise serializers.ValidationError({'empleado': 'El empleado no corresponde al que atendió el turno.'})
        elif turno and not empleado and turno.empleado:
             # Si el turno tiene un empleado pero no se provee en la calificación
             attrs['empleado'] = turno.empleado
        elif turno and empleado and not turno.empleado:
            # Esto no debería pasar si el turno está finalizado y fue atendido por alguien
            pass


        return attrs