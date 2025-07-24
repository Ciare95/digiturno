from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ..models import CalificacionServicio
from ..serializers import CalificacionServicioSerializer

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