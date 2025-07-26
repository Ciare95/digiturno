from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

class VerificarRolView(APIView):
    """Vista para verificar el rol del usuario autenticado"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Devuelve el rol del usuario autenticado"""
        usuario = request.user
        datos_respuesta = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'rol': 'usuario'
        }
        
        # Verificar si el usuario es un empleado
        if hasattr(usuario, 'perfil_empleado'):
            datos_respuesta['rol'] = 'empleado'
            datos_respuesta['codigo_empleado'] = usuario.perfil_empleado.codigo_empleado
            datos_respuesta['ventanilla'] = usuario.perfil_empleado.ventanilla_asignada
        
        # Verificar si el usuario es un administrador
        elif hasattr(usuario, 'perfil_administrador'):
            datos_respuesta['rol'] = 'admin'
            datos_respuesta['nivel_acceso'] = usuario.perfil_administrador.nivel_acceso
        
        return Response(datos_respuesta)
