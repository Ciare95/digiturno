from rest_framework import generics, permissions
from rest_framework import serializers
from django.db.models import Q

from ..models import Turno, ColaTurnos
from ..serializers import TurnoSerializer

class DetalleTurnoUsuarioView(generics.RetrieveUpdateDestroyAPIView):
    """Vista para ver, actualizar o cancelar un turno específico del usuario"""
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Devuelve solo los turnos del usuario autenticado"""
        # Temporal: permitir ver turnos sin usuario para pruebas
        return Turno.objects.filter(Q(usuario=self.request.user) | Q(usuario__isnull=True))
    
    def perform_destroy(self, instance):
        """Cancela un turno en lugar de eliminarlo físicamente"""
        # Verificar si el turno puede ser cancelado
        estados_no_cancelables = ['finalizado', 'cancelado', 'ausente']
        
        if instance.estado in estados_no_cancelables:
            raise serializers.ValidationError({
                'estado': f'No se puede cancelar un turno en estado: {instance.get_estado_display()}'
            })
        
        # Verificar si el turno está en atención
        if instance.estado == 'en_atencion':
            raise serializers.ValidationError({
                'estado': 'No se puede cancelar un turno que está en atención'
            })
        
        # Actualizar el estado a cancelado
        instance.estado = 'cancelado'
        instance.save()
        
        # Actualizar la cola de turnos
        try:
            cola_turno = ColaTurnos.objects.get(turno=instance, activo=True)
            cola_turno.activo = False
            cola_turno.save()
            
            # Reordenar la cola
            colas_posteriores = ColaTurnos.objects.filter(
                servicio=instance.servicio,
                posicion_cola__gt=cola_turno.posicion_cola,
                activo=True
            ).order_by('posicion_cola')
            
            for cola in colas_posteriores:
                cola.posicion_cola -= 1
                cola.save()
        except ColaTurnos.DoesNotExist:
            pass  # El turno no estaba en la cola activa