from rest_framework import permissions, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from apps.users.models.empleado import Empleado
from apps.users.serializers.roles_serializer import EmpleadoSerializer
from apps.users.serializers.registro_empleado_serializer import RegistroEmpleadoSerializer
from apps.users.permissions.es_administrador import EsAdministrador

class EmpleadoAdminViewSet(viewsets.ModelViewSet):
	"""ViewSet para la gestión completa de empleados por el administrador"""
	queryset = Empleado.objects.all()
	permission_classes = [permissions.IsAuthenticated, EsAdministrador]
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	filterset_fields = ['sucursal', 'estado_conexion']
	search_fields = ['codigo_empleado', 'usuario__username', 'usuario__email']
	ordering_fields = ['codigo_empleado', 'usuario__username']
	ordering = ['codigo_empleado']

	def get_serializer_class(self):
		if self.action in ['create', 'update', 'partial_update']:
			return RegistroEmpleadoSerializer
		return EmpleadoSerializer 