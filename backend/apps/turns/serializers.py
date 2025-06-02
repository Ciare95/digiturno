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
    
    class Meta:
        model = CalificacionServicio
        fields = [
            'id', 'turno', 'turno_numero', 'usuario', 'usuario_nombre',
            'empleado', 'empleado_nombre', 'servicio', 'servicio_nombre',
            'calificacion', 'comentario', 'aspectos_evaluados', 'fecha_calificacion'
        ]
        read_only_fields = ['fecha_calificacion']