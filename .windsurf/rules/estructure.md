---
trigger: manual
---

digiturno/
├── backend/
│   ├── manage.py
│   ├── digiturno/              # Proyecto principal de Django
│   │   ├── __init__.py
│   │   ├── asgi.py             # Configuración para Channels 
│   │   ├── settings.py         # Configuración del proyecto 
│   │   ├── urls.py             # URLs principales del proyecto
│   │   └── wsgi.py
│   │
│   ├── apps/                   # Aplicaciones de Django
│   │   ├── __init__.py
│   │   ├── core/               # App para modelos y lógica compartida 
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # Modelos: Turno, Servicio, Sucursal, CalificacionServicio, Configuracion
│   │   │   ├── admin.py        # Registro de modelos en el panel de 
│   │   │   ├── utils.py        # Funciones de utilidad (similar a tu apps/common/utils.py)
│   │   │   └── logic.py        # Lógica de negocio principal (ej. algoritmos de turnos) 
│   │   │
│   │   ├── users/              # App para autenticación y gestión de usuarios
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # Modelo de Usuario con roles (Usuario, Empleado, Administrador)
│   │   │   ├── serializers.py  # Serializers para APIs de usuarios
│   │   │   ├── views.py        # Vistas para registro, login (general, empleado, admin)
│   │   │   └── urls.py         # URLs para /api/auth/...
│   │   │
│   │   ├── turns/              # App para la lógica de turnos y APIs relacionadas
│   │   │   ├── __init__.py
            ├── apps.py
│   │   │   ├── models.py       # Podría incluir modelos específicos de turnos si no están en core
│   │   │   ├── serializers.py  # Serializers para APIs de turnos 
│   │   │   ├── views.py        # Vistas para APIs:
│   │   │   │                   #   - Cliente: seleccion_servicio, estado_turno, calificacion, agenda, historial
│   │   │   │                   #   - Empleado: gestion_turnos, panel_atencion, cola_turnos
│   │   │   │                   #   - Admin: gestion_modulos (servicios), gestion_sucursales, configuracion_general
│   │   │   └── urls.py         # URLs para /api/servicios/, /api/turnos/, /api/calificaciones/, etc.
│   │   │
│   │   └── reports/            # App para estadísticas y reportes 
│   │       ├── __init__.py
│   │       ├── serializers.py  # Serializers para datos de estadísticas
│   │       ├── views.py        # Vistas para APIs de estadísticas (empleado, admin)
│   │       └── urls.py         # URLs para /api/empleado/estadisticas/, /api/admin/reportes/
│   │
│   └── tests/                  # Carpeta para pruebas del backend 
│       ├── __init__.py
│       ├── test_unit/
│       │   ├── test_core_models.py
│       │   ├── test_users_auth.py
│       │   └── test_turns_logic.py
│       └── test_integration/
│           ├── test_auth_flow.py
│           └── test_full_turn_cycle.py
│
├── frontend/                   # Proyecto unificado de Vue.js
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── assets/             # Imágenes, fuentes, etc.
│   │   ├── components/         # Componentes reutilizables
│   │   │   ├── common/         # Botones, modales, inputs, etc.
│   │   │   ├── layout/         # Componentes de estructura (Navbar, Sidebar, Footer)
│   │   │   └── TurnNotification.vue # Componente para notificación 
│   │   ├── router/
│   │   │   └── index.js        # Configuración de Vue Router con rutas protegidas (Fase 2.1)
│   │   ├── services/           # Lógica de llamadas a API (ej. authService.js, turnService.js)
│   │   ├── store/              # Gestión de estado (Pinia o Vuex) 
│   │   ├── views/              # Vistas principales por rol 
│   │   │   ├── AuthView.vue    # Vista de Login/Registro general
│   │   │   ├── admin/          # Vistas específicas para Administradores
│   │   │   │   ├── AdminLayout.vue
│   │   │   │   ├── DashboardView.vue        
│   │   │   │   ├── ModulesView.vue           # Gestión de Módulos/Servicios (Fase 1.6.3)
│   │   │   │   ├── AdvancedStatsView.vue     # Estadísticas Avanzadas 
│   │   │   │   ├── UserManagementView.vue    # Gestión de Usuarios 
│   │   │   │   ├── BranchManagementView.vue  # Gestión de Sucursales 
│   │   │   │   └── GeneralConfigView.vue     # Configuración General 
│   │   │   ├── employee/       # Vistas específicas para Empleados
│   │   │   │   ├── EmployeeLayout.vue
│   │   │   │   ├── TurnManagementView.vue    # Gestión de Turnos 
│   │   │   │   ├── AttentionPanelView.vue    # Panel de Atención 
│   │   │   │   ├── QueueStatusView.vue       # Cola de Turnos 
│   │   │   │   └── EmployeeStatsView.vue     # Estadísticas del Empleado 
│   │   │   └── user/           # Vistas específicas para Usuarios (Cliente)
│   │   │       ├── UserLayout.vue
│   │   │       ├── ServiceSelectionView.vue  
│   │   │       ├── TurnStatusView.vue         - Polling
│   │   │       ├── ServiceRatingView.vue     
│   │   │       ├── TurnSchedulingView.vue    
│   │   │       └── TurnHistoryView.vue       
│   │   ├── App.vue             # Componente raíz de Vue
│   │   └── main.js             # Punto de entrada de la aplicación Vue
│   ├── tests/                  # Pruebas Frontend 
│   │   ├── unit/               # Pruebas unitarias de componentes
│   │   └── e2e/                # Pruebas End-to-End 
│   ├── .gitignore
│   ├── package.json
│   ├── tailwind.config.js      # Configuración de Tailwind CSS 
│   └── vite.config.js (o vue.config.js)
│
├── .gitignore                  # .gitignore general del proyecto
├── requirements.txt            # Dependencias de Python 
└── README.md                   # Documentación del proyecto