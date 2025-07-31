from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Turno
from ..services.logic import GestorTurnos

class FinalizarAtencionView(APIView):
    def post(self, request, *args, **kwargs):
        turno_id = request.data.get('turno_id')
        if not turno_id:
            return Response({'error': 'turno_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            gestor = GestorTurnos()
            gestor.finalizar_atencion_turno(turno_id)
            return Response({'message': 'Atención finalizada correctamente'}, status=status.HTTP_200_OK)
        except Turno.DoesNotExist:
            return Response({'error': 'Turno no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
