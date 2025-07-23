import pytest
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.users.models.usuario import Usuario
from apps.users.models.empleado import Empleado
from apps.users.models.administrador import Administrador
from apps.turns.models.turno import Turno
from apps.turns.models.calificacion_servicio import CalificacionServicio
from apps.core.models.servicio import Servicio
from apps.core.models.sucursal import Sucursal
from apps.reports.views.report_view import ReporteAvanzadoView
from apps.reports.serializers.report_serializer import ReporteAvanzadoSerializer, DashboardAdminSerializer

User = get_user_model()


class ReporteAvanzadoViewTest(TestCase):
    """Tests para la vista de reportes avanzados"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario administrador
        self.admin_user = Usuario.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='Test',
            is_staff=True
        )
        
        # Crear perfil de administrador
        self.admin_profile = Administrador.objects.create(
            usuario=self.admin_user,
            nivel_acceso='admin'
        )
        
        # Crear usuario normal
        self.normal_user = Usuario.objects.create_user(
            username='user_test',
            email='user@test.com',
            password='testpass123'
        )
        
        # Crear sucursal y servicio para los tests
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            codigo_servicio='ST',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=15,
            activo=True
        )
        
        # Crear empleado
        self.empleado_user = Usuario.objects.create_user(
            username='empleado_test',
            email='empleado@test.com',
            password='testpass123'
        )
        
        self.empleado = Empleado.objects.create(
            usuario=self.empleado_user,
            codigo_empleado='EMP001',
            sucursal=self.sucursal,
            ventanilla_asignada='V1'
        )
        
        # URL del endpoint
        self.url = reverse('reportes_avanzados')
    
    def test_acceso_sin_autenticacion(self):
        """Test que verifica que se requiere autenticación"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_acceso_usuario_normal_denegado(self):
        """Test que verifica que usuarios normales no pueden acceder"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_acceso_administrador_permitido(self):
        """Test que verifica que administradores pueden acceder"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_reporte_estructura_basica(self):
        """Test que verifica la estructura básica del reporte"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Verificar que contiene las secciones principales
        expected_keys = [
            'periodo',
            'metricas_generales',
            'metricas_servicios',
            'metricas_empleados',
            'satisfaccion',
            'tendencias',
            'comparativa_sucursales'
        ]
        
        for key in expected_keys:
            self.assertIn(key, data)
    
    def test_reporte_con_datos_turnos(self):
        """Test que verifica el reporte con datos de turnos"""
        # Crear algunos turnos de prueba
        turno1 = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.normal_user,
            empleado=self.empleado,
            estado=Turno.EstadoTurno.FINALIZADO,
            fecha_creacion=timezone.now() - timedelta(days=1),
            fecha_inicio_atencion=timezone.now() - timedelta(days=1, hours=1),
            fecha_finalizacion=timezone.now() - timedelta(days=1, minutes=45)
        )
        
        turno2 = Turno.objects.create(
            numero_turno='T002',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.CANCELADO,
            fecha_creacion=timezone.now() - timedelta(days=2)
        )
        
        # Crear calificación
        CalificacionServicio.objects.create(
            turno=turno1,
            usuario=self.normal_user,
            empleado=self.empleado,
            servicio=self.servicio,
            calificacion=5,
            comentario='Excelente servicio'
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Verificar métricas generales
        metricas = data['metricas_generales']
        self.assertEqual(metricas['total_turnos'], 2)
        self.assertEqual(metricas['turnos_completados'], 1)
        self.assertEqual(metricas['turnos_cancelados'], 1)
        
        # Verificar satisfacción
        satisfaccion = data['satisfaccion']
        self.assertEqual(satisfaccion['promedio_satisfaccion'], 5.0)
        self.assertEqual(satisfaccion['total_calificaciones'], 1)
    
    def test_reporte_con_fechas_personalizadas(self):
        """Test que verifica el reporte con rango de fechas personalizado"""
        fecha_inicio = (timezone.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        fecha_fin = timezone.now().strftime('%Y-%m-%d')
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url, {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Verificar que el período se estableció correctamente
        periodo = data['periodo']
        self.assertEqual(periodo['fecha_inicio'], fecha_inicio)
        self.assertEqual(periodo['fecha_fin'], fecha_fin)
        self.assertEqual(periodo['dias_totales'], 7)
    
    def test_reporte_formato_fecha_invalido(self):
        """Test que verifica el manejo de formatos de fecha inválidos"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url, {
            'fecha_inicio': 'fecha-invalida',
            'fecha_fin': '2023-13-45'  # Fecha inválida
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn('error', data)
        self.assertIn('formato de fecha', data['error'])
    
    def test_metricas_servicios_estructura(self):
        """Test que verifica la estructura de métricas de servicios"""
        # Crear turno para tener datos
        Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.FINALIZADO,
            fecha_creacion=timezone.now() - timedelta(days=1),
            fecha_inicio_atencion=timezone.now() - timedelta(days=1, hours=1),
            fecha_finalizacion=timezone.now() - timedelta(days=1, minutes=45)
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        
        data = response.json()
        metricas_servicios = data['metricas_servicios']
        
        self.assertIsInstance(metricas_servicios, list)
        if metricas_servicios:  # Si hay datos
            servicio_data = metricas_servicios[0]
            expected_keys = ['servicio', 'total_turnos', 'tiempo_promedio_atencion']
            for key in expected_keys:
                self.assertIn(key, servicio_data)
    
    def test_metricas_empleados_estructura(self):
        """Test que verifica la estructura de métricas de empleados"""
        # Crear turno atendido por empleado
        Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            empleado=self.empleado,
            estado=Turno.EstadoTurno.FINALIZADO,
            fecha_creacion=timezone.now() - timedelta(days=1),
            fecha_inicio_atencion=timezone.now() - timedelta(days=1, hours=1),
            fecha_finalizacion=timezone.now() - timedelta(days=1, minutes=45)
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        
        data = response.json()
        metricas_empleados = data['metricas_empleados']
        
        self.assertIsInstance(metricas_empleados, list)
        if metricas_empleados:  # Si hay datos
            empleado_data = metricas_empleados[0]
            expected_keys = ['empleado', 'codigo', 'turnos_atendidos', 'tiempo_promedio_atencion']
            for key in expected_keys:
                self.assertIn(key, empleado_data)


