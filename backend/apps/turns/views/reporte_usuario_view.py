from rest_framework import generics, permissions
from django.db.models import Value as V
from django.db.models.functions import Concat
from apps.users.permissions.es_administrador import EsAdministrador
from apps.users.models.usuario import Usuario

class ReporteUsuariosView(generics.GenericAPIView):
    """Vista para generar reportes de usuarios"""
    permission_classes = [permissions.IsAuthenticated, EsAdministrador]
    
    def get_reporte_usuarios(self):
        try:
            usuarios = Usuario.objects.annotate(
                nombre_completo=Concat('first_name', V(' '), 'last_name')
            ).values(
                'id',
                'username',
                'nombre_completo',
                'email',
                'cedula',
                'telefono',
                'ultimo_acceso',
                'date_joined'
            )
            
            return {
                'usuarios': list(usuarios),
                'total': usuarios.count()
            }
        except Exception as e:
            raise Exception(f"Error al generar reporte de usuarios: {str(e)}")