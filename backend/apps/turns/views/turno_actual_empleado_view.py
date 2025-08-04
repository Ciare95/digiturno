from rest_framework import generics, permissions, status
from rest_framework.response import Response

from ..models import Turno
from ..serializers import TurnoSerializer
from apps.users.permissions.es_empleado import EsEmpleado
from apps.users.models.empleado import Empleado

class TurnoActualEmpleadoView(generics.GenericAPIView):
    """Vista para obtener el turno actual en atención de un empleado"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TurnoSerializer

    def get(self, request, *args, **kwargs):
        try:
            empleado = request.user.perfil_empleado
            turno_actual = Turno.objects.get(
                empleado=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            )
            serializer = self.get_serializer(turno_actual)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Empleado.DoesNotExist:
            return Response(
                {"detail": "Perfil de empleado no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Turno.DoesNotExist:
            return Response(
                {"detail": "No tiene ningún turno en atención actualmente."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": "Error interno del servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
