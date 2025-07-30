from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import EmpleadoLoginSerializer, UsuarioSerializer, EmpleadoSerializer

class InicioSesionEmpleadoView(APIView):
    """Vista para el inicio de sesión de empleados"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = EmpleadoLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            validated_data = serializer.validated_data
            usuario = validated_data['usuario']
            empleado = validated_data['empleado']
            
            # Crear tokens para el usuario
            refresh = RefreshToken.for_user(usuario)
            
            # Añadir información de rol al token
            refresh['rol'] = 'empleado'
            refresh['codigo_empleado'] = empleado.codigo_empleado
            
            # Devolver datos del empleado y tokens
            return Response({
                'usuario': UsuarioSerializer(usuario).data,
                'empleado': EmpleadoSerializer(empleado).data,  
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)