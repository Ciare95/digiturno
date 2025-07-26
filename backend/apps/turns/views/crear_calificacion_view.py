from rest_framework import generics, permissions
from django.utils import timezone
from ..serializers import CalificacionServicioSerializer

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