class ReporteAvanzadoSerializerTest(TestCase):
    """Tests para el serializer de reportes avanzados"""
    
    def test_serializer_campos_opcionales(self):
        """Test que verifica que los campos de fecha son opcionales"""
        from apps.reports.serializers import ReporteAvanzadoSerializer
        
        # Test sin fechas
        serializer = ReporteAvanzadoSerializer(data={})
        self.assertTrue(serializer.is_valid())
        
        # Test con fechas válidas
        data = {
            'fecha_inicio': '2023-01-01',
            'fecha_fin': '2023-12-31'
        }
        serializer = ReporteAvanzadoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_dashboard_admin_serializer_estructura(self):
        """Test que verifica la estructura del DashboardAdminSerializer"""
        from apps.reports.serializers import DashboardAdminSerializer
        
        # Datos de ejemplo
        data = {
            'total_usuarios': 100,
            'total_empleados': 10,
            'total_servicios_activos': 5,
            'total_sucursales_activas': 3,
            'turnos_hoy': 50,
            'turnos_en_espera': 10,
            'turnos_en_atencion': 5,
            'turnos_finalizados': 30,
            'turnos_cancelados': 5,
            'tiempo_espera_promedio': timedelta(minutes=15),
            'servicios_mas_demandados': [
                {'nombre': 'Servicio 1', 'total': '25'}
            ],
            'calificacion_promedio_general': 4.5,
            'total_calificaciones': 100,
            'distribucion_calificaciones': {
                '1': 5, '2': 10, '3': 15, '4': 30, '5': 40
            },
            'rendimiento_sucursales': [
                {'sucursal': {'nombre': 'Sucursal 1', 'total_turnos': '50'}}
            ]
        }
        
        serializer = DashboardAdminSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
