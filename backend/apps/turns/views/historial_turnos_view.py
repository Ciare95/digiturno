from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from ..models import Turno
from ..serializers import TurnoSerializer

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
        
        # Filtrar turnos por cédula del usuario autenticado
        if not self.request.user.cedula:
            return Turno.objects.none()
            
        queryset = Turno.objects.filter(
            numero_cedula=self.request.user.cedula,
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
