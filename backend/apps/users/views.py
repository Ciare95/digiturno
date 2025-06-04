from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .permisos import EsEmpleado, EsAdministrador
from .serializers import (
    RegistroUsuarioSerializer, 
    InicioSesionSerializer, 
    UsuarioSerializer,
    EmpleadoLoginSerializer as EmpleadoSerializer,
    EmpleadoLoginSerializer as InicioSesionEmpleadoSerializer,
    AdministradorSerializer,
    InicioSesionAdminSerializer,
    RegistroEmpleadoSerializer
)

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

class InicioSesionEmpleadoView(APIView):
    """Vista para el inicio de sesión de empleados"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = InicioSesionEmpleadoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            usuario = serializer.validated_data['usuario']
            empleado = serializer.validated_data['empleado']
            
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
