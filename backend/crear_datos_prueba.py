import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digiturno.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.core.models import Sucursal, Servicio
from apps.users.models import Empleado, Administrador 
from apps.turns.models import Turno, CalificacionServicio, ColaTurnos

Usuario = get_user_model()

def crear_usuarios():
    # Usuario normal
    usuario_normal, created = Usuario.objects.get_or_create(
        username='usuario1',
        defaults={
            'email': 'usuario1@example.com',
            'first_name': 'Usuario',
            'last_name': 'Normal',
            'cedula': '123456789'
        }
    )
    if created:
        usuario_normal.set_password('password123')
        usuario_normal.save()
        print(f'Usuario normal creado: {usuario_normal.username}')

    # Empleado
    usuario_empleado, created = Usuario.objects.get_or_create(
        username='empleado1',
        defaults={
            'email': 'empleado1@example.com',
            'first_name': 'Empleado',
            'last_name': 'Uno',
            'cedula': '987654321'
        }
    )
    if created:
        usuario_empleado.set_password('password123')
        usuario_empleado.save()
    
    empleado, _ = Empleado.objects.get_or_create(
        usuario=usuario_empleado,
        defaults={
            'codigo_empleado': 'EMP001',
            'ventanilla_asignada': 'V1',
            'estado_conexion': 'conectado'
        }
    )
    print(f'Empleado creado/actualizado: {empleado.codigo_empleado}')

    # Administrador
    usuario_admin, created = Usuario.objects.get_or_create(
        username='admin1',
        defaults={
            'email': 'admin1@example.com',
            'first_name': 'Admin',
            'last_name': 'Uno',
            'cedula': '456789123',
            'is_staff': True
        }
    )
    if created:
        usuario_admin.set_password('password123')
        usuario_admin.save()
    
    admin, _ = Administrador.objects.get_or_create(
        usuario=usuario_admin,
        defaults={
            'nivel_acceso': 'super_admin'
        }
    )
    print(f'Administrador creado/actualizado: {admin.usuario.username}')

    return usuario_normal, empleado, admin

def crear_infraestructura():
    # Crear sucursal
    sucursal, created = Sucursal.objects.get_or_create(
        codigo_sucursal='SUC-001',
        defaults={
            'nombre': 'Sucursal Principal',
            'direccion': 'Calle Principal 123',
            'telefono': '555-1234',
            'ciudad': 'Bogotá',
            'departamento': 'Cundinamarca',
            'activa': True
        }
    )
    if created:
        print(f'Sucursal creada: {sucursal.nombre}')

    # Crear servicios
    servicios = [
        {
            'nombre': 'Atención al Cliente',
            'codigo_servicio': 'SERV-001',
            'tiempo_estimado_atencion': 15
        },
        {
            'nombre': 'Pagos y Facturación',
            'codigo_servicio': 'SERV-002',
            'tiempo_estimado_atencion': 10
        },
        {
            'nombre': 'Soporte Técnico',
            'codigo_servicio': 'SERV-003',
            'tiempo_estimado_atencion': 20
        }
    ]

    servicios_creados = []
    for serv_data in servicios:
        servicio, created = Servicio.objects.get_or_create(
            codigo_servicio=serv_data['codigo_servicio'],
            defaults={
                'nombre': serv_data['nombre'],
                'sucursal': sucursal,
                'tiempo_estimado_atencion': serv_data['tiempo_estimado_atencion']
            }
        )
        servicios_creados.append(servicio)
        if created:
            print(f'Servicio creado: {servicio.nombre}')

    return sucursal, servicios_creados

def crear_turnos(usuario_normal, empleado, servicios):
    estados = ['en_espera', 'llamado', 'en_atencion', 'finalizado']
    turnos_creados = []

    for i, estado in enumerate(estados):
        turno = Turno.objects.create(
            numero_turno=f'T{i+1:03d}',
            servicio=servicios[i % len(servicios)],
            sucursal=servicios[0].sucursal,
            usuario=usuario_normal,
            empleado=empleado if estado in ['en_atencion', 'finalizado'] else None,
            estado=estado,
            fecha_creacion=timezone.now() - timedelta(hours=i)
        )
        
        if estado == 'finalizado':
            turno.fecha_llamado = turno.fecha_creacion + timedelta(minutes=5)
            turno.fecha_inicio_atencion = turno.fecha_llamado + timedelta(minutes=2)
            turno.fecha_finalizacion = turno.fecha_inicio_atencion + timedelta(minutes=15)
            turno.save()
            
            # Modificar la creación de CalificacionServicio
            CalificacionServicio.objects.create(
                turno=turno,
                usuario=usuario_normal,
                empleado=empleado,  # Usar el empleado relacionado al usuario
                servicio=turno.servicio,
                calificacion=4,
                comentario='Buen servicio'
            )

        if estado in ['en_espera', 'llamado']:
            ColaTurnos.objects.create(
                turno=turno,
                servicio=turno.servicio,
                posicion_cola=i+1,
                tiempo_espera_estimado=15
            )

        turnos_creados.append(turno)
        print(f'Turno creado: {turno.numero_turno} - Estado: {estado}')

    return turnos_creados

if __name__ == '__main__':
    print("Creando datos de prueba...")
    
    # Crear usuarios
    usuario_normal, empleado, admin = crear_usuarios()
    
    # Crear infraestructura
    sucursal, servicios = crear_infraestructura()
    
    # Crear turnos
    turnos = crear_turnos(usuario_normal, empleado, servicios)
    
    print("\nDatos de prueba creados exitosamente!")
    print("\nCredenciales para pruebas:")
    print("Usuario normal:")
    print("  Username: usuario1")
    print("  Password: password123")
    print("\nEmpleado:")
    print("  Username: empleado1")
    print("  Password: password123")
    print("\nAdministrador:")
    print("  Username: admin1")
    print("  Password: password123")