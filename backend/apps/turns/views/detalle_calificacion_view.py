from rest_framework import generics, permissions

from ..models import CalificacionServicio
from ..serializers import CalificacionServicioSerializer

class DetalleCalificacionView(generics.RetrieveAPIView):
    """Vista para ver el detalle de una calificación específica"""
    serializer_class = CalificacionServicioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Devuelve solo las calificaciones del usuario autenticado"""
        return CalificacionServicio.objects.filter(usuario=self.request.user)