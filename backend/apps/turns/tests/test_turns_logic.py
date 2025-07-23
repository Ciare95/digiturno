import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch, MagicMock

from apps.users.models.usuario import Usuario, Empleado
from apps.turns.models.turno import Turno, ColaTurnos
from apps.turns.services.logic import GestorTurnos
from apps.core.models.core_model import Servicio, Sucursal


class GestorTurnosTest(TestCase):
    """Tests para la clase GestorTurnos"""
    
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
        
        # Establecer relación servicio-sucursal
        self.servicio.sucursal = self.sucursal
        self.servicio.save()
        
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
            ventanilla_asignada='V1',
            estado_conexion='conectado'
        )
        
        # Asignar servicio al empleado
        self.empleado.servicios.add(self.servicio)


class GenerarNumeroTurnoTest(GestorTurnosTest):
    """Tests para la generación de números de turno"""
    
    def test_generar_numero_turno_basico(self):
        """Test para generar un número de turno básico"""
        numero_turno = GestorTurnos.generar_numero_turno(self.servicio, self.sucursal)
        
        # Verificar formato: LETRA + 3 dígitos
        self.assertEqual(len(numero_turno), 4)
        self.assertEqual(numero_turno[0], 'S')  # Primera letra del código del servicio
        self.assertTrue(numero_turno[1:].isdigit())
        self.assertEqual(len(numero_turno[1:]), 3)
    
    def test_generar_numero_turno_unico(self):
        """Test para verificar que los números de turno son únicos"""
        # Crear un turno existente
        Turno.objects.create(
            numero_turno='S001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            fecha_creacion=timezone.now()
        )
        
        # Generar nuevo número
        with patch('random.randint') as mock_randint:
            # Primero devolver 1 (que ya existe), luego 2 (que no existe)
            mock_randint.side_effect = [1, 2]
            
            numero_turno = GestorTurnos.generar_numero_turno(self.servicio, self.sucursal)
            
            # Verificar que se generó S002 (no S001)
            self.assertEqual(numero_turno, 'S002')
            self.assertEqual(mock_randint.call_count, 2)
    
    def test_generar_numero_turno_diferentes_servicios(self):
        """Test para verificar números de turno con diferentes servicios"""
        # Crear otro servicio
        otro_servicio = Servicio.objects.create(
            nombre='Otro Servicio',
            codigo_servicio='OS',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=20,
            activo=True
        )
        
        numero1 = GestorTurnos.generar_numero_turno(self.servicio, self.sucursal)
        numero2 = GestorTurnos.generar_numero_turno(otro_servicio, self.sucursal)
        
        # Verificar que tienen diferentes prefijos
        self.assertEqual(numero1[0], 'S')
        self.assertEqual(numero2[0], 'O')


class CalcularTiempoEsperaTest(GestorTurnosTest):
    """Tests para el cálculo de tiempo de espera"""
    
    def test_calcular_tiempo_espera_sin_cola(self):
        """Test para calcular tiempo de espera sin turnos en cola"""
        tiempo_espera = GestorTurnos.calcular_tiempo_espera(self.servicio, self.sucursal)
        
        # Sin turnos en cola, el tiempo debería ser mínimo
        self.assertGreaterEqual(tiempo_espera, 0)
        self.assertLessEqual(tiempo_espera, 30)  # Máximo razonable para cola vacía
    
    def test_calcular_tiempo_espera_con_cola(self):
        """Test para calcular tiempo de espera con turnos en cola"""
        # Crear turnos en cola
        for i in range(3):
            turno = Turno.objects.create(
                numero_turno=f'T00{i+1}',
                servicio=self.servicio,
                sucursal=self.sucursal,
                estado=Turno.EstadoTurno.EN_ESPERA
            )
            
            ColaTurnos.objects.create(
                turno=turno,
                servicio=self.servicio,
                posicion_cola=i+1,
                activo=True
            )
        
        tiempo_espera = GestorTurnos.calcular_tiempo_espera(self.servicio, self.sucursal)
        
        # Con 3 turnos en cola, el tiempo debería ser mayor
        self.assertGreater(tiempo_espera, 0)
    
    def test_calcular_tiempo_espera_con_historial(self):
        """Test para calcular tiempo de espera usando historial de atención"""
        # Crear turnos finalizados con tiempos de atención
        fecha_ayer = timezone.now() - timedelta(hours=12)
        
        for i in range(2):
            Turno.objects.create(
                numero_turno=f'H00{i+1}',
                servicio=self.servicio,
                sucursal=self.sucursal,
                estado=Turno.EstadoTurno.FINALIZADO,
                fecha_inicio_atencion=fecha_ayer,
                fecha_finalizacion=fecha_ayer + timedelta(minutes=10)
            )
        
        # Crear turno en cola
        turno_cola = Turno.objects.create(
            numero_turno='C001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        ColaTurnos.objects.create(
            turno=turno_cola,
            servicio=self.servicio,
            posicion_cola=1,
            activo=True
        )
        
        tiempo_espera = GestorTurnos.calcular_tiempo_espera(self.servicio, self.sucursal)
        
        # El tiempo debería basarse en el historial real
        self.assertGreater(tiempo_espera, 0)


