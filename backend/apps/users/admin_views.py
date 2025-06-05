from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from .models import Usuario, Empleado, Administrador
from .serializers import (
    UsuarioSerializer, 
    EmpleadoSerializer,
    AdministradorSerializer,
    RegistroUsuarioSerializer
)
from .permisos import EsAdministrador

class GestionUsuariosAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de usuarios por parte del administrador.
    """
    queryset = Usuario.objects.all()
    permission_classes = [EsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'cedula']
    ordering_fields = ['username', 'date_joined', 'last_login']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.action == 'create':
            return RegistroUsuarioSerializer
        return UsuarioSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'mensaje': 'Usuario creado exitosamente'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UsuarioSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'id': usuario.id,
                'username': usuario.username,
                'email': usuario.email,
                'mensaje': 'Usuario actualizado exitosamente'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        usuario = self.get_object()
        usuario.is_active = False
        usuario.save()
        return Response({
            'mensaje': f'Usuario {usuario.username} desactivado exitosamente'
        })

    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        usuario = self.get_object()
        usuario.is_active = True
        usuario.save()
        return Response({
            'mensaje': f'Usuario {usuario.username} activado exitosamente'
        })