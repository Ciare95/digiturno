"""
Configuración de Django para el entorno de pruebas.
"""

from .base import *

# Configuración específica para pruebas
DEBUG = False

# Configuración de base de datos para pruebas
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }
}

# Configuración de caché para pruebas (más rápido)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Configuración de Channels para pruebas
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Configuración de email para pruebas
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Configuración de logging para pruebas
LOGGING['loggers']['django']['level'] = 'ERROR'
LOGGING['loggers']['apps']['level'] = 'ERROR'

# Configuración de JWT para pruebas (tokens cortos)
SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=5)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(hours=1)

# Configuración de archivos estáticos para pruebas
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuración de media para pruebas
MEDIA_ROOT = BASE_DIR / 'test_media'

# Configuración de CORS para pruebas
CORS_ALLOW_ALL_ORIGINS = True

# Configuración de hosts permitidos para pruebas
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']

# Configuración de CSRF para pruebas
CSRF_TRUSTED_ORIGINS = ['http://testserver']

# Configuración de sesiones para pruebas
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Configuración de REST Framework para pruebas
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]

# Configuración de paginación para pruebas
REST_FRAMEWORK['PAGE_SIZE'] = 10

# Configuración de rate limiting para pruebas (más permisivo)
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '1000/hour',
    'user': '10000/hour'
} 