from rest_framework import generics, permissions, status, filters, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sucursal, Servicio, Configuracion
from .serializers import SucursalSerializer, ServicioSerializer, ConfiguracionSerializer
from apps.users.permisos import EsAdministrador


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


class ListarSucursalesView(generics.ListAPIView):
    """Vista para listar sucursales activas"""
    queryset = Sucursal.objects.filter(activa=True)
    serializer_class = SucursalSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'ciudad', 'departamento']
    ordering_fields = ['nombre', 'ciudad']
    ordering = ['nombre']
