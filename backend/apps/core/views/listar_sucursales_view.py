from rest_framework import generics, permissions, filters
from apps.core.models import Sucursal
from apps.core.serializers import SucursalSerializer

class ListarSucursalesView(generics.ListAPIView):
    """Vista para listar sucursales activas"""
    queryset = Sucursal.objects.filter(activa=True)
    serializer_class = SucursalSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'ciudad', 'departamento']
    ordering_fields = ['nombre', 'ciudad']
    ordering = ['nombre']