from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction, models

from ..models import Turno, ColaTurnos
from ..serializers import TurnoSerializer, TransferirTurnoSerializer
from apps.core.models.servicio import Servicio
from apps.users.permissions.es_empleado import EsEmpleado

class TransferirTurnoEmpleadoView(generics.GenericAPIView):
    """Permite a un empleado transferir un turno a otro servicio"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TransferirTurnoSerializer

    @transaction.atomic
    def post(self, request, turno_id, *args, **kwargs):
        empleado = request.user.perfil_empleado
        try:
            turno = Turno.objects.get(
                id=turno_id,
                empleado=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            )
        except Turno.DoesNotExist:
            return Response(
                {"detail": "Turno no encontrado o no está en atención."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            nuevo_servicio_id = serializer.validated_data['nuevo_servicio_id']
            nuevo_servicio = Servicio.objects.get(id=nuevo_servicio_id)
            
            # Transferir turno
            turno.servicio = nuevo_servicio
            turno.estado = Turno.EstadoTurno.EN_ESPERA
            turno.empleado = None
            turno.fecha_inicio_atencion = None
            turno.save()
            
            # Desactivar cualquier entrada existente en cola para este turno
            ColaTurnos.objects.filter(turno=turno).update(activo=False)
            
            # Mover todos los turnos existentes en la cola una posición hacia abajo
            ColaTurnos.objects.filter(
                turno__servicio=nuevo_servicio,
                activo=True
            ).update(posicion_cola=models.F('posicion_cola') + 1)
            
            # Colocar el turno transferido en la primera posición
            ColaTurnos.objects.update_or_create(
                turno=turno,
                defaults={
                    'posicion_cola': 1,
                    'tiempo_espera_estimado': nuevo_servicio.tiempo_estimado_atencion,
                    'activo': True
                }
            )
            
            # Recalcular tiempos de espera para todos los turnos en la cola
            turnos_en_cola = ColaTurnos.objects.filter(
                turno__servicio=nuevo_servicio,
                activo=True
            ).order_by('posicion_cola')
            
            for idx, cola_turno in enumerate(turnos_en_cola, start=1):
                cola_turno.tiempo_espera_estimado = nuevo_servicio.tiempo_estimado_atencion * idx
                cola_turno.save()
            
            return Response(TurnoSerializer(turno).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
