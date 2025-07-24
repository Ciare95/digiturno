from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.models import Servicio
from apps.core.serializers import ServicioSerializer

class ListarServiciosView(generics.ListAPIView):
    """Vista para listar servicios disponibles para usuarios"""
    queryset = Servicio.objects.filter(sucursal__activa=True, activo=True)
    serializer_class = ServicioSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sucursal', 'codigo_servicio']
    search_fields = ['nombre', 'codigo_servicio']
    ordering_fields = ['nombre', 'tiempo_estimado_atencion']
    ordering = ['nombre']
    
    def get_queryset(self):
        """Personaliza el queryset para filtrar por sucursal si se proporciona"""
        queryset = super().get_queryset()
        sucursal_id = self.request.query_params.get('sucursal_id')
        
        if sucursal_id:
            queryset = queryset.filter(sucursal_id=sucursal_id)
            
        return queryset