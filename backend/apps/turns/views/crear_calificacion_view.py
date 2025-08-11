import logging
from rest_framework import generics, permissions, status
from django.utils import timezone
from rest_framework.response import Response
from ..models import Turno
from ..serializers import CalificacionServicioSerializer

logger = logging.getLogger(__name__)

class CrearCalificacionView(generics.CreateAPIView):
    """Vista para crear una calificación de servicio"""
    serializer_class = CalificacionServicioSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Incoming rating request data: {request.data}")
        turno_id = request.data.get('turno_id')
        if not turno_id:
            logger.error("Missing turno_id in request")
            return Response(
                {'detail': 'Se requiere el ID del turno.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            turno = Turno.objects.get(id=turno_id)
            logger.info(f"Found turno: {turno.id}, estado: {turno.estado}")
        except Turno.DoesNotExist as e:
            logger.error(f"Turno not found: {turno_id}, error: {str(e)}")
            return Response(
                {'detail': 'Turno no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error fetching turno: {str(e)}")
            return Response(
                {'detail': 'Error interno al buscar turno.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Preparar datos para el serializador
        data = {
            'turno': turno.id,
            'calificacion': request.data.get('calificacion'),
            'comentario': request.data.get('comentario', ''),
            'servicio': turno.servicio.id if turno.servicio else None,
            'empleado': turno.empleado.usuario.id if turno.empleado else None,
            'sucursal': turno.sucursal.id if turno.sucursal else None,
        }
        logger.info(f"Prepared serializer data: {data}")

        # Validar que el turno esté finalizado
        if turno.estado != 'finalizado':
            logger.error(f"Turno {turno.id} not in finalizado state: {turno.estado}")
            return Response(
                {'detail': 'Solo se pueden calificar turnos finalizados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info(f"Rating created successfully for turno {turno.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error creating rating: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'Error interno al crear calificación.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
    def perform_create(self, serializer):
        """Completa los datos de la calificación"""
        serializer.save(
            usuario=self.request.user if self.request.user.is_authenticated else None,
            fecha_calificacion=timezone.now()
        )
