# DigiTurno - Backend API

Sistema de gestión de turnos digital desarrollado con Django REST Framework.

## 🚀 Características

- **Autenticación JWT**: Sistema de autenticación seguro con tokens JWT
- **Gestión de Turnos**: Creación, seguimiento y gestión completa de turnos
- **Roles de Usuario**: Usuario, Empleado y Administrador con permisos específicos
- **APIs RESTful**: APIs completas para todas las funcionalidades
- **WebSockets**: Soporte para notificaciones en tiempo real
- **Configuración Modular**: Configuraciones separadas para desarrollo, producción y testing
- **Base de Datos PostgreSQL**: Base de datos robusta y escalable

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- Redis (opcional, para producción)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd digiturno/backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 5. Configurar base de datos
```bash
# Crear base de datos PostgreSQL
createdb digiturno

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 6. Crear datos de prueba (opcional)
```bash
python crear_datos_prueba.py
```

### 7. Ejecutar el servidor
```bash
python manage.py runserver
```

## 🏗️ Estructura del Proyecto

```
backend/
├── apps/                    # Aplicaciones Django
│   ├── core/               # Modelos base (Sucursal, Servicio)
│   ├── users/              # Gestión de usuarios y autenticación
│   ├── turns/              # Lógica de turnos y colas
│   └── reports/            # Reportes y estadísticas
├── config/                 # Configuraciones
│   └── settings/
│       ├── base.py         # Configuración base
│       ├── dev.py          # Configuración de desarrollo
│       ├── prod.py         # Configuración de producción
│       └── test.py         # Configuración de testing
├── tests/                  # Tests unitarios e integración
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos por usuarios
└── logs/                   # Archivos de log
```

## 🔧 Configuración

### Variables de Entorno

Copia `env.example` a `.env` y configura las siguientes variables:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=digiturno
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000

# JWT
JWT_ACCESS_TOKEN_LIFETIME_HOURS=24
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Entornos

- **Desarrollo**: `DJANGO_ENV=dev`
- **Producción**: `DJANGO_ENV=prod`
- **Testing**: `DJANGO_ENV=test`

## 📚 APIs

### Autenticación
- `POST /api/auth/registro/` - Registro de usuarios
- `POST /api/auth/iniciar-sesion/` - Inicio de sesión
- `POST /api/auth/empleado/iniciar-sesion/` - Login empleado
- `POST /api/auth/admin/iniciar-sesion/` - Login administrador

### Turnos
- `POST /api/turnos/` - Crear turno
- `GET /api/turnos/mio/` - Mis turnos
- `DELETE /api/turnos/mio/{id}/` - Cancelar turno
- `GET /api/turnos/agenda/` - Turnos agendados
- `GET /api/turnos/historial/` - Historial de turnos

### Empleados
- `POST /api/empleado/turnos/siguiente/` - Llamar siguiente turno
- `POST /api/empleado/turnos/{id}/completar/` - Completar turno
- `POST /api/empleado/turnos/{id}/transferir/` - Transferir turno
- `GET /api/empleado/estadisticas/` - Estadísticas del empleado

### Administración
- `GET /api/admin/panel/` - Panel de administración
- `GET /api/admin/reportes/` - Reportes
- `GET /api/admin/usuarios/` - Gestión de usuarios
- `GET /api/admin/sucursales/` - Gestión de sucursales

## 🧪 Testing

### Ejecutar tests
```bash
# Todos los tests
python -m pytest

# Tests específicos
python -m pytest tests/test_unit/
python -m pytest tests/test_integration/

# Con cobertura
python -m pytest --cov=apps --cov-report=html
```

### Estructura de tests
```
tests/
├── test_unit/              # Tests unitarios
│   ├── test_core_models.py
│   ├── test_users_auth.py
│   ├── test_turns_models.py
│   └── test_turns_views.py
└── test_integration/       # Tests de integración
    ├── test_auth_flow.py
    └── test_full_turn_cycle.py
```

## 🚀 Despliegue

### Desarrollo
```bash
python manage.py runserver
```

### Producción
```bash
# Configurar variables de entorno
export DJANGO_ENV=prod

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar con gunicorn
gunicorn digiturno.wsgi:application
```

## 📊 Monitoreo

### Logs
Los logs se guardan en `logs/django.log` y también se muestran en consola.

### Debug Toolbar
En desarrollo, Django Debug Toolbar está habilitado para debugging.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para soporte técnico, contacta al equipo de desarrollo o crea un issue en el repositorio.

## 🔄 Changelog

### v1.0.0
- Implementación inicial del sistema de turnos
- APIs completas para gestión de turnos
- Sistema de autenticación JWT
- Configuración modular
- Tests unitarios e integración 