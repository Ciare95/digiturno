from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.serializers import UsuarioSerializer

class PerfilUsuarioView(APIView):
    """Vista para obtener y actualizar el perfil del usuario autenticado"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)