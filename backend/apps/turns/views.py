from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction, models
from django.db.models import Q, Avg, F, Value as V
from django.db.models.functions import Concat
from rest_framework import serializers
import random
import string

from .models import Turno, CalificacionServicio, ColaTurnos, Notificacion
from .serializers import (
    TurnoSerializer, CrearTurnoSerializer, CalificacionServicioSerializer,
    TransferirTurnoSerializer, ColaTurnosSerializer, EstadisticasEmpleadoSerializer
)
from apps.users.permisos import EsEmpleado, EsAdministrador
from apps.users.models import Empleado, Usuario
from apps.core.models import Servicio, Sucursal
from .logic import GestorTurnos


class CrearTurnoView(APIView):
    """Vista para crear un nuevo turno"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = CrearTurnoSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                turno = GestorTurnos.crear_turno(
                    usuario=request.user if request.user.is_authenticated else None,
                    servicio=serializer.validated_data['servicio'],
                    sucursal=serializer.validated_data['sucursal'],
                    es_agendado=serializer.validated_data.get('es_agendado', False),
                    fecha_agendada=serializer.validated_data.get('fecha_agendada')
                )
                return Response(
                    TurnoSerializer(turno).data,
                    status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ListarTurnosUsuarioView(generics.ListAPIView):
    """Vista para listar los turnos del usuario autenticado"""
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['estado', 'servicio', 'sucursal', 'es_agendado']
    ordering_fields = ['fecha_creacion', 'fecha_agendada']
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        """Devuelve solo los turnos del usuario autenticado"""
        return Turno.objects.filter(usuario=self.request.user)


class DetalleTurnoUsuarioView(generics.RetrieveUpdateDestroyAPIView):
    """Vista para ver, actualizar o cancelar un turno específico del usuario"""
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Devuelve solo los turnos del usuario autenticado"""
        # Temporal: permitir ver turnos sin usuario para pruebas
        return Turno.objects.filter(Q(usuario=self.request.user) | Q(usuario__isnull=True))
    
    def perform_destroy(self, instance):
        """Cancela un turno en lugar de eliminarlo físicamente"""
        # Verificar si el turno puede ser cancelado
        estados_no_cancelables = ['atendido', 'cancelado', 'no_asistio']
        
        if instance.estado in estados_no_cancelables:
            raise serializers.ValidationError({
                'estado': f'No se puede cancelar un turno en estado: {instance.get_estado_display()}'
            })
        
        # Actualizar el estado a cancelado
        instance.estado = 'cancelado'
        instance.save()
        
        # Actualizar la cola de turnos
        try:
            cola_turno = ColaTurnos.objects.get(turno=instance, activo=True)
            cola_turno.activo = False
            cola_turno.save()
            
            # Reordenar la cola
            colas_posteriores = ColaTurnos.objects.filter(
                servicio=instance.servicio,
                posicion_cola__gt=cola_turno.posicion_cola,
                activo=True
            ).order_by('posicion_cola')
            
            for cola in colas_posteriores:
                cola.posicion_cola -= 1
                cola.save()
        except ColaTurnos.DoesNotExist:
            pass  # El turno no estaba en la cola activa


class CrearCalificacionView(generics.CreateAPIView):
    """Vista para crear una calificación de servicio"""
    serializer_class = CalificacionServicioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Asigna el usuario autenticado a la calificación"""
        serializer.save(
            usuario=self.request.user,
            fecha_calificacion=timezone.now()
        )


class ListarCalificacionesUsuarioView(generics.ListAPIView):
    """Vista para listar las calificaciones realizadas por el usuario autenticado"""
    serializer_class = CalificacionServicioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['turno', 'servicio', 'empleado', 'calificacion']
    ordering_fields = ['fecha_calificacion', 'calificacion']
    ordering = ['-fecha_calificacion']
    
    def get_queryset(self):
        """Devuelve solo las calificaciones del usuario autenticado"""
        return CalificacionServicio.objects.filter(usuario=self.request.user)


class DetalleCalificacionView(generics.RetrieveAPIView):
    """Vista para ver el detalle de una calificación específica"""
    serializer_class = CalificacionServicioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Devuelve solo las calificaciones del usuario autenticado"""
        return CalificacionServicio.objects.filter(usuario=self.request.user)


