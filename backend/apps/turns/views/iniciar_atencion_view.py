from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Turno
from ..services.logic import GestorTurnos

class IniciarAtencionView(APIView):
    def post(self, request, *args, **kwargs):
        turno_id = request.data.get('turno_id')
        if not turno_id:
            return Response({'error': 'turno_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            gestor = GestorTurnos()
            turno = gestor.iniciar_atencion_turno(turno_id)
            return Response({
                'id': turno.id,
                'numero_turno': turno.numero_turno,
                'servicio_nombre': turno.servicio.nombre if turno.servicio else 'Servicio no disponible',
                'nombre_cliente': turno.nombre_cliente,
                'numero_cedula': turno.numero_cedula,
                'estado_display': 'En Atención',
                'fecha_creacion': turno.fecha_creacion,
                'ventanilla': turno.ventanilla,
                'posicion_cola': turno.posicion_cola,
                'tiempo_espera_estimado': turno.tiempo_espera_estimado
            }, status=status.HTTP_200_OK)
        except Turno.DoesNotExist:
            return Response({'error': 'Turno no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
