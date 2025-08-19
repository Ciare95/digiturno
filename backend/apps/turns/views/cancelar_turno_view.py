from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import Turno
from ..services import GestorTurnos

class CancelarTurnoView(APIView):
    """
    Vista para que un usuario pueda cancelar un turno.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, turno_id):
        try:
            turno = GestorTurnos.cancelar_turno(turno_id)
            return Response(
                {'message': f'Turno {turno.numero_turno} ha sido cancelado exitosamente.'},
                status=status.HTTP_200_OK
            )
        except Turno.DoesNotExist:
            return Response(
                {'error': 'El turno no existe.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
