import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from apps.users.models.usuario import Usuario
from apps.users.models.empleado import Empleado
from apps.turns.models.turno import Turno
from apps.turns.models.calificacion_servicio import CalificacionServicio
from apps.turns.models.cola_turnos import ColaTurnos
from apps.turns.models.notificacion import Notificacion
from apps.turns.models.estadistica_empleado import EstadisticaEmpleado
from apps.core.models.servicio import Servicio
from apps.core.models.sucursal import Sucursal


class TurnoModelTest(TestCase):
    """Tests para el modelo Turno"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear sucursal
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        # Crear servicio
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
            codigo_empleado=f'EMP{hash(self.id()) % 10000:04d}',
            sucursal=self.sucursal,
            ventanilla_asignada='V1'
        )
    
    def test_crear_turno_basico(self):
        """Test para crear un turno básico"""
        turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario
        )
        
        self.assertEqual(turno.numero_turno, 'T001')
        self.assertEqual(turno.servicio, self.servicio)
        self.assertEqual(turno.sucursal, self.sucursal)
        self.assertEqual(turno.usuario, self.usuario)
        self.assertEqual(turno.estado, Turno.EstadoTurno.EN_ESPERA)
        self.assertIsNotNone(turno.fecha_creacion)
    
    def test_turno_sin_usuario(self):
        """Test para crear un turno sin usuario (turno anónimo)"""
        turno = Turno.objects.create(
            numero_turno='T002',
            servicio=self.servicio,
            sucursal=self.sucursal
        )
        
        self.assertIsNone(turno.usuario)
        self.assertEqual(turno.estado, Turno.EstadoTurno.EN_ESPERA)
    
    def test_turno_agendado(self):
        """Test para crear un turno agendado"""
        fecha_agendada = timezone.now() + timedelta(days=1)
        
        turno = Turno.objects.create(
            numero_turno='T003',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            es_agendado=True,
            fecha_agendada=fecha_agendada
        )
        
        self.assertTrue(turno.es_agendado)
        self.assertEqual(turno.fecha_agendada, fecha_agendada)
    
    def test_asignar_empleado_turno(self):
        """Test para asignar un empleado a un turno"""
        turno = Turno.objects.create(
            numero_turno='T004',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario
        )
        
        # Asignar empleado y cambiar estado
        turno.empleado = self.empleado
        turno.estado = Turno.EstadoTurno.EN_ATENCION
        turno.fecha_inicio_atencion = timezone.now()
        turno.save()
        
        self.assertEqual(turno.empleado, self.empleado)
        self.assertEqual(turno.estado, Turno.EstadoTurno.EN_ATENCION)
        self.assertIsNotNone(turno.fecha_inicio_atencion)
    
    def test_finalizar_turno(self):
        """Test para finalizar un turno"""
        turno = Turno.objects.create(
            numero_turno='T005',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            empleado=self.empleado,
            estado=Turno.EstadoTurno.EN_ATENCION,
            fecha_inicio_atencion=timezone.now() - timedelta(minutes=30)
        )
        
        # Finalizar turno
        turno.estado = Turno.EstadoTurno.FINALIZADO
        turno.fecha_finalizacion = timezone.now()
        turno.save()
        
        self.assertEqual(turno.estado, Turno.EstadoTurno.FINALIZADO)
        self.assertIsNotNone(turno.fecha_finalizacion)
    
    def test_turno_str_representation(self):
        """Test para la representación string del turno"""
        turno = Turno.objects.create(
            numero_turno='T006',
            servicio=self.servicio,
            sucursal=self.sucursal
        )
        
        expected_str = f"Turno T006 - {self.servicio.nombre}"
        self.assertEqual(str(turno), expected_str)
    
    def test_estados_turno_choices(self):
        """Test para verificar las opciones de estado del turno"""
        estados_esperados = [
            'en_espera', 'llamado', 'en_atencion', 
            'finalizado', 'cancelado', 'ausente'
        ]
        
        estados_disponibles = [choice[0] for choice in Turno.EstadoTurno.choices]
        
        for estado in estados_esperados:
            self.assertIn(estado, estados_disponibles)


class CalificacionServicioModelTest(TestCase):
    """Tests para el modelo CalificacionServicio"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear sucursal
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        # Crear servicio
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
            codigo_empleado=f'EMP{hash(self.id()) % 10000:04d}',
            sucursal=self.sucursal,
            ventanilla_asignada='V1'
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
    
    def test_crear_calificacion_basica(self):
        """Test para crear una calificación básica"""
        calificacion = CalificacionServicio.objects.create(
            turno=self.turno,
            usuario=self.usuario,
            empleado=self.empleado,
            servicio=self.servicio,
            calificacion=5,
            comentario='Excelente servicio'
        )
        
        self.assertEqual(calificacion.turno, self.turno)
        self.assertEqual(calificacion.usuario, self.usuario)
        self.assertEqual(calificacion.empleado, self.empleado)
        self.assertEqual(calificacion.servicio, self.servicio)
        self.assertEqual(calificacion.calificacion, 5)
        self.assertEqual(calificacion.comentario, 'Excelente servicio')
        self.assertIsNotNone(calificacion.fecha_calificacion)
    
    def test_calificacion_con_aspectos_evaluados(self):
        """Test para crear una calificación con aspectos evaluados"""
        aspectos = {
            'amabilidad': 5,
            'rapidez': 4,
            'conocimiento': 5,
            'resolucion': 4
        }
        
        calificacion = CalificacionServicio.objects.create(
            turno=self.turno,
            usuario=self.usuario,
            empleado=self.empleado,
            servicio=self.servicio,
            calificacion=4,
            aspectos_evaluados=aspectos
        )
        
        self.assertEqual(calificacion.aspectos_evaluados, aspectos)
        self.assertEqual(calificacion.aspectos_evaluados['amabilidad'], 5)
    
    def test_calificacion_str_representation(self):
        """Test para la representación string de la calificación"""
        calificacion = CalificacionServicio.objects.create(
            turno=self.turno,
            usuario=self.usuario,
            empleado=self.empleado,
            servicio=self.servicio,
            calificacion=3
        )
        
        expected_str = f"Calificación 3 - Turno {self.turno.numero_turno}"
        self.assertEqual(str(calificacion), expected_str)


