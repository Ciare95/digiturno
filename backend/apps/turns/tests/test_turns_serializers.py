import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIRequestFactory

from apps.users.models.usuario import Usuario, Empleado
from apps.turns.models.turno import Turno, CalificacionServicio
from apps.core.models.core_model import Servicio, Sucursal
from apps.turns.serializers import (
    TurnoSerializer, CrearTurnoSerializer, CalificacionServicioSerializer,
    TransferirTurnoSerializer, ColaTurnosSerializer, EstadisticasEmpleadoSerializer
)


class TurnoSerializerTest(TestCase):
    """Tests para el serializer de Turno"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Crear sucursal
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        # Crear servicio asociado a sucursal
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
            password='testpass123',
            first_name='Empleado',
            last_name='Test'
        )
        
        self.empleado = Empleado.objects.create(
            usuario=self.empleado_user,
            codigo_empleado='EMP001',
            sucursal=self.sucursal,
            ventanilla_asignada='V1'
        )
        
        # Crear turno
        self.turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            empleado=self.empleado,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
    
    def test_serializer_campos_basicos(self):
        """Test para verificar los campos básicos del serializer"""
        serializer = TurnoSerializer(self.turno)
        data = serializer.data
        
        # Verificar campos principales
        self.assertEqual(data['numero_turno'], 'T001')
        self.assertEqual(data['servicio'], self.servicio.id)
        self.assertEqual(data['sucursal'], self.sucursal.id)
        self.assertEqual(data['usuario'], self.usuario.id)
        self.assertEqual(data['estado'], 'en_espera')
        
        # Verificar campos calculados
        self.assertEqual(data['servicio_nombre'], 'Servicio Test')
        self.assertEqual(data['sucursal_nombre'], 'Sucursal Test')
        self.assertEqual(data['usuario_nombre'], 'Test User')
        self.assertEqual(data['estado_display'], 'En Espera')
    
    def test_serializer_turno_sin_usuario(self):
        """Test para serializer con turno sin usuario"""
        turno_anonimo = Turno.objects.create(
            numero_turno='T002',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        serializer = TurnoSerializer(turno_anonimo)
        data = serializer.data
        
        self.assertIsNone(data['usuario'])
        self.assertIsNone(data['usuario_nombre'])
    
    def test_serializer_turno_sin_empleado(self):
        """Test para serializer con turno sin empleado asignado"""
        turno_sin_empleado = Turno.objects.create(
            numero_turno='T003',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        serializer = TurnoSerializer(turno_sin_empleado)
        data = serializer.data
        
        self.assertIsNone(data['empleado'])
        self.assertIsNone(data['empleado_nombre'])
    
    def test_serializer_campos_readonly(self):
        """Test para verificar que los campos readonly no se pueden modificar"""
        serializer = TurnoSerializer()
        readonly_fields = serializer.Meta.read_only_fields
        
        expected_readonly = [
            'numero_turno', 'fecha_creacion', 'fecha_atencion', 
            'fecha_finalizacion', 'empleado_nombre', 'usuario_nombre', 
            'servicio_nombre', 'sucursal_nombre', 'estado_display'
        ]
        
        for field in expected_readonly:
            self.assertIn(field, readonly_fields)


class CrearTurnoSerializerTest(TestCase):
    """Tests para el serializer de creación de turnos"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear sucursal
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        # Crear servicio asociado a sucursal
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            codigo_servicio='ST',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=15,
            activo=True
        )
        
        # Asociar servicio con sucursal (usando relación inversa)
        self.servicio.sucursal = self.sucursal
        self.servicio.save()
        
        # Crear usuario para el contexto
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear factory para request
        self.factory = APIRequestFactory()
    
    def test_validacion_datos_validos(self):
        """Test para validación con datos válidos"""
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': False
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CrearTurnoSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
    
    def test_validacion_servicio_no_en_sucursal(self):
        """Test para validación cuando servicio no está en sucursal"""
        # Crear otra sucursal y servicio asociado
        otra_sucursal = Sucursal.objects.create(
            nombre='Otra Sucursal',
            codigo_sucursal='SUC-002',  # Código único para la nueva sucursal
            direccion='Calle Otra 123',
            activa=True
        )
        
        otro_servicio = Servicio.objects.create(
            nombre='Otro Servicio',
            codigo_servicio='OS',
            sucursal=otra_sucursal,
            tiempo_estimado_atencion=20,
            activo=True
        )
        
        data = {
            'servicio': otro_servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': False
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CrearTurnoSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('servicio', serializer.errors)
    
    def test_validacion_turno_agendado_sin_fecha(self):
        """Test para validación de turno agendado sin fecha"""
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': True
            # Falta fecha_agendada
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CrearTurnoSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_agendada', serializer.errors)
    
    def test_validacion_fecha_agendada_pasada(self):
        """Test para validación de fecha agendada en el pasado"""
        fecha_pasada = timezone.now() - timedelta(days=1)
        
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': True,
            'fecha_agendada': fecha_pasada
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CrearTurnoSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_agendada', serializer.errors)
    
    def test_validacion_fecha_agendada_futura(self):
        """Test para validación de fecha agendada futura válida"""
        fecha_futura = timezone.now() + timedelta(days=1)
        
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': True,
            'fecha_agendada': fecha_futura
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CrearTurnoSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())


