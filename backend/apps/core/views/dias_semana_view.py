from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.models import DiasSemana
from apps.core.serializers import DiasSemanaSerializer

class ListarDiasSemanaView(generics.ListAPIView):
    """Vista para listar dias de la semana"""
    queryset = DiasSemana.objects.all()
    serializer_class = DiasSemanaSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nombre']
    search_fields = ['nombre']
    ordering_fields = ['nombre']
    ordering = ['nombre']

