from rest_framework import permissions

class EsAdministrador(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo acceso a administradores
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)