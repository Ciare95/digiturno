from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Turno
from ..services.logic import GestorTurnos
from ..serializers import TurnoSerializer

import logging
logger = logging.getLogger(__name__)

class FinalizarAtencionView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"FinalizarAtencionView request data: {request.data}")
        turno_id = request.data.get('turno_id')
        if not turno_id:
            logger.error("turno_id is missing in request")
            return Response({'error': 'turno_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            turno = Turno.objects.get(id=turno_id)
            logger.info(f"Current turno state before finalizing: {turno.estado}")
            
            gestor = GestorTurnos()
            gestor.finalizar_atencion_turno(turno_id)

            turno_actualizado = Turno.objects.get(id=turno_id)
            serializer = TurnoSerializer(turno_actualizado)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Turno.DoesNotExist:
            logger.error(f"Turno not found with id: {turno_id}")
            return Response({'error': 'Turno no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error finalizing turno: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