class VerificarDisponibilidadTest(GestorTurnosTest):
    """Tests para verificar disponibilidad del servicio"""
    
    def test_verificar_disponibilidad_servicio_activo(self):
        """Test para verificar disponibilidad con servicio activo"""
        disponible = GestorTurnos.verificar_disponibilidad(self.servicio, self.sucursal)
        self.assertTrue(disponible)
    
    def test_verificar_disponibilidad_servicio_inactivo(self):
        """Test para verificar disponibilidad con servicio inactivo"""
        self.servicio.activo = False
        self.servicio.save()
        
        disponible = GestorTurnos.verificar_disponibilidad(self.servicio, self.sucursal)
        self.assertFalse(disponible)
    
    def test_verificar_disponibilidad_sucursal_inactiva(self):
        """Test para verificar disponibilidad con sucursal inactiva"""
        self.sucursal.activa = False
        self.sucursal.save()
        
        disponible = GestorTurnos.verificar_disponibilidad(self.servicio, self.sucursal)
        self.assertFalse(disponible)
    
    def test_verificar_disponibilidad_servicio_no_en_sucursal(self):
        """Test para verificar disponibilidad con servicio no disponible en sucursal"""
        # Crear otro servicio no asociado a la sucursal
        otra_sucursal = Sucursal.objects.create(
            nombre='Otra Sucursal',
            codigo_sucursal='OTRA123',
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
        
        disponible = GestorTurnos.verificar_disponibilidad(otro_servicio, self.sucursal)
        self.assertFalse(disponible)


class VerificarTurnosActivosTest(GestorTurnosTest):
    """Tests para verificar turnos activos del usuario"""
    
    def test_verificar_sin_turnos_activos(self):
        """Test para verificar usuario sin turnos activos"""
        resultado = GestorTurnos.verificar_turnos_activos(
            self.usuario, self.servicio, self.sucursal
        )
        self.assertTrue(resultado)
    
    def test_verificar_con_turno_activo(self):
        """Test para verificar usuario con turno activo"""
        # Crear turno activo
        Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        with self.assertRaises(ValueError) as context:
            GestorTurnos.verificar_turnos_activos(
                self.usuario, self.servicio, self.sucursal
            )
        
        self.assertIn('Ya tiene un turno activo', str(context.exception))
    
    def test_verificar_con_turno_finalizado(self):
        """Test para verificar usuario con turno finalizado (no activo)"""
        # Crear turno finalizado
        Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            estado=Turno.EstadoTurno.FINALIZADO
        )
        
        resultado = GestorTurnos.verificar_turnos_activos(
            self.usuario, self.servicio, self.sucursal
        )
        self.assertTrue(resultado)
    
    def test_verificar_usuario_anonimo(self):
        """Test para verificar usuario anónimo (None)"""
        resultado = GestorTurnos.verificar_turnos_activos(
            None, self.servicio, self.sucursal
        )
        self.assertTrue(resultado)


