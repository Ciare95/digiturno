"""
WSGI config for digiturno project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Obtener el entorno desde variable de entorno o usar 'prod' por defecto para WSGI
environment = os.getenv('DJANGO_ENV', 'prod')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{environment}')

application = get_wsgi_application()
