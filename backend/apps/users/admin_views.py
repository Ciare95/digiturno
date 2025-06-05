from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Usuario, Empleado, Administrador
from .serializers import UsuarioSerializer, EmpleadoSerializer, AdministradorSerializer
from .permisos import EsAdministrador

class GestionUsuariosViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de usuarios por parte del administrador.
    Permite listar, crear, actualizar y eliminar usuarios.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [EsAdministrador]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'cedula']
    ordering_fields = ['username', 'date_joined', 'last_login']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.action == 'empleados':
            return EmpleadoSerializer
        elif self.action == 'administradores':
            return AdministradorSerializer
        return UsuarioSerializer

    @action(detail=False, methods=['get'])
    def empleados(self, request):
        """Retorna la lista de usuarios con rol de empleado"""
        empleados = Empleado.objects.select_related('usuario').all()
        serializer = self.get_serializer(empleados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def administradores(self, request):
        """Retorna la lista de usuarios con rol de administrador"""
        administradores = Administrador.objects.select_related('usuario').all()
        serializer = self.get_serializer(administradores, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """Desactiva el usuario en lugar de eliminarlo"""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['post'])
    def reactivar(self, request, pk=None):
        """Reactivar un usuario desactivado"""
        usuario = self.get_object()
        usuario.is_active = True
        usuario.save()
        return Response({'status': 'usuario reactivado'})