class CrearTurnoTest(GestorTurnosTest):
    """Tests para la creación de turnos"""
    
    def test_crear_turno_basico(self):
        """Test para crear un turno básico"""
        turno = GestorTurnos.crear_turno(
            usuario=self.usuario,
            servicio=self.servicio,
            sucursal=self.sucursal
        )
        
        self.assertIsNotNone(turno)
        self.assertEqual(turno.usuario, self.usuario)
        self.assertEqual(turno.servicio, self.servicio)
        self.assertEqual(turno.sucursal, self.sucursal)
        self.assertEqual(turno.estado, Turno.EstadoTurno.EN_ESPERA)
        self.assertIsNotNone(turno.numero_turno)
        self.assertIsNotNone(turno.tiempo_espera_estimado)
        
        # Verificar que se creó entrada en cola
        cola = ColaTurnos.objects.get(turno=turno)
        self.assertTrue(cola.activo)
        self.assertEqual(cola.posicion_cola, 1)
    
    def test_crear_turno_anonimo(self):
        """Test para crear turno sin usuario"""
        turno = GestorTurnos.crear_turno(
            usuario=None,
            servicio=self.servicio,
            sucursal=self.sucursal
        )
        
        self.assertIsNotNone(turno)
        self.assertIsNone(turno.usuario)
        self.assertEqual(turno.servicio, self.servicio)
        self.assertEqual(turno.sucursal, self.sucursal)
    
    def test_crear_turno_agendado(self):
        """Test para crear turno agendado"""
        fecha_agendada = timezone.now() + timedelta(days=1)
        
        turno = GestorTurnos.crear_turno(
            usuario=self.usuario,
            servicio=self.servicio,
            sucursal=self.sucursal,
            es_agendado=True,
            fecha_agendada=fecha_agendada
        )
        
        self.assertTrue(turno.es_agendado)
        self.assertEqual(turno.fecha_agendada, fecha_agendada)
    
    def test_crear_turno_servicio_no_disponible(self):
        """Test para crear turno con servicio no disponible"""
        self.servicio.activo = False
        self.servicio.save()
        
        with self.assertRaises(ValueError) as context:
            GestorTurnos.crear_turno(
                usuario=self.usuario,
                servicio=self.servicio,
                sucursal=self.sucursal
            )
        
        self.assertIn('no está disponible', str(context.exception))
    
    def test_crear_turno_usuario_con_turno_activo(self):
        """Test para crear turno cuando usuario ya tiene uno activo"""
        # Crear primer turno
        GestorTurnos.crear_turno(
            usuario=self.usuario,
            servicio=self.servicio,
            sucursal=self.sucursal
        )
        
        # Intentar crear segundo turno
        with self.assertRaises(ValueError) as context:
            GestorTurnos.crear_turno(
                usuario=self.usuario,
                servicio=self.servicio,
                sucursal=self.sucursal
            )
        
        self.assertIn('Ya tiene un turno activo', str(context.exception))
    
    def test_crear_turno_agendado_fecha_duplicada(self):
        """Test para crear turno agendado con fecha ya ocupada"""
        fecha_agendada = timezone.now() + timedelta(days=1)
        
        # Crear primer turno agendado
        GestorTurnos.crear_turno(
            usuario=self.usuario,
            servicio=self.servicio,
            sucursal=self.sucursal,
            es_agendado=True,
            fecha_agendada=fecha_agendada
        )
        
        # Intentar crear segundo turno para la misma fecha
        with self.assertRaises(ValueError) as context:
            GestorTurnos.crear_turno(
                usuario=self.usuario,
                servicio=self.servicio,
                sucursal=self.sucursal,
                es_agendado=True,
                fecha_agendada=fecha_agendada
            )
        
        self.assertIn('Ya tiene un turno activo', str(context.exception))


class ObtenerSiguienteTurnoTest(GestorTurnosTest):
    """Tests para obtener el siguiente turno"""
    
    def test_obtener_siguiente_turno_exitoso(self):
        """Test para obtener el siguiente turno exitosamente"""
        # Crear turno en espera
        turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        siguiente = GestorTurnos.obtener_siguiente_turno(self.empleado)
        
        self.assertEqual(siguiente, turno)
    
    def test_obtener_siguiente_turno_sin_turnos(self):
        """Test para obtener siguiente turno cuando no hay turnos"""
        siguiente = GestorTurnos.obtener_siguiente_turno(self.empleado)
        
        self.assertIsNone(siguiente)
    
    def test_obtener_siguiente_turno_por_orden_llegada(self):
        """Test para obtener siguiente turno respetando orden de llegada"""
        # Crear otro servicio
        otro_servicio = Servicio.objects.create(
            nombre='Otro Servicio',
            codigo_servicio='OS',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=10,
            activo=True
        )
        
        # Asignar servicio al empleado
        self.empleado.servicios.add(otro_servicio)
        
        # Crear turnos
        turno_antiguo = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA,
            fecha_creacion=timezone.now() - timedelta(minutes=10)
        )
        
        turno_nuevo = Turno.objects.create(
            numero_turno='T002',
            servicio=otro_servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA,
            fecha_creacion=timezone.now()
        )
        
        siguiente = GestorTurnos.obtener_siguiente_turno(self.empleado)
        
        # Debería devolver el turno más antiguo (orden de llegada)
        self.assertEqual(siguiente, turno_antiguo)
    
    def test_obtener_siguiente_turno_empleado_sin_servicios(self):
        """Test para obtener siguiente turno con empleado sin servicios asignados"""
        # Remover servicios del empleado
        self.empleado.servicios.clear()
        
        siguiente = GestorTurnos.obtener_siguiente_turno(self.empleado)
        
        self.assertIsNone(siguiente)


