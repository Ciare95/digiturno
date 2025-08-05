from rest_framework import generics, permissions
from django.utils import timezone
from rest_framework.response import Response
from ..models import Turno
from ..serializers import TurnoSerializer
from apps.users.permissions.es_empleado import EsEmpleado
from rest_framework.exceptions import APIException

class UltimosTurnosFinalizadosView(generics.ListAPIView):
    """Vista para obtener los últimos 5 turnos finalizados para un empleado"""
    serializer_class = TurnoSerializer
    permission_classes = [permissions.IsAuthenticated, EsEmpleado]

    def get_queryset(self):
        """
        Devuelve los últimos 5 turnos finalizados para el empleado autenticado
        """
        try:
            if not hasattr(self.request.user, 'perfil_empleado'):
                raise APIException('Usuario no tiene perfil de empleado')
                
            empleado = self.request.user.perfil_empleado
            
            return Turno.objects.filter(
                empleado=empleado,
                estado=Turno.EstadoTurno.FINALIZADO
            ).select_related('servicio').order_by('-fecha_finalizacion')[:5]
        except Exception as e:
            print(f"Error en UltimosTurnosFinalizadosView: {str(e)}")
            raise APIException(f"Error al obtener turnos finalizados: {str(e)}")
            
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            
            # Format the response data to match frontend expectations
            formatted_data = []
            for turno in serializer.data:
                # Handle both serialized service object and service ID cases
                servicio_nombre = 'Servicio no disponible'
                if isinstance(turno.get('servicio'), dict):
                    servicio_nombre = turno['servicio'].get('nombre', servicio_nombre)
                elif 'servicio_nombre' in turno:
                    servicio_nombre = turno['servicio_nombre']
                
                formatted_data.append({
                    'id': turno['id'],
                    'numero': turno['numero_turno'],
                    'servicio': servicio_nombre,
                    'cliente': turno.get('nombre_cliente', 'Cliente no disponible'),
                    'estado': 'Atendido',
                    'fecha_creacion': turno.get('fecha_creacion'),
                    'hora': turno.get('fecha_finalizacion', '').split('T')[1][:5] if turno.get('fecha_finalizacion') else '--:--'
                })
                
            return Response(formatted_data)
        except Exception as e:
            print(f"Error formateando datos de turnos: {str(e)}")
            raise APIException(f"Error al procesar los datos de turnos: {str(e)}")
