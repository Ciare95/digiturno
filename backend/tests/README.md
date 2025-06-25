# Guía de Tests para el Sistema DigiTurno

Esta guía te explica cómo ejecutar y trabajar con los tests unitarios e integración del sistema DigiTurno.

## Estructura de Tests

```
backend/tests/
├── conftest.py              # Configuración global de pytest
├── test_unit/               # Tests unitarios
│   ├── test_core_models.py     # Tests de modelos core
│   ├── test_users_auth.py      # Tests de autenticación
│   ├── test_turns_models.py    # Tests de modelos de turnos
│   ├── test_turns_views.py     # Tests de vistas de turnos
│   ├── test_turns_logic.py     # Tests de lógica de negocio
│   ├── test_turns_serializers.py # Tests de serializers
│   └── test_reports_views.py   # Tests de reportes
└── test_integration/        # Tests de integración
    ├── test_auth_flow.py       # Flujo completo de autenticación
    └── test_full_turn_cycle.py # Ciclo completo de turnos
```

## Requisitos

Asegúrate de tener instaladas las dependencias de testing:

```bash
pip install pytest pytest-django pytest-cov factory-boy
```

## Ejecutar Tests

### 1. Todos los tests
```bash
# Desde el directorio backend/
python -m pytest

# O usando Django
python manage.py test
```

### 2. Tests específicos por categoría

#### Tests unitarios
```bash
python -m pytest tests/test_unit/
```

#### Tests de integración
```bash
python -m pytest tests/test_integration/
```

#### Tests específicos por módulo
```bash
# Tests de modelos de turnos
python -m pytest tests/test_unit/test_turns_models.py

# Tests de vistas de turnos
python -m pytest tests/test_unit/test_turns_views.py

# Tests de lógica de negocio
python -m pytest tests/test_unit/test_turns_logic.py

# Tests de serializers
python -m pytest tests/test_unit/test_turns_serializers.py

# Tests de reportes
python -m pytest tests/test_unit/test_reports_views.py

# Tests de autenticación
python -m pytest tests/test_unit/test_users_auth.py
```

### 3. Tests con cobertura
```bash
# Generar reporte de cobertura
python -m pytest --cov=apps --cov-report=html

# Ver reporte en el navegador
# El reporte se genera en htmlcov/index.html
```

### 4. Tests en modo verbose
```bash
# Ver detalles de cada test
python -m pytest -v

# Ver output de print statements
python -m pytest -s
```

### 5. Tests específicos por nombre
```bash
# Ejecutar un test específico
python -m pytest tests/test_unit/test_turns_models.py::TurnoModelTest::test_crear_turno_basico

# Ejecutar tests que contengan una palabra
python -m pytest -k "turno"
```

## Usando la Extensión de Testing en VS Code

### 1. Instalar la extensión
- Instala "Python Test Explorer for Visual Studio Code"
- O usa la extensión integrada de Python que incluye testing

### 2. Configurar VS Code
Crea o actualiza `.vscode/settings.json`:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

### 3. Ejecutar tests desde VS Code

#### Usando la interfaz gráfica:
1. Abre la vista de "Testing" (icono de tubo de ensayo en la barra lateral)
2. VS Code detectará automáticamente los tests
3. Haz clic en el botón "play" junto a cualquier test para ejecutarlo
4. Usa el botón "debug" para ejecutar en modo debug

#### Usando comandos:
- `Ctrl+Shift+P` → "Python: Run All Tests"
- `Ctrl+Shift+P` → "Python: Run Current Test File"
- `Ctrl+Shift+P` → "Python: Debug All Tests"

### 4. Características útiles de VS Code:
- **Ejecución individual**: Haz clic en el icono "play" junto a cada test
- **Debug**: Coloca breakpoints y usa el icono "debug"
- **Resultados en tiempo real**: Ve los resultados directamente en el editor
- **Filtros**: Filtra tests por estado (pasados, fallidos, etc.)

## Configuración de Base de Datos para Tests

Los tests están configurados para usar SQLite en memoria por defecto, lo que los hace más rápidos. La configuración está en `conftest.py`.

Si necesitas usar PostgreSQL para tests específicos:

```python
# En tu test específico
@pytest.mark.django_db
def test_con_postgresql():
    # Tu test aquí
    pass
```

## Fixtures Disponibles

El archivo `conftest.py` proporciona fixtures útiles:

- `api_client`: Cliente API para tests
- `authenticated_user`: Usuario autenticado
- `empleado_user`: Usuario con perfil de empleado
- `admin_user`: Usuario administrador
- `sucursal_test`: Sucursal de prueba
- `servicio_test`: Servicio de prueba
- `turno_test`: Turno de prueba

