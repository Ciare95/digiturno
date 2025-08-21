"""
Configuración de Django para el entorno de desarrollo.
"""

from .base import *

# Configuración específica para desarrollo
DEBUG = True

# Configuración de hosts permitidos para desarrollo
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Configuración de CORS para desarrollo
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]

# Configuración de CSRF para desarrollo
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]

# Configuración de logging para desarrollo
LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['apps']['level'] = 'INFO'
LOGGING['loggers']['django.db.backends']['level'] = 'INFO'

# Configuración de caché para desarrollo (memoria local)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Configuración de Channels para desarrollo (memoria local)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Configuración de JWT para desarrollo (tokens más largos)
SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=24)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=30)
SIMPLE_JWT['ROTATE_REFRESH_TOKENS'] = False
SIMPLE_JWT['BLACKLIST_AFTER_ROTATION'] = False

# Configuración de base de datos para desarrollo
DATABASES['default']['CONN_MAX_AGE'] = 0  # Sin pool de conexiones en desarrollo

# Configuración de email para desarrollo (consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración de archivos estáticos para desarrollo
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuración de debug toolbar (solo en desarrollo)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Configuración de CORS para desarrollo
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
