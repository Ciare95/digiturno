from rest_framework import generics, permissions, status, filters, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from .models import Sucursal, Servicio, Configuracion
from .serializers import SucursalSerializer, ServicioSerializer, ConfiguracionSerializer
from apps.users.permisos import EsAdministrador


class SucursalAdminViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión completa de sucursales por el administrador"""
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activa', 'ciudad', 'departamento']
    search_fields = ['nombre', 'codigo_sucursal', 'ciudad', 'departamento']
    ordering_fields = ['nombre', 'ciudad', 'departamento']
    ordering = ['nombre']

    def perform_create(self, serializer):
        """Guarda la sucursal con configuración por defecto"""
        serializer.save(
            configuracion=serializer.validated_data.get('configuracion', {})
        )

    def perform_update(self, serializer):
        """Actualiza la sucursal manteniendo la configuración existente"""
        instance = self.get_object()
        config_actual = instance.configuracion
        nueva_config = serializer.validated_data.get('configuracion', {})
        config_actualizada = {**config_actual, **nueva_config}
        serializer.save(configuracion=config_actualizada)


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


class ConfiguracionAdminViewSet(viewsets.ModelViewSet):
    """ViewSet para la gestión de configuraciones del sistema"""
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'es_global', 'sucursal']
    search_fields = ['clave', 'descripcion']
    ordering_fields = ['categoria', 'clave', 'fecha_actualizacion']
    ordering = ['categoria', 'clave']

    def get_queryset(self):
        """Personaliza el queryset según los parámetros de la solicitud"""
        queryset = super().get_queryset()
        categoria = self.request.query_params.get('categoria')
        sucursal_id = self.request.query_params.get('sucursal_id')

        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if sucursal_id:
            queryset = queryset.filter(Q(sucursal_id=sucursal_id) | Q(es_global=True))

        return queryset

    def perform_create(self, serializer):
        """Valida y guarda una nueva configuración"""
        try:
            serializer.save(
                fecha_actualizacion=timezone.now()
            )
        except ValidationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_update(self, serializer):
        """Actualiza una configuración existente"""
        try:
            serializer.save(
                fecha_actualizacion=timezone.now()
            )
        except ValidationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
