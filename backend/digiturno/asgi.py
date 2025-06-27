"""
ASGI config for digiturno project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Obtener el entorno desde variable de entorno o usar 'prod' por defecto para ASGI
environment = os.getenv('DJANGO_ENV', 'prod')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{environment}')

# Importamos las rutas de WebSocket después de configurar el entorno
import digiturno.routing

# Configuración de la aplicación ASGI con soporte para HTTP y WebSocket
application = ProtocolTypeRouter({

    'http': get_asgi_application(),
    
    'websocket': AuthMiddlewareStack(
        URLRouter(
            digiturno.routing.websocket_urlpatterns
        )
    ),
})
