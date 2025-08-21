from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum
from datetime import timedelta
import logging

from apps.users.models.empleado import Empleado
from apps.turns.models import Turno, CalificacionServicio, EstadisticaEmpleado
from apps.core.permissions.es_administrador import EsAdministrador

class EstadisticasEmpleadoAdminView(APIView):
    """Vista para obtener estadísticas de todos los empleados para administradores"""
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]

    def get(self, request):
        """Obtiene estadísticas de todos los empleados"""
        try:
            # Obtener todos los empleados (sin filtro de activo)
            empleados = Empleado.objects.all()
            
            estadisticas_empleados = []
            
            for empleado in empleados:
                estadisticas = self._get_estadisticas_empleado(empleado)
                estadisticas_empleados.append({
                    'empleado_id': empleado.usuario.id,
                    'empleado_nombre': f"{empleado.usuario.first_name} {empleado.usuario.last_name}",
                    'empleado_email': empleado.usuario.email,
                    **estadisticas
                })
            
            # Estadísticas generales
            estadisticas_generales = self._get_estadisticas_generales()
            
            return Response({
                'empleados': estadisticas_empleados,
                'estadisticas_generales': estadisticas_generales
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logging.exception("Error en EstadisticasEmpleadoAdminView:")
            return Response(
                {"detail": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_estadisticas_empleado(self, empleado):
        """Calcula las estadísticas para un empleado específico"""
        hoy = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        inicio_mes = hoy.replace(day=1)
        
        # Turnos atendidos por período
        turnos_base = Turno.objects.filter(
            empleado=empleado,
            estado=Turno.EstadoTurno.FINALIZADO
        )
        
        turnos_hoy = turnos_base.filter(fecha_finalizacion__gte=hoy).count()
        turnos_semana = turnos_base.filter(fecha_finalizacion__gte=inicio_semana).count()
        turnos_mes = turnos_base.filter(fecha_finalizacion__gte=inicio_mes).count()
        turnos_totales = turnos_base.count()
        
        # Tiempo promedio de atención
        turnos_con_tiempo = turnos_base.exclude(
            Q(fecha_inicio_atencion__isnull=True) | Q(fecha_finalizacion__isnull=True)
        )
        
        if turnos_con_tiempo.exists():
            tiempo_total = sum(
                (turno.fecha_finalizacion - turno.fecha_inicio_atencion 
                for turno in turnos_con_tiempo),
                timedelta()
            )
            tiempo_promedio_minutos = tiempo_total.total_seconds() / 60 / turnos_con_tiempo.count()
        else:
            tiempo_promedio_minutos = 0
        
        # Calificaciones
        calificaciones = CalificacionServicio.objects.filter(empleado=empleado)
        cantidad_calificaciones = calificaciones.count()
        
        if cantidad_calificaciones > 0:
            calificacion_promedio = calificaciones.aggregate(
                promedio=Avg('calificacion')
            )['promedio']
            
            # Distribución de calificaciones
            distribucion = {
                str(i): calificaciones.filter(calificacion=i).count()
                for i in range(1, 6)
            }
        else:
            calificacion_promedio = 0.0
            distribucion = {str(i): 0 for i in range(1, 6)}
        
        # Turnos transferidos
        estadisticas_empleado = EstadisticaEmpleado.objects.filter(empleado=empleado)
        turnos_transferidos = sum(est.turnos_transferidos for est in estadisticas_empleado)
        
        # Tiempo conectado (últimos 7 días)
        tiempo_conectado_minutos = sum(
            est.tiempo_conectado for est in estadisticas_empleado.filter(
                fecha__gte=hoy - timedelta(days=7)
            )
        )
        
        return {
            'turnos_atendidos_hoy': turnos_hoy,
            'turnos_atendidos_semana': turnos_semana,
            'turnos_atendidos_mes': turnos_mes,
            'turnos_atendidos_totales': turnos_totales,
            'tiempo_promedio_atencion_minutos': round(tiempo_promedio_minutos, 2),
            'calificacion_promedio': round(calificacion_promedio, 2),
            'turnos_transferidos': turnos_transferidos,
            'cantidad_calificaciones': cantidad_calificaciones,
            'tiempo_conectado_minutos': tiempo_conectado_minutos,
            'distribucion_calificaciones': distribucion
        }

    def _get_estadisticas_generales(self):
        """Calcula estadísticas generales de todos los empleados"""
        hoy = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Total de empleados activos
        total_empleados = Empleado.objects.count()
        
        # Turnos atendidos hoy
        turnos_hoy = Turno.objects.filter(
            estado=Turno.EstadoTurno.FINALIZADO,
            fecha_finalizacion__gte=hoy
        ).count()
        
        # Calificación promedio general
        calificacion_promedio = CalificacionServicio.objects.aggregate(
            promedio=Avg('calificacion')
        )['promedio'] or 0
        
        # Empleado con más turnos atendidos hoy
        empleado_mas_turnos_hoy = Turno.objects.filter(
            estado=Turno.EstadoTurno.FINALIZADO,
            fecha_finalizacion__gte=hoy
        ).values('empleado__usuario__first_name', 'empleado__usuario__last_name').annotate(
            total=Count('id')
        ).order_by('-total').first()
        
        # Empleado con mejor calificación
        empleado_mejor_calificacion = CalificacionServicio.objects.values(
            'empleado__usuario__first_name', 'empleado__usuario__last_name'
        ).annotate(
            promedio=Avg('calificacion')
        ).order_by('-promedio').first()
        
        return {
            'total_empleados': total_empleados,
            'turnos_atendidos_hoy': turnos_hoy,
            'calificacion_promedio_general': round(calificacion_promedio, 2),
            'empleado_mas_turnos_hoy': empleado_mas_turnos_hoy,
            'empleado_mejor_calificacion': empleado_mejor_calificacion
        }