class ListarTurnosAgendadosView(generics.ListAPIView):
    """Vista para listar los turnos agendados (futuros) del usuario autenticado"""
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['servicio', 'sucursal']
    ordering_fields = ['fecha_agendada', 'fecha_creacion']
    ordering = ['fecha_agendada']
    
    def get_queryset(self):
        """Devuelve solo los turnos agendados futuros del usuario autenticado"""
        # Obtener la fecha y hora actual
        ahora = timezone.now()
        
        # Filtrar turnos agendados con fecha futura
        queryset = Turno.objects.filter(
            usuario=self.request.user,
            es_agendado=True,
            fecha_agendada__gte=ahora
        )
        
        # Filtro adicional por rango de fechas si se proporciona
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            try:
                fecha_desde = timezone.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_agendada__date__gte=fecha_desde)
            except ValueError:
                pass
        
        if fecha_hasta:
            try:
                fecha_hasta = timezone.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_agendada__date__lte=fecha_hasta)
            except ValueError:
                pass
        
        return queryset


class HistorialTurnosView(generics.ListAPIView):
    """Vista para listar el historial de turnos completados del usuario autenticado"""
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['servicio', 'sucursal', 'estado', 'empleado']
    ordering_fields = ['fecha_creacion', 'fecha_atencion', 'fecha_finalizacion']
    ordering = ['-fecha_finalizacion', '-fecha_creacion']
    
    def get_queryset(self):
        """Devuelve los turnos históricos (finalizados, cancelados o ausentes) del usuario autenticado"""
        # Estados que consideramos como históricos
        estados_historicos = ['finalizado', 'cancelado', 'ausente']
        
        # Filtrar turnos que ya han sido completados o cancelados
        queryset = Turno.objects.filter(
            usuario=self.request.user,
            estado__in=estados_historicos
        )
        
        # Filtro adicional por rango de fechas si se proporciona
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            try:
                fecha_desde = timezone.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_creacion__date__gte=fecha_desde)
            except ValueError:
                pass
        
        if fecha_hasta:
            try:
                fecha_hasta = timezone.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_creacion__date__lte=fecha_hasta)
            except ValueError:
                pass
        
        return queryset


