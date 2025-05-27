---
trigger: manual
---

digiturno/
├── .gitignore
├── db_postgresql.sql
├── requirements.txt
├── venv/
├── windsurf/
│   └── rules/
│       ├── estructure.md
│       └── peps-8.md
├── backend/
│   ├── manage.py
│   ├── apps/
│   │   ├── __pycache__/
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
│   │   │   └── utils.py
│   │   ├── reports/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   ├── turns/
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── consumidores.py
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
│   │       ├── apps.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── views.py
│   ├── digiturno/
│   │   ├── __pycache__/
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
│   │       ├── test_users_auth.py
│   │       └── __init__.py
│   └── prueba_websocket.html
└── frontend/
    ├── public/
    │   └── index.html
    └── src/
        ├── assets/
        ├── components/
        │   ├── common/
        │   └── layout/
        │       └── TurnNotification.vue
        ├── router/
        │   └── index.js
        ├── services/
        ├── store/
        ├── views/
        │   ├── admin/
        │   │   ├── AdminLayout.vue
        │   │   ├── AdvanceStatsView.vue
        │   │   ├── BranchManagementView.vue
        │   │   ├── DashboardView.vue
        │   │   ├── GeneralConfigView.vue
        │   │   ├── ModulesView.vue
        │   │   └── UserManagementView.vue
        │   ├── employee/
        │   │   ├── AttentionPanelView.vue
        │   │   ├── EmployeeLayout.vue
        │   │   ├── EmployeeStatsView.vue
        │   │   ├── QueueStatusView.vue
        │   │   └── TurnManagementView.vue
        │   └── user/
        │       ├── ServiceRatingView.vue
        │       ├── ServiceSelectionView.vue
        │       ├── TurnHistoryView.vue
        │       ├── TurnSchedulingView.vue
        │       ├── TurnStatusView.vue
        │       └── UserLayout.vue
        ├── AuthView.vue
        ├── App.vue
        ├── main.js
        ├── tests/
        │   ├── e2e/
        │   └── unit/
        ├── package.json
        ├── tailwind.config.js
        └── vue.config.js