class CalificacionServicioSerializerTest(TestCase):
    """Tests para el serializer de CalificacionServicio"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Crear empleado
        self.empleado_user = Usuario.objects.create_user(
            username='empleado_test',
            email='empleado@test.com',
            password='testpass123',
            first_name='Empleado',
            last_name='Test'
        )
        
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        self.empleado = Empleado.objects.create(
            usuario=self.empleado_user,
            codigo_empleado='EMP001',
            sucursal=self.sucursal,
            ventanilla_asignada='V1'
        )
        
        # Crear servicio asociado a sucursal
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            codigo_servicio='ST',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=15,
            activo=True
        )
        
        # Crear turno finalizado
        self.turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            empleado=self.empleado,
            estado=Turno.EstadoTurno.FINALIZADO
        )
        
        # Crear factory para request
        self.factory = APIRequestFactory()
    
    def test_serializer_campos_basicos(self):
        """Test para verificar los campos básicos del serializer"""
        calificacion = CalificacionServicio.objects.create(
            turno=self.turno,
            usuario=self.usuario,
            empleado=self.empleado,
            servicio=self.servicio,
            calificacion=5,
            comentario='Excelente servicio'
        )
        
        serializer = CalificacionServicioSerializer(calificacion)
        data = serializer.data
        
        # Verificar campos principales
        self.assertEqual(data['calificacion'], 5)
        self.assertEqual(data['comentario'], 'Excelente servicio')
        self.assertEqual(data['turno_numero'], 'T001')
        self.assertEqual(data['servicio_nombre'], 'Servicio Test')
        self.assertEqual(data['empleado_nombre'], 'Empleado Test')
        self.assertEqual(data['usuario_nombre'], 'Test User')
    
    def test_validacion_calificacion_valida(self):
        """Test para validación de calificación válida"""
        data = {
            'turno': self.turno.id,
            'servicio': self.servicio.id,
            'empleado': self.empleado.usuario.id,
            'calificacion': 4,
            'comentario': 'Buen servicio'
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CalificacionServicioSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
    
    def test_validacion_calificacion_fuera_rango(self):
        """Test para validación de calificación fuera de rango"""
        data = {
            'turno': self.turno.id,
            'servicio': self.servicio.id,
            'empleado': self.empleado.usuario.id,
            'calificacion': 6  # Fuera del rango 1-5
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CalificacionServicioSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('calificacion', serializer.errors)
    
    def test_validacion_turno_no_finalizado(self):
        """Test para validación de turno no finalizado"""
        # Crear turno en espera
        turno_en_espera = Turno.objects.create(
            numero_turno='T002',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        data = {
            'turno': turno_en_espera.id,
            'servicio': self.servicio.id,
            'empleado': self.empleado.usuario.id,
            'calificacion': 5
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CalificacionServicioSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('turno', serializer.errors)
    
    def test_validacion_calificacion_duplicada(self):
        """Test para validación de calificación duplicada"""
        # Crear primera calificación
        CalificacionServicio.objects.create(
            turno=self.turno,
            usuario=self.usuario,
            empleado=self.empleado,
            servicio=self.servicio,
            calificacion=4
        )
        
        data = {
            'turno': self.turno.id,
            'servicio': self.servicio.id,
            'empleado': self.empleado.usuario.id,
            'calificacion': 5
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CalificacionServicioSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('turno', serializer.errors)
    
    def test_validacion_servicio_no_corresponde(self):
        """Test para validación cuando servicio no corresponde al turno"""
        # Crear otro servicio
        otro_servicio = Servicio.objects.create(
            nombre='Otro Servicio',
            codigo_servicio='OS',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=20,
            activo=True
        )
        
        data = {
            'turno': self.turno.id,
            'servicio': otro_servicio.id,  # Servicio diferente al del turno
            'empleado': self.empleado.usuario.id,
            'calificacion': 5
        }
        
        request = self.factory.post('/')
        request.user = self.usuario
        
        serializer = CalificacionServicioSerializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('servicio', serializer.errors)


class TransferirTurnoSerializerTest(TestCase):
    """Tests para el serializer de transferencia de turnos"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear sucursal para los servicios
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        # Crear servicios asociados a sucursal
        self.servicio1 = Servicio.objects.create(
            nombre='Servicio 1',
            codigo_servicio='S1',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=15,
            activo=True
        )
        
        self.servicio2 = Servicio.objects.create(
            nombre='Servicio 2',
            codigo_servicio='S2',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=20,
            activo=True
        )
    
    def test_validacion_servicio_valido(self):
        """Test para validación con servicio válido"""
        data = {
            'nuevo_servicio_id': self.servicio2.id
        }
        
        serializer = TransferirTurnoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_validacion_servicio_inexistente(self):
        """Test para validación con servicio inexistente"""
        data = {
            'nuevo_servicio_id': 999  # ID inexistente
        }
        
        serializer = TransferirTurnoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nuevo_servicio_id', serializer.errors)
    
    def test_validacion_servicio_inactivo(self):
        """Test para validación con servicio inactivo"""
        servicio_inactivo = Servicio.objects.create(
            nombre='Servicio Inactivo',
            codigo_servicio='SI',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=15,
            activo=False
        )
        
        data = {
            'nuevo_servicio_id': servicio_inactivo.id
        }
        
        serializer = TransferirTurnoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nuevo_servicio_id', serializer.errors)


