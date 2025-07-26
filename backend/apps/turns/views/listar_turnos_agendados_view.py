from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from ..models import Turno
from ..serializers import TurnoSerializer

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