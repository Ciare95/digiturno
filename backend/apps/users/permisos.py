from rest_framework import permissions

class EsEmpleado(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un empleado.
    """
    mensaje = 'El usuario debe ser un empleado para acceder a este recurso.'
    
    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado y es un empleado
        if request.user.is_authenticated:
            return hasattr(request.user, 'perfil_empleado')
        return False

class EsAdministrador(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un administrador.
    """
    mensaje = 'El usuario debe ser un administrador para acceder a este recurso.'
    
    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado y es un administrador
        if request.user.is_authenticated:
            return hasattr(request.user, 'perfil_administrador')
        return False

class EsUsuarioNormal(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un usuario normal
    (no es empleado ni administrador).
    """
    mensaje = 'El usuario debe ser un usuario normal para acceder a este recurso.'
    
    def has_permission(self, request, view):
        # Verificar si el usuario está autenticado y no es ni empleado ni administrador
        if request.user.is_authenticated:
            return not (hasattr(request.user, 'perfil_empleado') or 
                      hasattr(request.user, 'perfil_administrador'))
        return False
