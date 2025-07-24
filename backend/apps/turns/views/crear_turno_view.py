from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import TurnoSerializer, CrearTurnoSerializer
from ..services import GestorTurnos

class CrearTurnoView(APIView):
    """Vista para crear un nuevo turno"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = CrearTurnoSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                turno = GestorTurnos.crear_turno(
                    usuario=request.user if request.user.is_authenticated else None,
                    servicio=serializer.validated_data['servicio'],
                    sucursal=serializer.validated_data['sucursal'],
                    es_agendado=serializer.validated_data.get('es_agendado', False),
                    fecha_agendada=serializer.validated_data.get('fecha_agendada')
                )
                return Response(
                    TurnoSerializer(turno).data,
                    status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
