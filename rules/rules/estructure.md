---
trigger: manual
---

digiturno/
├── .windsurf/
│   └── rules/
│       ├── estructure.md
│       └── peps-8.md
├── backend/
│   ├── apps/
│   │   ├── core/
│   │   │   ├── __pycache__/
│   │   │   ├── migrations/
│   │   │   │   ├── __pycache__/
│   │   │   │   └── 0001_initial.py
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── logic.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── utils.py
│   │   ├── reports/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── turns/
│   │   │   ├── migrations/
│   │   │   │   ├── __pycache__/
│   │   │   │   └── 0001_initial.py
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── consumidores.py
│   │   │   ├── logic.py  
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   └── users/
│   │       ├── __pycache__/
│   │       ├── migrations/
│   │       │   ├── __pycache__/
│   │       │   └── 0001_initial.py
│   │       ├── __init__.py
│   │       ├── admin.py
│   │       ├── admin_views.py
│   │       ├── apps.py
│   │       ├── models.py
│   │       ├── permisos.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── views.py
│   ├── digiturno/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── routing.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── tests/
│   │   ├── test_integration/
│   │   │   ├── test_auth_flow.py
│   │   │   └── test_full_turn_cycle.py
│   │   └── test_unit/
│   │       ├── test_core_models.py
│   │       ├── test_turns_logic.py
│   │       └── test_users_auth.py
│   ├── __init__.py
│   ├── manage.py
│   └── prueba_websocket.html
├── frontend/
│   ├── node_modules/
│   ├── public/
│   │   ├── favicon.ico
│   │   └── index.html
│   ├── src/
│   │   ├── assets/
│   │   │   ├── css/
│   │   │   │   └── hero-image.svg
│   │   │   └── logo.png
│   │   ├── componentes/
│   │   │   ├── Cargador.vue
│   │   │   └── HelloWorld.vue
│   │   ├── enrutador/
│   │   │   └── index.js
│   │   ├── layouts/
│   │   │   ├── LayoutAutenticado.vue
│   │   │   └── LayoutPrincipal.vue
│   │   ├── servicios/
│   │   │   └── tienda/
│   │   │       └── index.js
│   │   ├── utilidades/
│   │   └── vistas/
│   │       ├── administrador/
│   │       │   ├── Configuracion.vue
│   │       │   ├── Estadisticas.vue
│   │       │   ├── GestionEmpleados.vue
│   │       │   ├── GestionServicios.vue
│   │       │   ├── GestionSucursales.vue
│   │       │   ├── GestionUsuarios.vue
│   │       │   └── Panel.vue
│   │       ├── empleado/
│   │       │   ├── Estadisticas.vue
│   │       │   ├── GestionTurnos.vue
│   │       │   └── Panel.vue
│   │       └── usuario/
│   │           ├── IniciarSesion.vue
│   │           ├── Inicio.vue
│   │           ├── NoEncontrado.vue
│   │           ├── Panel.vue
│   │           ├── Perfil.vue
│   │           ├── Registro.vue
│   │           └── Turnos.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── .gitignore
│   ├── babel.config.js
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.js
│   └── vue.config.js
├── node_modules/
├── venv/
├── .gitignore
├── db_postgresql.sql
├── package-lock.json
├── package.json
├── requirements.txt
└── step_by_step.txt