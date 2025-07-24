from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction

from ..models import Turno, ColaTurnos
from ..serializers import TurnoSerializer, TransferirTurnoSerializer
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
                empleado_actual=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            )
        except Turno.DoesNotExist:
            return Response(
                {"detail": "Turno no encontrado o no está en atención."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            nuevo_servicio = serializer.validated_data['nuevo_servicio']
            
            # Transferir turno
            turno.servicio = nuevo_servicio
            turno.estado = Turno.EstadoTurno.EN_ESPERA
            turno.empleado_actual = None
            turno.fecha_inicio_atencion = None
            turno.save()
            
            # Actualizar cola
            ColaTurnos.objects.filter(turno=turno, activo=True).update(activo=False)
            
            # Calcular nueva posición en cola
            nueva_posicion = ColaTurnos.objects.filter(
                servicio=nuevo_servicio,
                activo=True
            ).count() + 1
            
            ColaTurnos.objects.create(
                turno=turno,
                servicio=nuevo_servicio,
                posicion_cola=nueva_posicion,
                tiempo_espera_estimado=nuevo_servicio.tiempo_estimado_atencion * nueva_posicion,
                activo=True
            )
            
            return Response(TurnoSerializer(turno).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)