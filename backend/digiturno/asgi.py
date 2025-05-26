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

# Configurar el entorno de Django antes de importar módulos que dependan de la configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiturno.settings')

# Importamos las rutas de WebSocket después de configurar el entorno
import digiturno.routing

# Configuración de la aplicación ASGI con soporte para HTTP y WebSocket
# Configuración simplificada para pruebas (sin validador de origen)
application = ProtocolTypeRouter({
    # Django maneja las solicitudes HTTP de forma predeterminada
    'http': get_asgi_application(),
    
    # Configuración simplificada para pruebas
    # Omitimos AllowedHostsOriginValidator temporalmente
    'websocket': AuthMiddlewareStack(
        URLRouter(
            digiturno.routing.websocket_urlpatterns
        )
    ),
})
