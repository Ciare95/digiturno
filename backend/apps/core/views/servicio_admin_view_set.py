from rest_framework import permissions, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.models import Servicio
from apps.core.serializers import ServicioSerializer
from apps.users.permissions.es_administrador import EsAdministrador

class ServicioAdminViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de servicios por el administrador"""
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sucursal', 'codigo_servicio', 'activo']
    search_fields = ['nombre', 'codigo_servicio']
    ordering_fields = ['nombre', 'tiempo_estimado_atencion', 'sucursal__nombre']
    ordering = ['sucursal__nombre', 'nombre']

    def get_queryset(self):
        """Personaliza el queryset para filtrar por sucursal si se proporciona"""
        queryset = super().get_queryset()
        sucursal_id = self.request.query_params.get('sucursal_id')
        
        if sucursal_id:
            queryset = queryset.filter(sucursal_id=sucursal_id)
            
        return queryset
    
    def perform_create(self, serializer):
        """Guarda el servicio y registra quien lo creó"""
        serializer.save()
    
    def perform_update(self, serializer):
        """Guarda los cambios del servicio"""
        serializer.save()