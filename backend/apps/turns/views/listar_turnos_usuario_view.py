from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Turno
from ..serializers import TurnoSerializer

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