class EstadisticasEmpleadoSerializerTest(TestCase):
    """Tests para el serializer de estadísticas del empleado"""
    
    def test_serializer_estructura_completa(self):
        """Test para verificar la estructura completa del serializer"""
        data = {
            'turnos_atendidos_hoy': 5,
            'turnos_atendidos_semana': 25,
            'turnos_atendidos_mes': 100,
            'tiempo_promedio_atencion': timedelta(minutes=15),
            'calificacion_promedio': 4.5,
            'turnos_transferidos': 3,
            'cantidad_calificaciones': 20,
            'distribucion_calificaciones': {
                '1': 1,
                '2': 2,
                '3': 5,
                '4': 7,
                '5': 5
            }
        }
        
        serializer = EstadisticasEmpleadoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Verificar que todos los campos están presentes
        expected_fields = [
            'turnos_atendidos_hoy', 'turnos_atendidos_semana', 'turnos_atendidos_mes',
            'tiempo_promedio_atencion', 'calificacion_promedio', 'turnos_transferidos',
            'cantidad_calificaciones', 'distribucion_calificaciones'
        ]
        
        for field in expected_fields:
            self.assertIn(field, serializer.validated_data)
    
    def test_serializer_distribucion_calificaciones(self):
        """Test para verificar el campo de distribución de calificaciones"""
        data = {
            'turnos_atendidos_hoy': 0,
            'turnos_atendidos_semana': 0,
            'turnos_atendidos_mes': 0,
            'tiempo_promedio_atencion': timedelta(0),
            'calificacion_promedio': 0.0,
            'turnos_transferidos': 0,
            'cantidad_calificaciones': 0,
            'distribucion_calificaciones': {
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0
            }
        }
        
        serializer = EstadisticasEmpleadoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Verificar que la distribución es un diccionario con enteros
        distribucion = serializer.validated_data['distribucion_calificaciones']
        self.assertIsInstance(distribucion, dict)
        
        for key, value in distribucion.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, int)
    
    def test_serializer_tiempo_promedio_atencion(self):
        """Test para verificar el campo de tiempo promedio de atención"""
        tiempo_15_min = timedelta(minutes=15)
        
        data = {
            'turnos_atendidos_hoy': 1,
            'turnos_atendidos_semana': 1,
            'turnos_atendidos_mes': 1,
            'tiempo_promedio_atencion': tiempo_15_min,
            'calificacion_promedio': 5.0,
            'turnos_transferidos': 0,
            'cantidad_calificaciones': 1,
            'distribucion_calificaciones': {'5': 1}
        }
        
        serializer = EstadisticasEmpleadoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Verificar que el tiempo se maneja correctamente
        tiempo_validado = serializer.validated_data['tiempo_promedio_atencion']
        self.assertEqual(tiempo_validado, tiempo_15_min)
        self.assertEqual(tiempo_validado.total_seconds(), 900)  # 15 minutos = 900 segundos