class ColaTurnosModelTest(TestCase):
    """Tests para el modelo ColaTurnos"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear sucursal
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        # Crear servicio
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            codigo_servicio='ST',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=15,
            activo=True
        )
        
        # Crear turno
        self.turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal
        )
    
    def test_crear_entrada_cola(self):
        """Test para crear una entrada en la cola"""
        cola = ColaTurnos.objects.create(
            turno=self.turno,
            servicio=self.servicio,
            posicion_cola=1,
            tiempo_espera_estimado=15
        )
        
        self.assertEqual(cola.turno, self.turno)
        self.assertEqual(cola.servicio, self.servicio)
        self.assertEqual(cola.posicion_cola, 1)
        self.assertEqual(cola.tiempo_espera_estimado, 15)
        self.assertTrue(cola.activo)
        self.assertIsNotNone(cola.fecha_ingreso_cola)
    
    def test_desactivar_entrada_cola(self):
        """Test para desactivar una entrada en la cola"""
        cola = ColaTurnos.objects.create(
            turno=self.turno,
            servicio=self.servicio,
            posicion_cola=1
        )
        
        # Desactivar entrada
        cola.activo = False
        cola.save()
        
        self.assertFalse(cola.activo)
    
    def test_cola_str_representation(self):
        """Test para la representación string de la cola"""
        cola = ColaTurnos.objects.create(
            turno=self.turno,
            servicio=self.servicio,
            posicion_cola=3
        )
        
        expected_str = f"Posición 3 - {self.turno.numero_turno}"
        self.assertEqual(str(cola), expected_str)


class NotificacionModelTest(TestCase):
    """Tests para el modelo Notificacion"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear sucursal y servicio
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
        
        # Crear turno
        self.turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario
        )
    
    def test_crear_notificacion_basica(self):
        """Test para crear una notificación básica"""
        notificacion = Notificacion.objects.create(
            usuario=self.usuario,
            turno=self.turno,
            tipo='llamado_turno',
            titulo='Su turno ha sido llamado',
            mensaje='Por favor diríjase a la ventanilla 1'
        )
        
        self.assertEqual(notificacion.usuario, self.usuario)
        self.assertEqual(notificacion.turno, self.turno)
        self.assertEqual(notificacion.tipo, 'llamado_turno')
        self.assertEqual(notificacion.titulo, 'Su turno ha sido llamado')
        self.assertFalse(notificacion.leida)
        self.assertEqual(notificacion.canal, 'websocket')
        self.assertIsNotNone(notificacion.fecha_envio)
    
    def test_marcar_notificacion_como_leida(self):
        """Test para marcar una notificación como leída"""
        notificacion = Notificacion.objects.create(
            usuario=self.usuario,
            tipo='sistema',
            titulo='Notificación de prueba',
            mensaje='Mensaje de prueba'
        )
        
        # Marcar como leída
        notificacion.leida = True
        notificacion.fecha_lectura = timezone.now()
        notificacion.save()
        
        self.assertTrue(notificacion.leida)
        self.assertIsNotNone(notificacion.fecha_lectura)
    
    def test_notificacion_tipos_disponibles(self):
        """Test para verificar los tipos de notificación disponibles"""
        tipos_esperados = [
            'llamado_turno', 'turno_finalizado', 'turno_cancelado',
            'turno_transferido', 'sistema'
        ]
        
        tipos_disponibles = [choice[0] for choice in Notificacion.TIPOS_NOTIFICACION]
        
        for tipo in tipos_esperados:
            self.assertIn(tipo, tipos_disponibles)
    
    def test_notificacion_canales_disponibles(self):
        """Test para verificar los canales de notificación disponibles"""
        canales_esperados = ['websocket', 'email', 'sms', 'push']
        
        canales_disponibles = [choice[0] for choice in Notificacion.CANALES_NOTIFICACION]
        
        for canal in canales_esperados:
            self.assertIn(canal, canales_disponibles)
    
    def test_notificacion_str_representation(self):
        """Test para la representación string de la notificación"""
        notificacion = Notificacion.objects.create(
            usuario=self.usuario,
            tipo='llamado_turno',
            titulo='Turno llamado',
            mensaje='Su turno ha sido llamado'
        )
        
        expected_str = "Turno llamado (Llamado de turno)"
        self.assertEqual(str(notificacion), expected_str)


