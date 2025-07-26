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