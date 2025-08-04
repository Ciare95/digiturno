from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import InicioSesionAdminSerializer, UsuarioSerializer, AdministradorSerializer

class InicioSesionAdminView(APIView):
    """Vista para el inicio de sesión de administradores"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = InicioSesionAdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            admin = serializer.validated_data['admin']
            
            # Crear tokens para el usuario
            refresh = RefreshToken.for_user(usuario)
            
            # Añadir información de rol al token
            refresh['rol'] = 'admin'
            refresh['nivel_acceso'] = admin.nivel_acceso
            
            # Devolver datos del administrador y tokens
            return Response({
                'usuario': UsuarioSerializer(usuario).data,
                'admin': AdministradorSerializer(admin).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)