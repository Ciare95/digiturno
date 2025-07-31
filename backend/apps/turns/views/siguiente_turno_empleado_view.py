import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction

from ..models import Turno, Notificacion
from ..serializers import TurnoSerializer
from apps.users.permissions.es_empleado import EsEmpleado
from ..services import GestorTurnos

logger = logging.getLogger(__name__)

class SiguienteTurnoEmpleadoView(generics.GenericAPIView):
    """Permite a un empleado llamar al siguiente turno disponible"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TurnoSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            logger.info(f"SiguienteTurnoEmpleadoView request data: {request.data}")
            empleado = request.user.perfil_empleado
            logger.info(f"Empleado: {empleado.id} - Ventanilla: {getattr(empleado, 'ventanilla_asignada', 'No asignada')}")

            # Verificar que el empleado esté activo y tenga servicios asignados
            if not empleado.servicios.filter(activo=True).exists():
                logger.error("Empleado no tiene servicios activos asignados")
                return Response(
                    {"detail": "No tiene servicios activos asignados."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verificar si ya tiene un turno en atención
            turno_actual = Turno.objects.filter(
                empleado=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            ).first()

            if turno_actual:
                logger.error(f"Empleado ya tiene turno en atencion: {turno_actual.id}")
                return Response(
                    {"detail": "Ya tiene un turno en atención. Debe finalizarlo primero."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener turno específico si se proporciona ID, sino obtener siguiente
            turno_id = request.data.get('turno_id')
            if turno_id:
                logger.info(f"Buscando turno específico: {turno_id}")
                siguiente_turno = Turno.objects.filter(
                    id=turno_id,
                    estado=Turno.EstadoTurno.EN_ESPERA
                ).first()
                
                if not siguiente_turno:
                    logger.error(f"Turno {turno_id} no disponible o no en espera")
                    return Response(
                        {"detail": "El turno especificado no está disponible."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                logger.info("Buscando siguiente turno disponible")
                siguiente_turno = GestorTurnos.obtener_siguiente_turno(empleado)
                if not siguiente_turno:
                    logger.info("No hay turnos en espera")
                    return Response(
                        {"detail": "No hay turnos en espera."},
                        status=status.HTTP_204_NO_CONTENT
                    )

            logger.info(f"Turno a asignar: {siguiente_turno.id} - Estado: {siguiente_turno.estado}")
            
            # Asignar el turno al empleado
            try:
                turno_asignado = GestorTurnos.asignar_turno_empleado(siguiente_turno, empleado)
                logger.info(f"Turno asignado exitosamente: {turno_asignado.id}")
            except Exception as e:
                logger.error(f"Error asignando turno: {str(e)}")
                raise
            
            # Enviar notificación al usuario si está registrado
            if turno_asignado.usuario:
                logger.info(f"Creando notificación para usuario {turno_asignado.usuario.id}")
                Notificacion.objects.create(
                    usuario=turno_asignado.usuario,
                    turno=turno_asignado,
                    tipo='llamado_turno',
                    titulo=f'Su turno {turno_asignado.numero_turno} ha sido llamado',
                    mensaje=f'Por favor diríjase a la ventanilla {empleado.ventanilla_asignada}'
                )

            serializer = self.get_serializer(turno_asignado)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error en SiguienteTurnoEmpleadoView: {str(e)}", exc_info=True)
            return Response(
                {"detail": "Error interno al procesar el turno. Por favor intente nuevamente."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
