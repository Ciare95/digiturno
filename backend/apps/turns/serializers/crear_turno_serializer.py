from rest_framework import serializers
from ..models import Turno
from django.utils import timezone

class CrearTurnoSerializer(serializers.ModelSerializer):
    numero_cedula = serializers.CharField(required=True)
    nombre_cliente = serializers.CharField(required=True)

    class Meta:
        model = Turno
        fields = ['servicio', 'sucursal', 'nombre_cliente', 'numero_cedula']

    def validate(self, attrs):
        servicio = attrs.get('servicio')
        sucursal = attrs.get('sucursal')
        numero_cedula = attrs.get('numero_cedula')
        es_agendado = attrs.get('es_agendado', False)
        fecha_agendada = attrs.get('fecha_agendada')
        request = self.context.get('request')
        usuario = request.user if request and hasattr(request, 'user') and request.user.is_authenticated else None
        
        # Validar que no exista un turno activo con el mismo número de cédula
        if numero_cedula:
            turnos_activos = Turno.objects.filter(
                numero_cedula=numero_cedula,
                estado__in=[
                    Turno.EstadoTurno.EN_ESPERA,
                    Turno.EstadoTurno.LLAMADO,
                    Turno.EstadoTurno.EN_ATENCION
                ]
            )
            
            if turnos_activos.exists():
                raise serializers.ValidationError({
                    'numero_cedula': f'Ya existe un turno activo con el número de cédula {numero_cedula}. Debe esperar a que finalice o sea cancelado.'
                })
        
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