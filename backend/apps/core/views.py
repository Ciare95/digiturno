from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sucursal, Servicio, Configuracion
from .serializers import SucursalSerializer, ServicioSerializer, ConfiguracionSerializer


class ListarServiciosView(generics.ListAPIView):
    """Vista para listar servicios disponibles"""
    queryset = Servicio.objects.filter(sucursal__activa=True)
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
