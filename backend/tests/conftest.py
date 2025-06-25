"""
Configuración global para los tests de Django con pytest
"""
import pytest
import os
import django
from django.conf import settings
from django.test.utils import get_runner


def pytest_configure():
    """Configuración inicial para pytest con Django"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiturno.settings')
    django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """Configuración de la base de datos para tests"""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'ATOMIC_REQUESTS': True,
        'TEST': {
            'ATOMIC_REQUESTS': True
        }
    }


@pytest.fixture
def api_client():
    """Cliente API para tests"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_user():
    """Usuario autenticado para tests"""
    from apps.users.models import Usuario
    return Usuario.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def empleado_user():
    """Usuario empleado para tests"""
    from apps.users.models import Usuario, Empleado
    from apps.core.models import Sucursal
    
    user = Usuario.objects.create_user(
        username='empleado',
        email='empleado@example.com',
        password='testpass123',
        first_name='Empleado',
        last_name='Test'
    )
    
    sucursal = Sucursal.objects.create(
        nombre='Sucursal Test',
        direccion='Calle Test 123',
        activa=True
    )
    
    empleado = Empleado.objects.create(
        usuario=user,
        codigo_empleado='EMP001',
        sucursal=sucursal,
        ventanilla_asignada='V1'
    )
    
    return user


@pytest.fixture
def admin_user():
    """Usuario administrador para tests"""
    from apps.users.models import Usuario, Administrador
    
    user = Usuario.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='testpass123',
        first_name='Admin',
        last_name='Test',
        is_staff=True
    )
    
    admin = Administrador.objects.create(
        usuario=user,
        nivel_acceso='admin'
    )
    
    return user


@pytest.fixture
def sucursal_test():
    """Sucursal de prueba"""
    from apps.core.models import Sucursal
    return Sucursal.objects.create(
        nombre='Sucursal Test',
        direccion='Calle Test 123',
        activa=True
    )


@pytest.fixture
def servicio_test(sucursal_test):
    """Servicio de prueba"""
    from apps.core.models import Servicio
    return Servicio.objects.create(
        nombre='Servicio Test',
        codigo_servicio='ST',
        sucursal=sucursal_test,
        tiempo_estimado_atencion=15,
        activo=True
    )


@pytest.fixture
def turno_test(authenticated_user, servicio_test, sucursal_test):
    """Turno de prueba"""
    from apps.turns.models import Turno
    return Turno.objects.create(
        numero_turno='T001',
        servicio=servicio_test,
        sucursal=sucursal_test,
        usuario=authenticated_user,
        estado=Turno.EstadoTurno.EN_ESPERA
    )


# Configuración para usar la base de datos en tests
pytest_plugins = ['pytest_django']
