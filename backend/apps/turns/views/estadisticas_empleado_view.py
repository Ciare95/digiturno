from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from django.db.models import Q
import logging

from ..models import Turno, CalificacionServicio
from ..serializers import EstadisticasEmpleadoSerializer

from apps.users.permissions.es_empleado import EsEmpleado
from apps.users.models.empleado import Empleado


class EstadisticasEmpleadoView(generics.GenericAPIView):
    """Vista para obtener las estadísticas de un empleado"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = EstadisticasEmpleadoSerializer

    def get_estadisticas_empleado(self, empleado):
        """Calcula las estadísticas para un empleado"""
        hoy = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_semana = hoy - timezone.timedelta(days=hoy.weekday())
        inicio_mes = hoy.replace(day=1)

        # Base query para turnos finalizados
        turnos_base = Turno.objects.filter(
            empleado=empleado,
            estado=Turno.EstadoTurno.FINALIZADO
        )

        # Turnos atendidos por período
        turnos_hoy = turnos_base.filter(fecha_finalizacion__gte=hoy).count()
        turnos_semana = turnos_base.filter(fecha_finalizacion__gte=inicio_semana).count()
        turnos_mes = turnos_base.filter(fecha_finalizacion__gte=inicio_mes).count()

        # Tiempo promedio de atención
        turnos_con_tiempo = turnos_base.exclude(
            Q(fecha_inicio_atencion__isnull=True) | Q(fecha_finalizacion__isnull=True)
        )
        if turnos_con_tiempo.exists():
            tiempo_total = sum(
                (turno.fecha_finalizacion - turno.fecha_inicio_atencion 
                for turno in turnos_con_tiempo),
                timezone.timedelta()
            )
            tiempo_promedio = tiempo_total / turnos_con_tiempo.count()
        else:
            tiempo_promedio = timezone.timedelta()

        # Calificaciones
        calificaciones = CalificacionServicio.objects.filter(empleado=empleado)
        cantidad_calificaciones = calificaciones.count()
        
        if cantidad_calificaciones > 0:
            calificacion_promedio = calificaciones.aggregate(
                promedio=models.Avg('calificacion')
            )['promedio']
            
            # Distribución de calificaciones
            distribucion = {
                str(i): calificaciones.filter(calificacion=i).count()
                for i in range(1, 6)
            }
        else:
            calificacion_promedio = 0.0
            distribucion = {str(i): 0 for i in range(1, 6)}

        # Turnos transferidos - obtener de las estadísticas del empleado o calcular de otra manera
        # Como no hay un campo directo para contar transferencias, usaremos las estadísticas guardadas
        from apps.turns.models import EstadisticaEmpleado
        estadisticas_empleado = EstadisticaEmpleado.objects.filter(empleado=empleado)
        turnos_transferidos = sum(est.turnos_transferidos for est in estadisticas_empleado)

        return {
            'turnos_atendidos_hoy': turnos_hoy,
            'turnos_atendidos_semana': turnos_semana,
            'turnos_atendidos_mes': turnos_mes,
            'tiempo_promedio_atencion': tiempo_promedio,
            'calificacion_promedio': round(calificacion_promedio, 2),
            'turnos_transferidos': turnos_transferidos,
            'cantidad_calificaciones': cantidad_calificaciones,
            'distribucion_calificaciones': distribucion
        }

    def get(self, request, *args, **kwargs):
        """Obtiene las estadísticas del empleado"""
        try:
            empleado = request.user.perfil_empleado
            estadisticas = self.get_estadisticas_empleado(empleado)
            serializer = self.get_serializer(estadisticas)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Empleado.DoesNotExist:
            return Response(
                {"detail": "Perfil de empleado no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logging.exception("Error interno en EstadisticasEmpleadoView:")
            return Response(
                {"detail": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )