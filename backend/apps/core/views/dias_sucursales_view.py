from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.models import DiaSucursal
from apps.core.serializers import DiaSucursalSerializer


class ListarDiasSucursalesView(generics.ListAPIView):
    """Vista para listar dias de la semana"""
    queryset = DiaSucursal.objects.all()
    serializer_class = DiaSucursalSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sucursal', 'dia_semana']
    search_fields = ['sucursal__nombre', 'dia_semana__nombre']
    ordering_fields = ['sucursal', 'dia_semana']
    ordering = ['sucursal', 'dia_semana']
    