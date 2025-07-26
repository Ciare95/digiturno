from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from ..models import Turno
from ..serializers import TurnoSerializer
from apps.users.permissions.es_empleado import EsEmpleado

class CompletarTurnoEmpleadoView(generics.GenericAPIView):
    """Permite a un empleado marcar un turno como completado"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TurnoSerializer

    @transaction.atomic
    def post(self, request, turno_id, *args, **kwargs):
        empleado = request.user.perfil_empleado
        try:
            turno = Turno.objects.get(
                id=turno_id,
                empleado_actual=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            )
        except Turno.DoesNotExist:
            return Response(
                {"detail": "Turno no encontrado o no está en atención."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Finalizar turno
        turno.estado = Turno.EstadoTurno.FINALIZADO
        turno.fecha_finalizacion = timezone.now()
        turno.save()

        serializer = self.get_serializer(turno)
        return Response(serializer.data, status=status.HTTP_200_OK)