from rest_framework import serializers
from ..models import Turno
from django.utils import timezone

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
        request = self.context.get('request')
        usuario = request.user if request and hasattr(request, 'user') and request.user.is_authenticated else None
        
        if servicio and sucursal:
            # Validar que el servicio pertenezca a la sucursal
            if not sucursal.servicio_set.filter(id=servicio.id).exists():
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