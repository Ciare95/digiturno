from django.db.models import Count, Avg, F, Q, ExpressionWrapper, fields
from django.db.models.functions import TruncDate, ExtractHour
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.turns.models import Turno
from apps.core.permissions import EsAdministrador
from .serializers import ReporteAvanzadoSerializer

class ReporteAvanzadoView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    serializer_class = ReporteAvanzadoSerializer

    def get_queryset_turnos(self, fecha_inicio, fecha_fin):
        queryset = Turno.objects.filter(
            fecha_creacion__gte=fecha_inicio,
            fecha_creacion__lte=fecha_fin
        ).select_related(
            'servicio', 
            'sucursal', 
            'empleado',
            'usuario'
        )
        return queryset

    def get_metricas_turnos(self, turnos, dias_totales):
        total_turnos = turnos.count()
        turnos_completados = turnos.filter(estado=Turno.EstadoTurno.FINALIZADO).count()
        turnos_cancelados = turnos.filter(estado=Turno.EstadoTurno.CANCELADO).count()
        
        tiempo_espera_avg = turnos.filter(
            fecha_llamado__isnull=False
        ).aggregate(
            tiempo_espera=Avg(
                ExpressionWrapper(
                    F('fecha_llamado') - F('fecha_creacion'),
                    output_field=fields.DurationField()
                )
            )
        )['tiempo_espera']

        tiempo_atencion_avg = turnos.filter(
            fecha_finalizacion__isnull=False
        ).aggregate(
            tiempo_atencion=Avg(
                ExpressionWrapper(
                    F('fecha_finalizacion') - F('fecha_inicio_atencion'),
                    output_field=fields.DurationField()
                )
            )
        )['tiempo_atencion']

        return {
            'total_turnos': total_turnos,
            'promedio_diario': round(total_turnos / dias_totales, 2),
            'turnos_completados': turnos_completados,
            'turnos_cancelados': turnos_cancelados,
            'tasa_completion': round((turnos_completados / total_turnos * 100), 2) if total_turnos > 0 else 0,
            'tiempo_espera_promedio': str(tiempo_espera_avg) if tiempo_espera_avg else "0:00:00",
            'tiempo_atencion_promedio': str(tiempo_atencion_avg) if tiempo_atencion_avg else "0:00:00"
        }

    def get_metricas_servicios(self, turnos):
        metricas_servicios = turnos.values(
            'servicio__nombre'
        ).annotate(
            total_turnos=Count('id'),
            tiempo_promedio_atencion=Avg(
                ExpressionWrapper(
                    F('fecha_finalizacion') - F('fecha_inicio_atencion'),
                    output_field=fields.DurationField()
                )
            )
        ).order_by('-total_turnos')

        return [{
            'servicio': metrica['servicio__nombre'],
            'total_turnos': metrica['total_turnos'],
            'tiempo_promedio_atencion': str(metrica['tiempo_promedio_atencion']) if metrica['tiempo_promedio_atencion'] else "0:00:00"
        } for metrica in metricas_servicios]

    def get_metricas_empleados(self, turnos):
        metricas_empleados = turnos.values(
            'empleado__usuario__nombre',
            'empleado__codigo_empleado'
        ).annotate(
            turnos_atendidos=Count('id', filter=Q(estado=Turno.EstadoTurno.FINALIZADO)),
            tiempo_promedio_atencion=Avg(
                ExpressionWrapper(
                    F('fecha_finalizacion') - F('fecha_inicio_atencion'),
                    output_field=fields.DurationField()
                )
            )
        ).order_by('-turnos_atendidos')

        return [{
            'empleado': metrica['empleado__usuario__nombre'],
            'codigo': metrica['empleado__codigo_empleado'],
            'turnos_atendidos': metrica['turnos_atendidos'],
            'tiempo_promedio_atencion': str(metrica['tiempo_promedio_atencion']) if metrica['tiempo_promedio_atencion'] else "0:00:00"
        } for metrica in metricas_empleados]

    def get_metricas_satisfaccion(self, turnos):
        calificaciones = turnos.filter(
            calificacion__isnull=False
        ).aggregate(
            promedio=Avg('calificacion__puntuacion'),
            total_calificaciones=Count('calificacion')
        )

        return {
            'promedio_satisfaccion': round(calificaciones['promedio'], 2) if calificaciones['promedio'] else 0,
            'total_calificaciones': calificaciones['total_calificaciones'],
            'tasa_respuesta': round(
                (calificaciones['total_calificaciones'] / turnos.filter(
                    estado=Turno.EstadoTurno.FINALIZADO
                ).count() * 100), 
                2
            ) if turnos.exists() else 0
        }

    def get_tendencias_turnos(self, turnos, fecha_inicio, fecha_fin):
        turnos_por_dia = turnos.annotate(
            fecha=TruncDate('fecha_creacion')
        ).values('fecha').annotate(
            total=Count('id')
        ).order_by('fecha')

        turnos_por_hora = turnos.annotate(
            hora=ExtractHour('fecha_creacion')
        ).values('hora').annotate(
            total=Count('id')
        ).order_by('hora')

        return {
            'por_dia': [{
                'fecha': tendencia['fecha'],
                'total': tendencia['total']
            } for tendencia in turnos_por_dia],
            'por_hora': [{
                'hora': tendencia['hora'],
                'total': tendencia['total']
            } for tendencia in turnos_por_hora]
        }

    def get_comparativa_sucursales(self, turnos):
        return turnos.values(
            'sucursal__nombre'
        ).annotate(
            total_turnos=Count('id'),
            turnos_completados=Count('id', filter=Q(estado=Turno.EstadoTurno.FINALIZADO)),
            tiempo_promedio_espera=Avg(
                ExpressionWrapper(
                    F('fecha_llamado') - F('fecha_creacion'),
                    output_field=fields.DurationField()
                )
            ),
            satisfaccion_promedio=Avg('calificacion__puntuacion')
        ).order_by('-total_turnos')

    def get(self, request, *args, **kwargs):
        try:
            fecha_fin = timezone.now()
            fecha_inicio = fecha_fin - timedelta(days=30)

            if 'fecha_inicio' in request.query_params:
                fecha_inicio = timezone.datetime.strptime(
                    request.query_params['fecha_inicio'],
                    '%Y-%m-%d'
                )

            if 'fecha_fin' in request.query_params:
                fecha_fin = timezone.datetime.strptime(
                    request.query_params['fecha_fin'],
                    '%Y-%m-%d'
                )

            dias_totales = (fecha_fin - fecha_inicio).days or 1
            turnos = self.get_queryset_turnos(fecha_inicio, fecha_fin)

            reporte = {
                'periodo': {
                    'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
                    'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
                    'dias_totales': dias_totales
                },
                'metricas_generales': self.get_metricas_turnos(turnos, dias_totales),
                'metricas_servicios': self.get_metricas_servicios(turnos),
                'metricas_empleados': self.get_metricas_empleados(turnos),
                'satisfaccion': self.get_metricas_satisfaccion(turnos),
                'tendencias': self.get_tendencias_turnos(turnos, fecha_inicio, fecha_fin),
                'comparativa_sucursales': self.get_comparativa_sucursales(turnos)
            }

            return Response(reporte)

        except ValueError as e:
            return Response(
                {"error": f"Error en el formato de fecha. Use YYYY-MM-DD. Detalle: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Error al generar el reporte: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
