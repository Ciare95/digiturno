from rest_framework import serializers
from .models import Turno, CalificacionServicio
from apps.users.serializers import UsuarioSerializer
from apps.core.serializers import ServicioSerializer, SucursalSerializer


class TurnoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Turno"""
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)
    empleado_nombre = serializers.CharField(source='empleado.usuario.get_full_name', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Turno
        fields = [
            'id', 'numero_turno', 'usuario', 'usuario_nombre', 'servicio', 
            'servicio_nombre', 'sucursal', 'sucursal_nombre', 'empleado',
            'empleado_nombre', 'estado', 'estado_display', 'prioridad',
            'fecha_creacion', 'fecha_llamado', 'fecha_inicio_atencion',
            'fecha_finalizacion', 'tiempo_espera_estimado', 'es_agendado',
            'fecha_agendada', 'observaciones'
        ]
        read_only_fields = ['numero_turno', 'fecha_creacion', 'fecha_llamado', 
                          'fecha_inicio_atencion', 'fecha_finalizacion']


class CrearTurnoSerializer(serializers.ModelSerializer):
    """Serializador para crear un nuevo turno"""
    
    class Meta:
        model = Turno
        fields = ['servicio', 'sucursal', 'prioridad', 'es_agendado', 'fecha_agendada', 'observaciones']
    
    def validate(self, attrs):
        # Validar que el servicio pertenezca a la sucursal seleccionada
        servicio = attrs.get('servicio')
        sucursal = attrs.get('sucursal')
        
        if servicio and sucursal and servicio.sucursal.id != sucursal.id:
            raise serializers.ValidationError({
                'servicio': 'El servicio seleccionado no pertenece a la sucursal indicada.'
            })
        
        # Validar que si es agendado, tenga fecha agendada
        es_agendado = attrs.get('es_agendado')
        fecha_agendada = attrs.get('fecha_agendada')
        
        if es_agendado and not fecha_agendada:
            raise serializers.ValidationError({
                'fecha_agendada': 'Debe proporcionar una fecha para el turno agendado.'
            })
        
        return attrs


class CalificacionServicioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo CalificacionServicio"""
    turno_numero = serializers.CharField(source='turno.numero_turno', read_only=True)
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    empleado_nombre = serializers.CharField(source='empleado.usuario.get_full_name', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    fecha_calificacion_formateada = serializers.DateTimeField(source='fecha_calificacion', format='%d/%m/%Y %H:%M', read_only=True)
    
    class Meta:
        model = CalificacionServicio
        fields = [
            'id', 'turno', 'turno_numero', 'usuario', 'usuario_nombre', 'empleado', 'empleado_nombre',
            'servicio', 'servicio_nombre', 'calificacion', 'comentario',
            'aspectos_evaluados', 'fecha_calificacion', 'fecha_calificacion_formateada'
        ]
        read_only_fields = ['usuario', 'fecha_calificacion']
    
    def validate_calificacion(self, value):
        """Validar que la calificación esté entre 1 y 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError('La calificación debe estar entre 1 y 5')
        return value
    
    def validate_turno(self, value):
        """Validar que el turno esté finalizado"""
        if value.estado != 'finalizado':
            raise serializers.ValidationError('Solo se pueden calificar turnos finalizados')
        return value
    
    def validate(self, attrs):
        """Validaciones adicionales"""
        # Verificar que el turno corresponda al servicio y empleado indicados
        turno = attrs.get('turno')
        servicio = attrs.get('servicio')
        empleado = attrs.get('empleado')
        
        if turno and servicio and turno.servicio.id != servicio.id:
            raise serializers.ValidationError({
                'servicio': 'El servicio no corresponde al turno indicado'
            })
        
        if turno and empleado and turno.empleado and turno.empleado.id != empleado.id:
            raise serializers.ValidationError({
                'empleado': 'El empleado no corresponde al turno indicado'
            })
        
        return attrs