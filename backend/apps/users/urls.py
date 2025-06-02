from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegistroUsuarioView, 
    InicioSesionView, 
    PerfilUsuarioView,
    InicioSesionEmpleadoView,
    InicioSesionAdminView,
    VerificarRolView
)

urlpatterns = [
    # Rutas de autenticación para usuarios normales
    path('auth/registro/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('auth/iniciar-sesion/', InicioSesionView.as_view(), name='inicio_sesion'),
    path('auth/token/refrescar/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Rutas de autenticación para empleados y administradores
    path('auth/empleado/iniciar-sesion/', InicioSesionEmpleadoView.as_view(), name='inicio_sesion_empleado'),
    path('auth/admin/iniciar-sesion/', InicioSesionAdminView.as_view(), name='inicio_sesion_admin'),
    
    # Ruta de perfil de usuario
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil_usuario'),
    
    # Ruta para verificar el rol del usuario autenticado
    path('auth/verificar-rol/', VerificarRolView.as_view(), name='verificar_rol'),
]