from rest_framework import permissions, status, filters, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from apps.core.models import Configuracion
from apps.core.serializers import ConfiguracionSerializer
from apps.users.permissions.es_administrador import EsAdministrador

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