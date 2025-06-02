import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiturno.settings')
django.setup()

from apps.core.models import Sucursal, Servicio

# Crear sucursal
try:
    sucursal = Sucursal.objects.create(
        nombre='Sucursal Principal',
        codigo_sucursal='SUC-001',
        direccion='Calle Principal 123',
        telefono='555-1234',
        ciudad='Bogotá',
        departamento='Cundinamarca',
        activa=True
    )
    print(f'Sucursal creada: {sucursal.nombre}')

except Exception as e:
    print(f'Error creando sucursal: {e}')

# Crear servicio
try:
    servicio = Servicio.objects.create(
        nombre='Servicio al Cliente',
        codigo_servicio='SERV-001',
        sucursal=sucursal,
        tiempo_estimado_atencion=15
    )
    print(f'Servicio creado: {servicio.nombre}')

except Exception as e:
    print(f'Error creando servicio: {e}')
