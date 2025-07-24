from rest_framework import permissions

class EsAdministrador(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un administrador.
    """
    mensaje = 'El usuario debe ser un administrador para acceder a este recurso.'
    
    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado y es un administrador o un superusuario
        if request.user.is_authenticated:
            return hasattr(request.user, 'perfil_administrador') or request.user.is_superuser
        return False