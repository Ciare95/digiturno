from rest_framework import generics, permissions

from ..models import ColaTurnos
from ..serializers import ColaTurnosSerializer
from apps.users.permissions.es_empleado import EsEmpleado

class ListarColaTurnosEmpleadoView(generics.ListAPIView):
    """Vista para listar los turnos en cola para un empleado específico"""
    serializer_class = ColaTurnosSerializer
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]
    
    def get_queryset(self):
        """
        Devuelve solo los turnos activos en cola para los servicios 
        asignados al empleado en su sucursal
        """
        empleado = self.request.user.perfil_empleado
        servicios_empleado = empleado.servicios.all()
        
        return ColaTurnos.objects.filter(
            activo=True,
            turno__servicio__in=servicios_empleado,
            turno__sucursal=empleado.sucursal
        ).select_related(
            'turno', 
            'turno__servicio'
        ).order_by('turno__servicio', 'posicion_cola')
