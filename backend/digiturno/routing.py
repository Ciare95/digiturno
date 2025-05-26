"""
Configuración de enrutamiento para WebSockets en el proyecto digiturno.

Este archivo define las rutas de WebSocket para la aplicación.
"""

from django.urls import path
from channels.routing import URLRouter

# Aquí importaremos los consumidores de WebSocket cuando los creemos
from apps.turns.consumidores import ConsumidorTurnos

# Patrones de URL para WebSockets
websocket_urlpatterns = [
    # Ejemplos de rutas de WebSocket:
    path('ws/turnos/', ConsumidorTurnos.as_asgi()),
    # path('ws/notificaciones/', NotificacionConsumer.as_asgi()),
]
