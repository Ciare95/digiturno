from django.apps import AppConfig


class TurnsConfig(AppConfig):
    """
    Configuración para la aplicación de turnos.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.turns'
    verbose_name = 'Gestión de Turnos'
