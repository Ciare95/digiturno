from rest_framework import generics, permissions
from ..models import ColaTurnos
from ..serializers import ColaTurnosSerializer

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