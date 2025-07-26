from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class InicioSesionView(APIView):
    """Vista para el inicio de sesión de usuarios"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = InicioSesionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            # Crear tokens para el usuario
            refresh = RefreshToken.for_user(usuario)
            # Actualizar último acceso (opcional)
            # usuario.ultimo_acceso = timezone.now()
            # usuario.save(update_fields=['ultimo_acceso'])
            # Devolver datos del usuario y tokens
            return Response({
                'usuario': UsuarioSerializer(usuario).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)