class AsignarTurnoEmpleadoTest(GestorTurnosTest):
    """Tests para asignar turno a empleado"""
    
    def test_asignar_turno_empleado_exitoso(self):
        """Test para asignar turno a empleado exitosamente"""
        # Crear turno en espera
        turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        # Crear entrada en cola
        ColaTurnos.objects.create(
            turno=turno,
            servicio=self.servicio,
            posicion_cola=1,
            activo=True
        )
        
        turno_asignado = GestorTurnos.asignar_turno_empleado(turno, self.empleado)
        
        self.assertEqual(turno_asignado.empleado, self.empleado)
        self.assertEqual(turno_asignado.estado, Turno.EstadoTurno.EN_ATENCION)
        self.assertIsNotNone(turno_asignado.fecha_inicio_atencion)
        self.assertEqual(turno_asignado.ventanilla, self.empleado.ventanilla_asignada)
        
        # Verificar que la entrada en cola se desactivó
        cola = ColaTurnos.objects.get(turno=turno)
        self.assertFalse(cola.activo)
    
    def test_asignar_turno_reordena_cola(self):
        """Test para verificar que se reordena la cola al asignar turno"""
        # Crear múltiples turnos en cola
        turnos = []
        for i in range(3):
            turno = Turno.objects.create(
                numero_turno=f'T00{i+1}',
                servicio=self.servicio,
                sucursal=self.sucursal,
                estado=Turno.EstadoTurno.EN_ESPERA
            )
            
            ColaTurnos.objects.create(
                turno=turno,
                servicio=self.servicio,
                posicion_cola=i+1,
                activo=True
            )
            
            turnos.append(turno)
        
        # Asignar el primer turno
        GestorTurnos.asignar_turno_empleado(turnos[0], self.empleado)
        
        # Verificar que las posiciones se reordenaron
        cola_2 = ColaTurnos.objects.get(turno=turnos[1], activo=True)
        cola_3 = ColaTurnos.objects.get(turno=turnos[2], activo=True)
        
        self.assertEqual(cola_2.posicion_cola, 1)  # Era 2, ahora es 1
        self.assertEqual(cola_3.posicion_cola, 2)  # Era 3, ahora es 2


class TransferirTurnoTest(GestorTurnosTest):
    """Tests para transferir turnos"""
    
    def test_transferir_turno_exitoso(self):
        """Test para transferir turno exitosamente"""
        # Crear otro servicio
        nuevo_servicio = Servicio.objects.create(
            nombre='Nuevo Servicio',
            codigo_servicio='NS',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=20,
            activo=True
        )
        
        # Crear turno en atención
        turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            empleado=self.empleado,
            estado=Turno.EstadoTurno.EN_ATENCION,
            fecha_inicio_atencion=timezone.now()
        )
        
        turno_transferido = GestorTurnos.transferir_turno(
            turno, nuevo_servicio, self.empleado
        )
        
        self.assertEqual(turno_transferido.servicio, nuevo_servicio)
        self.assertEqual(turno_transferido.estado, Turno.EstadoTurno.EN_ESPERA)
        self.assertIsNone(turno_transferido.empleado)
        self.assertIsNone(turno_transferido.fecha_inicio_atencion)
        
        # Verificar que se creó nueva entrada en cola
        nueva_cola = ColaTurnos.objects.get(
            turno=turno, servicio=nuevo_servicio, activo=True
        )
        self.assertIsNotNone(nueva_cola)
    
    def test_transferir_turno_estado_incorrecto(self):
        """Test para transferir turno con estado incorrecto"""
        # Crear turno en espera (no en atención)
        turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        nuevo_servicio = Servicio.objects.create(
            nombre='Nuevo Servicio',
            codigo_servicio='NS',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=20,
            activo=True
        )
        
        with self.assertRaises(ValueError) as context:
            GestorTurnos.transferir_turno(turno, nuevo_servicio, self.empleado)
        
        self.assertIn('debe estar en atención', str(context.exception))
    
    def test_transferir_turno_empleado_incorrecto(self):
        """Test para transferir turno con empleado incorrecto"""
        # Crear otro empleado
        otro_empleado_user = Usuario.objects.create_user(
            username='otro_empleado',
            email='otro@test.com',
            password='testpass123'
        )
        
        otro_empleado = Empleado.objects.create(
            usuario=otro_empleado_user,
            codigo_empleado='EMP002',
            sucursal=self.sucursal,
            ventanilla_asignada='V2'
        )
        
        # Crear turno en atención por el primer empleado
        turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            empleado=self.empleado,
            estado=Turno.EstadoTurno.EN_ATENCION,
            fecha_inicio_atencion=timezone.now()
        )
        
        nuevo_servicio = Servicio.objects.create(
            nombre='Nuevo Servicio',
            codigo_servicio='NS',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=20,
            activo=True
        )
        
        # Intentar transferir con otro empleado
        with self.assertRaises(ValueError) as context:
            GestorTurnos.transferir_turno(turno, nuevo_servicio, otro_empleado)
        
        self.assertIn('debe estar en atención por el empleado actual', str(context.exception))