class SiguienteTurnoEmpleadoView(generics.GenericAPIView):
    """Permite a un empleado llamar al siguiente turno disponible"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TurnoSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            empleado = request.user.perfil_empleado

            # Verificar que el empleado esté activo y tenga servicios asignados
            if not empleado.servicios.filter(activo=True).exists():
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
                return Response(
                    {"detail": "Ya tiene un turno en atención. Debe finalizarlo primero."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener siguiente turno
            siguiente_turno = GestorTurnos.obtener_siguiente_turno(empleado)

            if not siguiente_turno:
                return Response(
                    {"detail": "No hay turnos en espera."},
                    status=status.HTTP_204_NO_CONTENT
                )

            # Asignar el turno al empleado
            turno_asignado = GestorTurnos.asignar_turno_empleado(siguiente_turno, empleado)
            
            # Enviar notificación al usuario si está registrado
            if turno_asignado.usuario:
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
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TurnoActualEmpleadoView(generics.GenericAPIView):
    """Vista para obtener el turno actual en atención de un empleado"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TurnoSerializer

    def get(self, request, *args, **kwargs):
        try:
            empleado = request.user.perfil_empleado
            turno_actual = Turno.objects.get(
                empleado_actual=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            )
            serializer = self.get_serializer(turno_actual)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Empleado.DoesNotExist:
            return Response(
                {"detail": "Perfil de empleado no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Turno.DoesNotExist:
            return Response(
                {"detail": "No tiene ningún turno en atención actualmente."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": "Error interno del servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompletarTurnoEmpleadoView(generics.GenericAPIView):
    """Permite a un empleado marcar un turno como completado"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TurnoSerializer

    @transaction.atomic
    def post(self, request, turno_id, *args, **kwargs):
        empleado = request.user.perfil_empleado
        try:
            turno = Turno.objects.get(
                id=turno_id,
                empleado_actual=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            )
        except Turno.DoesNotExist:
            return Response(
                {"detail": "Turno no encontrado o no está en atención."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Finalizar turno
        turno.estado = Turno.EstadoTurno.FINALIZADO
        turno.fecha_finalizacion = timezone.now()
        turno.save()

        serializer = self.get_serializer(turno)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransferirTurnoEmpleadoView(generics.GenericAPIView):
    """Permite a un empleado transferir un turno a otro servicio"""
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    serializer_class = TransferirTurnoSerializer

    @transaction.atomic
    def post(self, request, turno_id, *args, **kwargs):
        empleado = request.user.perfil_empleado
        try:
            turno = Turno.objects.get(
                id=turno_id,
                empleado_actual=empleado,
                estado=Turno.EstadoTurno.EN_ATENCION
            )
        except Turno.DoesNotExist:
            return Response(
                {"detail": "Turno no encontrado o no está en atención."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            nuevo_servicio = serializer.validated_data['nuevo_servicio']
            
            # Transferir turno
            turno.servicio = nuevo_servicio
            turno.estado = Turno.EstadoTurno.EN_ESPERA
            turno.empleado_actual = None
            turno.fecha_inicio_atencion = None
            turno.save()
            
            # Actualizar cola
            ColaTurnos.objects.filter(turno=turno, activo=True).update(activo=False)
            
            # Calcular nueva posición en cola
            nueva_posicion = ColaTurnos.objects.filter(
                servicio=nuevo_servicio,
                activo=True
            ).count() + 1
            
            ColaTurnos.objects.create(
                turno=turno,
                servicio=nuevo_servicio,
                posicion_cola=nueva_posicion,
                tiempo_espera_estimado=nuevo_servicio.tiempo_estimado_atencion * nueva_posicion,
                activo=True
            )
            
            return Response(TurnoSerializer(turno).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarColaTurnosView(generics.ListAPIView):
    """Vista para listar los turnos en cola"""
    serializer_class = ColaTurnosSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Devuelve solo los turnos activos en cola"""
        return ColaTurnos.objects.filter(
            activo=True
        ).select_related(
            'turno', 'servicio'
        ).order_by('servicio', 'posicion_cola')


class ListarColaTurnosEmpleadoView(generics.ListAPIView):
    """Vista para listar los turnos en cola para un empleado específico"""
    serializer_class = ColaTurnosSerializer
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    
    def get_queryset(self):
        """
        Devuelve solo los turnos activos en cola para los servicios 
        asignados al empleado en su sucursal
        """
        empleado = self.request.user.perfil_empleado
        servicios_empleado = empleado.servicios.all()
        
        return ColaTurnos.objects.filter(
            activo=True,
            servicio__in=servicios_empleado,
            turno__sucursal=empleado.sucursal
        ).select_related(
            'turno', 
            'servicio'
        ).order_by('servicio', 'posicion_cola')


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
            empleado_actual=empleado,
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
        calificaciones = CalificacionServicio.objects.filter(empleado_actual=empleado)
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

        # Turnos transferidos
        turnos_transferidos = Turno.objects.filter(
            empleado_actual=empleado,
            estado=Turno.EstadoTurno.EN_ESPERA,
            transferencias_count__gt=0
        ).count()

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
            return Response(
                {"detail": "Error interno del servidor"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReporteUsuariosView(generics.GenericAPIView):
    """Vista para generar reportes de usuarios"""
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    
    def get_reporte_usuarios(self):
        try:
            usuarios = Usuario.objects.annotate(
                nombre_completo=Concat('first_name', V(' '), 'last_name')
            ).values(
                'id',
                'username',
                'nombre_completo',
                'email',
                'cedula',
                'telefono',
                'ultimo_acceso',
                'date_joined'
            )
            
            return {
                'usuarios': list(usuarios),
                'total': usuarios.count()
            }
        except Exception as e:
            raise Exception(f"Error al generar reporte de usuarios: {str(e)}")