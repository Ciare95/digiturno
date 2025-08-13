from rest_framework import permissions, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.models import Sucursal
from apps.core.serializers import SucursalSerializer
from apps.users.permissions.es_administrador import EsAdministrador

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
        """Guarda la sucursal"""
        serializer.save()

    def perform_update(self, serializer):
        """Actualiza la sucursal"""
        serializer.save()
