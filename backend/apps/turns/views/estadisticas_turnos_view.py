from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Q
from ..models import Turno

class EstadisticasTurnosView(APIView):
    """Endpoint para obtener estadísticas de turnos"""
    
    def get(self, request):
        hoy = timezone.now().date()
        
        # Obtener conteos de turnos
        total_turnos = Turno.objects.filter(fecha_creacion__date=hoy).count()
        turnos_atendidos = Turno.objects.filter(
            fecha_creacion__date=hoy,
            estado='ATENDIDO'
        ).count()
        turnos_pendientes = Turno.objects.filter(
            fecha_creacion__date=hoy,
            estado__in=['PENDIENTE', 'EN_ATENCION']
        ).count()
        
        data = {
            'turnosHoy': total_turnos,
            'turnosAtendidos': turnos_atendidos,
            'turnosPendientes': turnos_pendientes
        }
        
        return Response(data, status=status.HTTP_200_OK)
