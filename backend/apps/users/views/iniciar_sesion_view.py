from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import InicioSesionSerializer, UsuarioSerializer
from ..models import Empleado, Administrador


class InicioSesionView(APIView):
    """Vista para el inicio de sesión de usuarios"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = InicioSesionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            # Crear tokens para el usuario
            refresh = RefreshToken.for_user(usuario)
            
            # Determinar tipo de usuario
            es_empleado = Empleado.objects.filter(usuario=usuario).exists()
            es_admin = Administrador.objects.filter(usuario=usuario).exists()
            
            # Devolver datos del usuario y tokens
            return Response({
                'usuario': UsuarioSerializer(usuario).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'es_empleado': es_empleado,
                'es_admin': es_admin
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