class EstadisticaEmpleadoModelTest(TestCase):
    """Tests para el modelo EstadisticaEmpleado"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario empleado
        self.empleado_user = Usuario.objects.create_user(
            username='empleado_test',
            email='empleado@test.com',
            password='testpass123'
        )
        
        # Crear sucursal
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Calle Test 123',
            activa=True
        )
        
        # Crear empleado
        self.empleado = Empleado.objects.create(
            usuario=self.empleado_user,
            codigo_empleado=f'EMP{hash(self.id()) % 10000:04d}',
            sucursal=self.sucursal,
            ventanilla_asignada='V1'
        )
    
    def test_crear_estadistica_empleado(self):
        """Test para crear estadísticas de empleado"""
        fecha_hoy = timezone.now().date()
        
        estadistica = EstadisticaEmpleado.objects.create(
            empleado=self.empleado,
            fecha=fecha_hoy,
            turnos_atendidos=10,
            tiempo_promedio_atencion=15,
            calificacion_promedio=4.5,
            tiempo_conectado=480,  # 8 horas en minutos
            turnos_transferidos=2
        )
        
        self.assertEqual(estadistica.empleado, self.empleado)
        self.assertEqual(estadistica.fecha, fecha_hoy)
        self.assertEqual(estadistica.turnos_atendidos, 10)
        self.assertEqual(estadistica.tiempo_promedio_atencion, 15)
        self.assertEqual(float(estadistica.calificacion_promedio), 4.5)
        self.assertEqual(estadistica.tiempo_conectado, 480)
        self.assertEqual(estadistica.turnos_transferidos, 2)
    
    def test_estadistica_empleado_unique_constraint(self):
        """Test para verificar la restricción única por empleado y fecha"""
        fecha_hoy = timezone.now().date()
        
        # Crear primera estadística
        EstadisticaEmpleado.objects.create(
            empleado=self.empleado,
            fecha=fecha_hoy,
            turnos_atendidos=5
        )
        
        # Intentar crear otra estadística para el mismo empleado y fecha
        with self.assertRaises(Exception):  # Debería lanzar IntegrityError
            EstadisticaEmpleado.objects.create(
                empleado=self.empleado,
                fecha=fecha_hoy,
                turnos_atendidos=10
            )
    
    def test_estadistica_empleado_str_representation(self):
        """Test para la representación string de la estadística"""
        fecha_hoy = timezone.now().date()
        
        estadistica = EstadisticaEmpleado.objects.create(
            empleado=self.empleado,
            fecha=fecha_hoy
        )
        
        expected_str = f"Estadísticas {self.empleado} - {fecha_hoy}"
        self.assertEqual(str(estadistica), expected_str)
    
    def test_valores_por_defecto(self):
        """Test para verificar los valores por defecto"""
        fecha_hoy = timezone.now().date()
        
        estadistica = EstadisticaEmpleado.objects.create(
            empleado=self.empleado,
            fecha=fecha_hoy
        )
        
        self.assertEqual(estadistica.turnos_atendidos, 0)
        self.assertEqual(estadistica.tiempo_promedio_atencion, 0)
        self.assertEqual(float(estadistica.calificacion_promedio), 0.0)
        self.assertEqual(estadistica.tiempo_conectado, 0)
        self.assertEqual(estadistica.turnos_transferidos, 0)
