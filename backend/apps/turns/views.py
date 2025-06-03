from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
import random
import string

from .models import Turno, CalificacionServicio, ColaTurnos
from .serializers import TurnoSerializer, CrearTurnoSerializer, CalificacionServicioSerializer
from apps.users.permisos import EsEmpleado, EsAdministrador


class CrearTurnoView(APIView):
    """Vista para crear un nuevo turno"""
    permission_classes = [permissions.AllowAny]
    
    def generar_numero_turno(self, servicio):
        """Genera un número de turno único"""
        # Prefijo basado en el código del servicio
        prefijo = servicio.codigo_servicio[:2].upper()
        
        # Obtener fecha actual para incluir en el número
        fecha = timezone.now().strftime('%y%m%d')
        
        # Contar cuántos turnos se han generado hoy para este servicio
        contador = Turno.objects.filter(
            servicio=servicio,
            fecha_creacion__date=timezone.now().date()
        ).count() + 1
        
        # Generar número de turno: PREFIJO-FECHA-CONTADOR
        numero_turno = f"{prefijo}-{fecha}-{contador:03d}"
        return numero_turno
    
    @transaction.atomic
    def post(self, request):
        """Crea un nuevo turno"""
        serializer = CrearTurnoSerializer(data=request.data)
        
        if serializer.is_valid():
            # Obtener datos validados
            servicio = serializer.validated_data['servicio']
            sucursal = serializer.validated_data['sucursal']
            
            # Generar número de turno
            numero_turno = self.generar_numero_turno(servicio)
            
            # Crear el turno
            turno = serializer.save(
                numero_turno=numero_turno,
                estado='en_espera',
                usuario=request.user if request.user.is_authenticated else None
            )
            
            # Calcular tiempo estimado de espera
            turnos_en_espera = Turno.objects.filter(
                servicio=servicio,
                sucursal=sucursal,
                estado='en_espera'
            ).count()
            
            tiempo_estimado = turnos_en_espera * servicio.tiempo_estimado_atencion
            turno.tiempo_espera_estimado = tiempo_estimado
            turno.save()
            
            # Crear entrada en la cola de turnos
            posicion_cola = ColaTurnos.objects.filter(
                servicio=servicio,
                activo=True
            ).count() + 1
            
            ColaTurnos.objects.create(
                turno=turno,
                servicio=servicio,
                posicion_cola=posicion_cola,
                tiempo_espera_estimado=tiempo_estimado
            )
            
            # Devolver datos del turno creado
            return Response(
                TurnoSerializer(turno).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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