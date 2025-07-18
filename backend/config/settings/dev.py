"""
Configuración de Django para el entorno de desarrollo.
"""

from .base import *

# Configuración específica para desarrollo
DEBUG = True

# Configuración de CORS más permisiva para desarrollo
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Configuración de hosts permitidos para desarrollo
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Configuración de CSRF para desarrollo
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
]

# Configuración de logging para desarrollo
LOGGING['loggers']['django'] = {
    'level': 'WARNING',
    'handlers': ['console'],
    'propagate': False
}
LOGGING['loggers']['django.db.backends'] = {'level': 'WARNING'}
LOGGING['loggers']['django.template'] = {'level': 'WARNING'}
LOGGING['loggers']['django.utils.autoreload'] = {'level': 'WARNING'}
LOGGING['loggers']['apps'] = {'level': 'WARNING'}
LOGGING['loggers']['debug_toolbar'] = {'level': 'WARNING'}

# Configuración de caché para desarrollo (más rápido)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutos
    }
}

# Configuración de sesiones para desarrollo
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Configuración de Channels para desarrollo
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Configuración de email para desarrollo (consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración de debug toolbar (opcional)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Configuración de archivos estáticos para desarrollo
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuración de media para desarrollo
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de JWT para desarrollo (tokens más largos)
SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(days=1)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=30)

# Configuración de REST Framework para desarrollo
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',  # Para desarrollo
]
