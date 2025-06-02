from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction
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
        print(f"Usuario autenticado: {self.request.user}")  # Depuración
        print(f"Token: {self.request.headers.get('Authorization')}")  # Depuración
        return Turno.objects.filter(usuario=self.request.user)