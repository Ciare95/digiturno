from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q, F, ExpressionWrapper, fields
from datetime import timedelta, datetime
from django.utils.dateparse import parse_date

from apps.turns.models import Turno, CalificacionServicio
from apps.users.models import Usuario, Empleado
from apps.core.models import Servicio, Sucursal
from apps.users.permisos import EsAdministrador
from .serializers import DashboardAdminSerializer, ReporteAvanzadoSerializer


class DashboardAdminView(generics.GenericAPIView):
    """Vista para el dashboard del administrador"""
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    serializer_class = DashboardAdminSerializer

    def get_estadisticas_generales(self):
        """Obtiene estadísticas generales del sistema"""
        return {
            'total_usuarios': Usuario.objects.filter(is_staff=False, is_superuser=False).count(),
            'total_empleados': Empleado.objects.count(),
            'total_servicios_activos': Servicio.objects.filter(activo=True).count(),
            'total_sucursales_activas': Sucursal.objects.filter(activa=True).count(),
        }

    def get_estadisticas_turnos(self):
        """Obtiene estadísticas de turnos"""
        hoy = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        turnos_base = Turno.objects.all()
        turnos_hoy = turnos_base.filter(fecha_creacion__gte=hoy)

        # Calcular tiempo promedio de espera
        turnos_finalizados = turnos_base.filter(
            estado='finalizado',
            fecha_inicio_atencion__isnull=False,
            fecha_creacion__isnull=False
        )
        if turnos_finalizados.exists():
            tiempo_espera = sum(
                (turno.fecha_inicio_atencion - turno.fecha_creacion 
                for turno in turnos_finalizados),
                timedelta()
            ) / turnos_finalizados.count()
        else:
            tiempo_espera = timedelta()

        return {
            'turnos_hoy': turnos_hoy.count(),
            'turnos_en_espera': turnos_base.filter(estado='en_espera').count(),
            'turnos_en_atencion': turnos_base.filter(estado='en_atencion').count(),
            'turnos_finalizados': turnos_base.filter(estado='finalizado').count(),
            'turnos_cancelados': turnos_base.filter(estado='cancelado').count(),
            'tiempo_espera_promedio': tiempo_espera,
        }

    def get_servicios_mas_demandados(self):
        """Obtiene los servicios más demandados"""
        servicios = Turno.objects.values('servicio__nombre')\
                   .annotate(total=Count('id'))\
                   .order_by('-total')[:5]
        
        return [
            {'nombre': s['servicio__nombre'], 'total': str(s['total'])}
            for s in servicios
        ]

    def get_estadisticas_calificaciones(self):
        """Obtiene estadísticas de calificaciones"""
        calificaciones = CalificacionServicio.objects.all()
        total = calificaciones.count()
        promedio = calificaciones.aggregate(Avg('calificacion'))['calificacion__avg'] or 0.0

        distribucion = {
            str(i): calificaciones.filter(calificacion=i).count()
            for i in range(1, 6)
        }

        return {
            'calificacion_promedio_general': round(promedio, 2),
            'total_calificaciones': total,
            'distribucion_calificaciones': distribucion
        }

    def get_rendimiento_sucursales(self):
        """Obtiene estadísticas de rendimiento por sucursal"""
        sucursales = Sucursal.objects.filter(activa=True)
        rendimiento = []

        for sucursal in sucursales:
            turnos_sucursal = Turno.objects.filter(sucursal=sucursal)
            calificaciones_sucursal = CalificacionServicio.objects.filter(
                turno__sucursal=sucursal
            )

            rendimiento.append({
                'sucursal': {
                    'id': sucursal.id,
                    'nombre': sucursal.nombre,
                    'turnos_totales': turnos_sucursal.count(),
                    'turnos_finalizados': turnos_sucursal.filter(
                        estado='finalizado'
                    ).count(),
                    'calificacion_promedio': calificaciones_sucursal.aggregate(
                        Avg('calificacion')
                    )['calificacion__avg'] or 0.0
                }
            })

        return rendimiento

    def get(self, request, *args, **kwargs):
        """Obtiene las estadísticas del dashboard"""
        try:
            datos_dashboard = {
                **self.get_estadisticas_generales(),
                **self.get_estadisticas_turnos(),
                'servicios_mas_demandados': self.get_servicios_mas_demandados(),
                **self.get_estadisticas_calificaciones(),
                'rendimiento_sucursales': self.get_rendimiento_sucursales()
            }

            serializer = self.get_serializer(datos_dashboard)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": f"Error al obtener datos del dashboard: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReporteAvanzadoView(generics.GenericAPIView):
    """Vista para generar reportes avanzados para administradores"""
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    serializer_class = ReporteAvanzadoSerializer

    def get_queryset_turnos(self, fecha_inicio, fecha_fin):
        """Obtiene el queryset base de turnos filtrado por fechas"""
        return Turno.objects.filter(
            fecha_creacion__date__gte=fecha_inicio,
            fecha_creacion__date__lte=fecha_fin
        )

    def get_metricas_turnos(self, turnos, dias_totales):
        """Calcula métricas generales de turnos"""
        turnos_finalizados = turnos.filter(
            estado='finalizado',
            fecha_inicio_atencion__isnull=False,
            fecha_finalizacion__isnull=False
        )

        # Calcular tiempos promedio
        tiempo_espera = turnos_finalizados.annotate(
            tiempo_espera=F('fecha_inicio_atencion') - F('fecha_creacion')
        ).aggregate(promedio=Avg('tiempo_espera'))['promedio'] or timedelta()

        tiempo_atencion = turnos_finalizados.annotate(
            tiempo_atencion=F('fecha_finalizacion') - F('fecha_inicio_atencion')
        ).aggregate(promedio=Avg('tiempo_atencion'))['promedio'] or timedelta()

        return {
            'total_turnos': turnos.count(),
            'promedio_turnos_diario': round(turnos.count() / dias_totales, 2),
            'tiempo_espera_promedio': tiempo_espera,
            'tiempo_atencion_promedio': tiempo_atencion
        }

    def get_metricas_servicios(self, turnos):
        """Obtiene métricas detalladas por servicio"""
        return list(turnos.values('servicio__nombre').annotate(
            total_turnos=Count('id'),
            tiempo_promedio_atencion=Avg(
                ExpressionWrapper(
                    F('fecha_finalizacion') - F('fecha_inicio_atencion'),
                    output_field=fields.DurationField()
                )
            ),
            calificacion_promedio=Avg('calificacion_servicio__calificacion')
        ).order_by('-total_turnos'))

    def get_metricas_empleados(self, turnos):
        """Obtiene métricas detalladas por empleado"""
        return list(turnos.values(
            'empleado__usuario__username',
            'empleado__codigo_empleado'
        ).annotate(
            total_turnos=Count('id'),
            tiempo_promedio_atencion=Avg(
                ExpressionWrapper(
                    F('fecha_finalizacion') - F('fecha_inicio_atencion'),
                    output_field=fields.DurationField()
                )
            ),
            calificacion_promedio=Avg('calificacion_servicio__calificacion')
        ).filter(empleado__isnull=False).order_by('-total_turnos'))

    def get_metricas_satisfaccion(self, turnos):
        """Obtiene métricas detalladas de satisfacción"""
        calificaciones = CalificacionServicio.objects.filter(turno__in=turnos)
        
        return {
            'promedio_general': calificaciones.aggregate(
                Avg('calificacion')
            )['calificacion__avg'] or 0.0,
            'distribucion': {
                str(i): calificaciones.filter(calificacion=i).count()
                for i in range(1, 6)
            }
        }

    def get_tendencias_turnos(self, turnos, fecha_inicio, fecha_fin):
        """Obtiene tendencias de turnos por día"""
        return list(turnos.annotate(
            fecha=F('fecha_creacion__date')
        ).values('fecha').annotate(
            total=Count('id')
        ).order_by('fecha'))

    def get_comparativa_sucursales(self, turnos):
        """Obtiene comparativa entre sucursales"""
        return list(turnos.values('sucursal__nombre').annotate(
            total_turnos=Count('id'),
            tiempo_promedio_espera=Avg(
                ExpressionWrapper(
                    F('fecha_inicio_atencion') - F('fecha_creacion'),
                    output_field=fields.DurationField()
                )
            ),
            tiempo_promedio_atencion=Avg(
                ExpressionWrapper(
                    F('fecha_finalizacion') - F('fecha_inicio_atencion'),
                    output_field=fields.DurationField()
                )
            ),
            calificacion_promedio=Avg('calificacion_servicio__calificacion')
        ).filter(sucursal__isnull=False).order_by('-total_turnos'))

    def get(self, request, *args, **kwargs):
        """Genera el reporte avanzado basado en los parámetros recibidos"""
        # Obtener fechas del request, default último mes
        fecha_fin = parse_date(request.query_params.get('fecha_fin')) or timezone.now().date()
        fecha_inicio = parse_date(request.query_params.get('fecha_inicio')) or (fecha_fin - timedelta(days=30))
        
        # Validar fechas
        if fecha_inicio > fecha_fin:
            return Response(
                {'error': 'La fecha de inicio debe ser anterior a la fecha fin'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calcular días totales del periodo
        dias_totales = (fecha_fin - fecha_inicio).days + 1

        # Obtener turnos del periodo
        turnos = self.get_queryset_turnos(fecha_inicio, fecha_fin)

        # Generar reporte
        reporte = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            **self.get_metricas_turnos(turnos, dias_totales),
            'servicios': self.get_metricas_servicios(turnos),
            'empleados': self.get_metricas_empleados(turnos),
            'satisfaccion': self.get_metricas_satisfaccion(turnos),
            'tendencia_turnos': self.get_tendencias_turnos(turnos, fecha_inicio, fecha_fin),
            'comparativa_sucursales': self.get_comparativa_sucursales(turnos)
        }

        serializer = self.get_serializer(reporte)
        return Response(serializer.data)