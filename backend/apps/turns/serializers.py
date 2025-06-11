from rest_framework import serializers
from .models import Turno, CalificacionServicio, ColaTurnos
from apps.users.serializers import UsuarioSerializer
from apps.core.serializers import ServicioSerializer, SucursalSerializer
from apps.core.models import Servicio 
from django.utils import timezone


class TurnoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Turno"""
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    empleado_nombre = serializers.CharField(source='empleado_actual.usuario.get_full_name', read_only=True, allow_null=True) # Permitir null si no hay empleado
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True, allow_null=True) # Permitir null si no hay usuario
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Turno
        fields = [
            'id', 'numero_turno', 'usuario', 'usuario_nombre', 'servicio', 
            'servicio_nombre', 'sucursal', 'sucursal_nombre', 'empleado_actual', # Cambiado de 'empleado' a 'empleado_actual'
            'empleado_nombre', 'estado', 'estado_display', 'prioridad',
            'fecha_creacion', 'fecha_atencion', 'fecha_finalizacion', # Cambiados nombres de fechas
            'tiempo_espera_estimado', 'es_agendado',
            'fecha_agendada', 'observaciones', 'ventanilla_atencion' # Añadido ventanilla_atencion
        ]
        read_only_fields = ['numero_turno', 'fecha_creacion', 'fecha_atencion', 
                          'fecha_finalizacion', 'empleado_nombre', 'usuario_nombre', 
                          'servicio_nombre', 'sucursal_nombre', 'estado_display']


class CrearTurnoSerializer(serializers.ModelSerializer):
    """Serializador para crear un nuevo turno"""
    
    class Meta:
        model = Turno
        fields = ['servicio', 'sucursal', 'es_agendado', 'fecha_agendada']
        
    def validate(self, attrs):
        servicio = attrs.get('servicio')
        sucursal = attrs.get('sucursal')
        es_agendado = attrs.get('es_agendado', False)
        fecha_agendada = attrs.get('fecha_agendada')
        usuario = self.context['request'].user if self.context['request'].user.is_authenticated else None
        
        if servicio and sucursal:
            # Validar que el servicio pertenezca a la sucursal
            if not sucursal.servicios.filter(id=servicio.id).exists():
                raise serializers.ValidationError({
                    'servicio': 'El servicio seleccionado no está disponible en esta sucursal.'
                })
        
        # Validar turno agendado
        if es_agendado:
            if not fecha_agendada:
                raise serializers.ValidationError({
                    'fecha_agendada': 'Debe proporcionar una fecha para el turno agendado.'
                })
            
            # Verificar que la fecha no sea pasada
            if fecha_agendada < timezone.now():
                raise serializers.ValidationError({
                    'fecha_agendada': 'No puede agendar turnos para fechas pasadas.'
                })

        return attrs


class CalificacionServicioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo CalificacionServicio"""
    turno_numero = serializers.CharField(source='turno.numero_turno', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    empleado_nombre = serializers.CharField(source='empleado_actual.usuario.get_full_name', read_only=True, allow_null=True) # Usar empleado_actual
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True, allow_null=True)
    fecha_calificacion_formateada = serializers.DateTimeField(source='fecha_calificacion', format='%d/%m/%Y %H:%M', read_only=True)
    
    class Meta:
        model = CalificacionServicio
        fields = [
            'id', 'turno', 'turno_numero', 'usuario', 'usuario_nombre', 'empleado_actual', 'empleado_nombre', # Usar empleado_actual
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
        empleado_actual = attrs.get('empleado_actual') # Usar empleado_actual

        # Validar que el usuario que califica sea el mismo del turno (si el turno tiene usuario)
        if turno.usuario and self.context['request'].user != turno.usuario:
            raise serializers.ValidationError('No puede calificar un turno que no le pertenece.')

        if turno and servicio and turno.servicio.id != servicio.id:
            raise serializers.ValidationError({'servicio': 'El servicio no corresponde al turno indicado.'})
        
        # El empleado_actual en la calificación debe ser el mismo que atendió el turno.
        if turno and empleado_actual and turno.empleado_actual and turno.empleado_actual.id != empleado_actual.id:
            raise serializers.ValidationError({'empleado_actual': 'El empleado no corresponde al que atendió el turno.'})
        elif turno and not empleado_actual and turno.empleado_actual:
             # Si el turno tiene un empleado_actual pero no se provee en la calificación
             attrs['empleado_actual'] = turno.empleado_actual
        elif turno and empleado_actual and not turno.empleado_actual:
            # Esto no debería pasar si el turno está finalizado y fue atendido por alguien
            pass


        return attrs

class TransferirTurnoSerializer(serializers.Serializer):
    """Serializador para la transferencia de turnos por un empleado."""
    nuevo_servicio_id = serializers.IntegerField(required=True, help_text="ID del nuevo servicio al que se transferirá el turno.")

    def validate_nuevo_servicio_id(self, value):
        """Verifica que el nuevo_servicio_id corresponda a un servicio válido y activo."""
        # Esta validación asume que el servicio existe y está activo.
        # La validación de que el servicio pertenece a la sucursal del empleado
        # se maneja directamente en la vista, ya que el serializer no tiene acceso directo al request.user aquí.
        if not Servicio.objects.filter(id=value, activo=True).exists():
            raise serializers.ValidationError("El servicio especificado no existe o no está activo.")
        return value

class ColaTurnosSerializer(serializers.ModelSerializer):
    """Serializador para la cola de turnos"""
    turno_numero = serializers.CharField(source='turno.numero_turno', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    estado_turno = serializers.CharField(source='turno.get_estado_display', read_only=True)
    
    class Meta:
        model = ColaTurnos
        fields = [
            'id', 'turno', 'turno_numero', 'servicio', 'servicio_nombre', 
            'posicion_cola', 'tiempo_espera_estimado', 'activo',
            'estado_turno'
        ]
        read_only_fields = ['turno_numero', 'servicio_nombre', 'estado_turno']

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