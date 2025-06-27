# DigiTurno - Sistema de Gestión de Turnos Digital

Sistema completo de gestión de turnos digital desarrollado con Django (Backend) y Vue.js (Frontend).

## 🎯 Descripción

DigiTurno es una solución integral para la gestión de turnos en entidades públicas y privadas. Permite a los usuarios solicitar turnos, a los empleados atenderlos de manera eficiente, y a los administradores gestionar y monitorear todo el proceso.

## 🚀 Características Principales

### Para Usuarios
- ✅ Solicitud de turnos en tiempo real
- ✅ Seguimiento del estado del turno
- ✅ Agenda de turnos futuros
- ✅ Historial de turnos
- ✅ Calificación del servicio
- ✅ Notificaciones en tiempo real

### Para Empleados
- ✅ Panel de atención de turnos
- ✅ Llamado automático del siguiente turno
- ✅ Transferencia de turnos entre servicios
- ✅ Estadísticas de rendimiento
- ✅ Gestión de colas

### Para Administradores
- ✅ Dashboard completo con métricas
- ✅ Gestión de usuarios y empleados
- ✅ Configuración de servicios y sucursales
- ✅ Reportes detallados
- ✅ Monitoreo en tiempo real

## 🏗️ Arquitectura

```
digiturno/
├── backend/                 # API Django REST Framework
│   ├── apps/               # Aplicaciones Django
│   ├── config/             # Configuraciones
│   ├── tests/              # Tests unitarios e integración
│   └── requirements.txt    # Dependencias Python
├── frontend/               # Aplicación Vue.js
│   ├── src/                # Código fuente
│   ├── public/             # Archivos públicos
│   └── package.json        # Dependencias Node.js
└── docs/                   # Documentación
```

## 🛠️ Tecnologías

### Backend
- **Django 4.2** - Framework web
- **Django REST Framework** - APIs RESTful
- **PostgreSQL** - Base de datos
- **Redis** - Cache y WebSockets
- **JWT** - Autenticación
- **Channels** - WebSockets para tiempo real

### Frontend
- **Vue.js 3** - Framework frontend
- **Vue Router** - Enrutamiento
- **Tailwind CSS** - Estilos
- **Axios** - Cliente HTTP
- **Pinia** - Gestión de estado

## 📋 Requisitos

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Redis (opcional)

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd digiturno
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Editar .env con tus configuraciones
python manage.py migrate
python manage.py runserver
```

### 3. Frontend
```bash
cd frontend
npm install
npm run serve
```

### 4. Crear datos de prueba
```bash
cd backend
python crear_datos_prueba.py
```

## 📚 Documentación

- [Guía de Instalación](backend/README.md)
- [Documentación de APIs](docs/api.md)
- [Guía de Desarrollo](docs/development.md)
- [Guía de Despliegue](docs/deployment.md)

## 🧪 Testing

### Backend
```bash
cd backend
python -m pytest
```

### Frontend
```bash
cd frontend
npm run test:unit
```

## 🚀 Despliegue

### Desarrollo
```bash
# Backend
cd backend
python manage.py runserver

# Frontend
cd frontend
npm run serve
```

### Producción
Ver [Guía de Despliegue](docs/deployment.md) para instrucciones detalladas.

## 📊 Estado del Proyecto

### ✅ Completado (FASE 1)
- [x] Configuración del proyecto
- [x] Modelos de base de datos
- [x] Sistema de autenticación JWT
- [x] APIs RESTful completas
- [x] Lógica de negocio de turnos
- [x] Tests unitarios e integración
- [x] Configuración modular
- [x] Documentación básica

### 🔄 En Desarrollo (FASE 2)
- [ ] Frontend Vue.js
- [ ] Interfaces de usuario
- [ ] Integración frontend-backend
- [ ] WebSockets para tiempo real

### 📋 Pendiente
- [ ] Despliegue en producción
- [ ] Optimizaciones de rendimiento
- [ ] Funcionalidades avanzadas

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- 📧 Email: soporte@digiturno.com
- 📱 WhatsApp: +57 XXX XXX XXXX
- 🐛 Issues: [GitHub Issues](https://github.com/tu-usuario/digiturno/issues)

## 🙏 Agradecimientos

- Equipo de desarrollo
- Contribuidores de la comunidad
- Usuarios beta que proporcionaron feedback

---

**DigiTurno** - Transformando la gestión de turnos digitalmente 🚀 