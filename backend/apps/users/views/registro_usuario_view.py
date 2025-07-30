from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import RegistroUsuarioSerializer, UsuarioSerializer

class RegistroUsuarioView(APIView):
    """Vista para el registro de nuevos usuarios"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegistroUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            # Crear tokens para el usuario
            refresh = RefreshToken.for_user(usuario)
            # Devolver datos del usuario y tokens
            return Response({
                'usuario': UsuarioSerializer(usuario).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)