### Ejemplo de uso:
```python
def test_ejemplo(api_client, authenticated_user, turno_test):
    api_client.force_authenticate(user=authenticated_user)
    response = api_client.get(f'/api/turnos/{turno_test.id}/')
    assert response.status_code == 200
```

## Mejores Prácticas

### 1. Nomenclatura de tests
```python
def test_[accion]_[condicion]_[resultado_esperado]():
    # Ejemplo:
    def test_crear_turno_usuario_autenticado_exitoso():
        pass
```

### 2. Estructura AAA (Arrange, Act, Assert)
```python
def test_ejemplo():
    # Arrange - Preparar datos
    usuario = Usuario.objects.create_user(...)
    
    # Act - Ejecutar acción
    response = client.post('/api/turnos/', data)
    
    # Assert - Verificar resultado
    assert response.status_code == 201
```

### 3. Usar mocks para dependencias externas
```python
from unittest.mock import patch

@patch('apps.turns.logic.GestorTurnos.crear_turno')
def test_con_mock(mock_crear):
    mock_crear.return_value = turno_mock
    # Tu test aquí
```

### 4. Tests independientes
- Cada test debe ser independiente
- No dependas del orden de ejecución
- Limpia datos después de cada test (Django lo hace automáticamente)

## Debugging Tests

### 1. Usar pdb
```python
def test_debug():
    import pdb; pdb.set_trace()
    # Tu código aquí
```

### 2. Usar pytest con pdb
```bash
python -m pytest --pdb
```

### 3. Ver output detallado
```bash
python -m pytest -s -v
```

## Integración Continua

Para CI/CD, usa este comando:
```bash
python -m pytest --cov=apps --cov-report=xml --junitxml=test-results.xml
```

## Troubleshooting

### Error: "No module named 'apps'"
```bash
# Asegúrate de estar en el directorio backend/
cd backend/
python -m pytest
```

### Error de base de datos
```bash
# Ejecuta las migraciones primero
python manage.py migrate
python -m pytest
```

### Tests lentos
```bash
# Usa SQLite en memoria (configurado por defecto)
# O ejecuta tests en paralelo
python -m pytest -n auto  # Requiere pytest-xdist
```

### Error de importación
```bash
# Verifica que el PYTHONPATH incluya el directorio backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m pytest
```

## Cobertura de Tests

### Generar reporte de cobertura
```bash
python -m pytest --cov=apps --cov-report=html --cov-report=term
```

### Ver reporte detallado
```bash
# Abrir reporte HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Configurar cobertura mínima
En `pytest.ini` o `setup.cfg`:
```ini
[tool:pytest]
addopts = --cov=apps --cov-fail-under=80
```

## Configuración Adicional

### pytest.ini
Crea un archivo `pytest.ini` en el directorio backend:
```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = digiturno.settings
python_files = tests.py test_*.py *_tests.py
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Configuración de VS Code para testing
En `.vscode/settings.json`:
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests",
        "--no-cov"
    ],
    "python.testing.autoTestDiscoverOnSaveEnabled": true,
    "python.testing.promptToConfigure": false
}
```

## Ejemplos de Tests Comunes

### Test de modelo
```python
def test_crear_usuario():
    usuario = Usuario.objects.create_user(
        username='test',
        email='test@example.com',
        password='testpass123'
    )
    assert usuario.username == 'test'
    assert usuario.email == 'test@example.com'
```

### Test de API
```python
def test_crear_turno_api(api_client, authenticated_user, servicio_test, sucursal_test):
    api_client.force_authenticate(user=authenticated_user)
    data = {
        'servicio': servicio_test.id,
        'sucursal': sucursal_test.id
    }
    response = api_client.post('/api/turnos/', data)
    assert response.status_code == 201
    assert 'numero_turno' in response.data
```

### Test con mock
```python
from unittest.mock import patch

@patch('apps.turns.logic.GestorTurnos.crear_turno')
def test_crear_turno_con_mock(mock_crear, api_client, authenticated_user):
    mock_turno = MagicMock()
    mock_turno.numero_turno = 'T001'
    mock_crear.return_value = mock_turno
    
    api_client.force_authenticate(user=authenticated_user)
    response = api_client.post('/api/turnos/', {})
    
    assert response.status_code == 201
    mock_crear.assert_called_once()
```

## Comandos Útiles

```bash
# Ejecutar solo tests que fallaron la última vez
python -m pytest --lf

# Ejecutar tests hasta el primer fallo
python -m pytest -x

# Ejecutar tests en paralelo (requiere pytest-xdist)
python -m pytest -n auto

# Ejecutar tests con tiempo de ejecución
python -m pytest --durations=10

# Ejecutar tests específicos por marca
python -m pytest -m "not slow"

# Generar reporte JUnit para CI
python -m pytest --junitxml=test-results.xml
```


