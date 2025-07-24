from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import RegistroEmpleadoSerializer
from ..serializers import UsuarioSerializer

class RegistroEmpleadoView(APIView):
    """Vista para el registro de nuevos empleados"""
    permission_classes = [permissions.IsAdminUser]  # Solo administradores pueden crear empleados

    def post(self, request):
        serializer = RegistroEmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            # No es necesario devolver el token aquí, ya que es un administrador quien está creando el empleado
            return Response({
                'usuario': UsuarioSerializer(usuario).data,
                'mensaje': 'Empleado registrado exitosamente',
                'empleado_id': usuario.perfil_empleado.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)