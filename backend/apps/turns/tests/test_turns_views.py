import pytest
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

from apps.users.models.usuario import Usuario
from apps.users.models.empleado import Empleado
from apps.turns.models.turno import Turno
from apps.turns.models.calificacion_servicio import CalificacionServicio
from apps.turns.models.cola_turnos import ColaTurnos
from apps.core.models.servicio import Servicio
from apps.core.models.sucursal import Sucursal
from apps.turns.services.logic import GestorTurnos


class CrearTurnoViewTest(TransactionTestCase):
    """Tests para la vista de creación de turnos"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
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
        
        self.url = reverse('crear_turno')
    
    def test_crear_turno_usuario_autenticado(self):
        """Test para crear turno con usuario autenticado"""
        self.client.force_authenticate(user=self.usuario)
        
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': False
        }
        
        with patch.object(GestorTurnos, 'crear_turno') as mock_crear:
            turno = Turno(
                id=1,
                numero_turno='T001',
                servicio=self.servicio,
                sucursal=self.sucursal,
                usuario=self.usuario,
                estado=Turno.EstadoTurno.EN_ESPERA
            )
            mock_crear.return_value = turno
            
            response = self.client.post(self.url, data)
            mock_crear.assert_called_once_with(
                usuario=self.usuario,
                servicio=self.servicio,
                sucursal=self.sucursal,
                es_agendado=False,
                fecha_agendada=None
            )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_crear_turno_usuario_anonimo(self):
        """Test para crear turno sin autenticación (usuario anónimo)"""
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': False
        }
        
        with patch.object(GestorTurnos, 'crear_turno') as mock_crear:
            turno = Turno(
                id=1,
                numero_turno='T001',
                servicio=self.servicio,
                sucursal=self.sucursal,
                usuario=None,
                estado=Turno.EstadoTurno.EN_ESPERA
            )
            mock_crear.return_value = turno
            
            response = self.client.post(self.url, data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_crear.assert_called_once_with(
                usuario=None,
                servicio=self.servicio,
                sucursal=self.sucursal,
                es_agendado=False,
                fecha_agendada=None
            )
    
    def test_crear_turno_agendado(self):
        """Test para crear turno agendado"""
        self.client.force_authenticate(user=self.usuario)
        
        fecha_agendada = timezone.now() + timedelta(days=1)
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
            'es_agendado': True,
            'fecha_agendada': fecha_agendada.isoformat()
        }
        
        with patch.object(GestorTurnos, 'crear_turno') as mock_crear:
            turno = Turno(
                id=1,
                numero_turno='T001',
                servicio=self.servicio,
                sucursal=self.sucursal,
                usuario=self.usuario,
                estado=Turno.EstadoTurno.EN_ESPERA
            )
            mock_crear.return_value = turno
            
            response = self.client.post(self.url, data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_crear_turno_datos_invalidos(self):
        """Test para crear turno con datos inválidos"""
        self.client.force_authenticate(user=self.usuario)
        
        data = {
            'servicio': 999,  # Servicio inexistente
            'sucursal': self.sucursal.id,
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_crear_turno_error_gestor(self):
        """Test para manejar errores del GestorTurnos"""
        self.client.force_authenticate(user=self.usuario)
        
        data = {
            'servicio': self.servicio.id,
            'sucursal': self.sucursal.id,
        }
        
        with patch.object(GestorTurnos, 'crear_turno') as mock_crear:
            mock_crear.side_effect = ValueError("Ya tiene un turno activo")
            
            response = self.client.post(self.url, data)
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('detail', response.json())


class ListarTurnosUsuarioViewTest(TransactionTestCase):
    """Tests para la vista de listado de turnos del usuario"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear otro usuario
        self.otro_usuario = Usuario.objects.create_user(
            username='otro_user',
            email='otro@example.com',
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
        
        # Crear turnos
        self.turno_usuario = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario
        )
        
        self.turno_otro_usuario = Turno.objects.create(
            numero_turno='T002',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.otro_usuario
        )
        
        self.url = reverse('listar_turnos_usuario')
    
    def test_acceso_sin_autenticacion(self):
        """Test que verifica que se requiere autenticación"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listar_turnos_usuario_autenticado(self):
        """Test para listar turnos del usuario autenticado"""
        self.client.force_authenticate(user=self.usuario)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Verificar que solo devuelve los turnos del usuario autenticado
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['numero_turno'], 'T001')
    
    def test_filtrar_turnos_por_estado(self):
        """Test para filtrar turnos por estado"""
        self.client.force_authenticate(user=self.usuario)
        
        # Crear turno con estado diferente
        Turno.objects.create(
            numero_turno='T003',
            servicio=self.servicio,
            sucursal=self.sucursal,
            usuario=self.usuario,
            estado=Turno.EstadoTurno.FINALIZADO
        )
        
        # Filtrar por estado EN_ESPERA
        response = self.client.get(self.url, {'estado': 'en_espera'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['estado'], 'en_espera')


class DetalleTurnoUsuarioViewTest(TransactionTestCase):
    """Tests para la vista de detalle de turno del usuario"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
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
        
        self.url = reverse('detalle_turno_usuario', kwargs={'pk': self.turno.id})
    
    def test_obtener_detalle_turno(self):
        """Test para obtener el detalle de un turno"""
        self.client.force_authenticate(user=self.usuario)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['numero_turno'], 'T001')
        self.assertEqual(data['estado'], 'en_espera')
    
    def test_cancelar_turno(self):
        """Test para cancelar un turno"""
        self.client.force_authenticate(user=self.usuario)
        
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que el turno fue cancelado
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.estado, 'cancelado')
    
    def test_cancelar_turno_no_cancelable(self):
        """Test para intentar cancelar un turno que no se puede cancelar"""
        self.client.force_authenticate(user=self.usuario)
        
        # Cambiar estado a finalizado
        self.turno.estado = Turno.EstadoTurno.FINALIZADO
        self.turno.save()
        
        response = self.client.delete(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SiguienteTurnoEmpleadoViewTest(TransactionTestCase):
    """Tests para la vista de siguiente turno del empleado"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
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
        
        # Crear servicio
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            codigo_servicio='ST',
            sucursal=self.sucursal,
            tiempo_estimado_atencion=15,
            activo=True
        )
        
        # Crear empleado
        self.empleado = Empleado.objects.create(
            usuario=self.empleado_user,
            codigo_empleado=f'EMP{hash(self.id()) % 10000:04d}',
            sucursal=self.sucursal,
            ventanilla_asignada='V1'
        )
        
        # Asignar servicio al empleado
        self.empleado.servicios.add(self.servicio)
        
        # Crear turno en espera
        self.turno = Turno.objects.create(
            numero_turno='T001',
            servicio=self.servicio,
            sucursal=self.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        )
        
        self.url = reverse('siguiente_turno_empleado')
    
    def test_acceso_sin_autenticacion(self):
        """Test que verifica que se requiere autenticación"""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_acceso_usuario_no_empleado(self):
        """Test que verifica que solo empleados pueden acceder"""
        usuario_normal = Usuario.objects.create_user(
            username='normal_user',
            email='normal@test.com',
            password='testpass123'
        )
        
        self.client.force_authenticate(user=usuario_normal)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_obtener_siguiente_turno_exitoso(self):
        """Test para obtener el siguiente turno exitosamente"""
        self.client.force_authenticate(user=self.empleado_user)
        
        with patch.object(GestorTurnos, 'obtener_siguiente_turno') as mock_obtener:
            with patch.object(GestorTurnos, 'asignar_turno_empleado') as mock_asignar:
                mock_obtener.return_value = self.turno
                mock_asignar.return_value = self.turno
                
                response = self.client.post(self.url)
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                mock_obtener.assert_called_once_with(self.empleado)
                mock_asignar.assert_called_once_with(self.turno, self.empleado)
    
    def test_no_hay_turnos_disponibles(self):
        """Test cuando no hay turnos disponibles"""
        self.client.force_authenticate(user=self.empleado_user)
        
        with patch.object(GestorTurnos, 'obtener_siguiente_turno') as mock_obtener:
            mock_obtener.return_value = None
            
            response = self.client.post(self.url)
            
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_empleado_ya_tiene_turno_en_atencion(self):
        """Test cuando el empleado ya tiene un turno en atención"""
        self.client.force_authenticate(user=self.empleado_user)
