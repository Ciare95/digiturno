# 📋 Configuración del Proyecto Digiturno

## 🚀 Configuración por Entornos

Este proyecto utiliza una configuración modular que permite manejar diferentes entornos de manera eficiente.

### 📁 Estructura de Configuración

```
config/settings/
├── base.py      # Configuración común para todos los entornos
├── dev.py       # Configuración específica para desarrollo
├── prod.py      # Configuración específica para producción
└── test.py      # Configuración específica para testing
```

### 🔧 Variables de Entorno Requeridas

Copia el archivo `env.example` a `.env` y configura las siguientes variables:

#### 🔐 Seguridad (OBLIGATORIAS)
```bash
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DJANGO_ENV=dev  # o 'prod' para producción
```

#### 🗄️ Base de Datos (OBLIGATORIAS)
```bash
DB_NAME=digiturno
DB_USER=tu_usuario_db
DB_PASSWORD=tu_contraseña_segura
DB_HOST=localhost
DB_PORT=5432
```

#### 🔄 Redis (RECOMENDADO para producción)
```bash
REDIS_URL=redis://127.0.0.1:6379
```

#### 🌐 CORS y Dominios
```bash
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### 🔑 JWT
```bash
JWT_ACCESS_TOKEN_LIFETIME_HOURS=1
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_BLACKLIST_AFTER_ROTATION=True
```

## 🚀 Ejecutar el Proyecto

### 1. Entorno de Desarrollo
```bash
# Usar configuración de desarrollo
export DJANGO_ENV=dev
python manage.py runserver
```

### 2. Entorno de Producción
```bash
# Usar configuración de producción
export DJANGO_ENV=prod
python manage.py runserver
```

### 3. Entorno de Testing
```bash
# Usar configuración de testing
export DJANGO_ENV=test
python manage.py test
```

## 📊 Monitoreo y Logging

### 📝 Logs Disponibles
- `logs/django.log` - Logs generales de Django
- `logs/error.log` - Solo errores
- `logs/app.json` - Logs en formato JSON

### 🔍 Niveles de Log
- **Desarrollo**: DEBUG (máximo detalle)
- **Producción**: INFO (información esencial)
- **Testing**: WARNING (solo advertencias)

## 🛡️ Seguridad

### ✅ Configuraciones Implementadas
- [x] Validación de variables de entorno
- [x] Middleware de seguridad
- [x] Rate limiting
- [x] CORS configurado
- [x] JWT con rotación de tokens
- [x] Headers de seguridad

### 🔒 Configuraciones de Producción
- HTTPS forzado
- Cookies seguras
- HSTS habilitado
- XSS protection
- CSRF protection

## 📈 Escalabilidad

### 🗄️ Base de Datos
- Pool de conexiones configurado
- Transacciones atómicas
- Timeouts configurados

### 🚀 Caché
- Redis configurado para producción
- Compresión habilitada
- Pool de conexiones optimizado

### 🔄 WebSockets
- Channels con Redis backend
- Autenticación en WebSockets
- Manejo de múltiples instancias

## 🧪 Testing

### 📋 Comandos de Testing
```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test apps.users

# Ejecutar tests con coverage
coverage run --source='.' manage.py test
coverage report
```

### 🔧 Configuración de Testing
- Base de datos de testing separada
- Logging configurado para testing
- Caché en memoria para testing

## 🚀 Despliegue

### 📋 Checklist de Despliegue
- [ ] Variables de entorno configuradas
- [ ] `DJANGO_ENV=prod`
- [ ] `DEBUG=False`
- [ ] Base de datos configurada
- [ ] Redis configurado
- [ ] Logs configurados
- [ ] Archivos estáticos recolectados
- [ ] Migraciones aplicadas

### 🔧 Comandos de Despliegue
```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

## 📚 Recursos Adicionales

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Django Channels](https://channels.readthedocs.io/en/stable/)
- [Django REST Framework](https://www.django-rest-framework.org/)
