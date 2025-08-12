from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import Turno
from ..serializers import TurnoSerializer

class PublicTurnoStatusView(APIView):
    """
    Vista pública para consultar el estado de un turno por su ID.
    No requiere autenticación.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, turno_id, *args, **kwargs):
        try:
            turno = Turno.objects.get(id=turno_id)
            serializer = TurnoSerializer(turno)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Turno.DoesNotExist:
            return Response({"detail": "Turno no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
