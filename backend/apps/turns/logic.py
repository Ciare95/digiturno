import random
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, Min, F
from .models import Turno, ColaTurnos
from apps.core.models import Servicio, Sucursal

class GestorTurnos:
    """
    Clase para manejar la lógica de negocio relacionada con turnos y colas
    """
    
    @staticmethod
    def generar_numero_turno(servicio, sucursal):
        """
        Genera un número de turno único con el formato: LETRA-NÚMERO
        donde LETRA corresponde al servicio y NÚMERO es aleatorio de 3 dígitos
        """
        # Obtener la letra del servicio
        letra = servicio.codigo_servicio[0].upper()
        
        # Generar número aleatorio de 3 dígitos
        while True:
            numero = str(random.randint(1, 999)).zfill(3)
            numero_turno = f"{letra}{numero}"
            
            # Verificar que no exista este número de turno hoy
            existe = Turno.objects.filter(
                numero_turno=numero_turno,
                sucursal=sucursal,
                fecha_creacion__date=timezone.now().date()
            ).exists()
            
            if not existe:
                break
        
        return numero_turno

    @staticmethod
    def calcular_tiempo_espera(servicio, sucursal):
        """
        Calcula el tiempo estimado de espera para un nuevo turno
        """
        # Obtener cantidad de turnos en espera para este servicio
        turnos_en_espera = Turno.objects.filter(
            servicio=servicio,
            sucursal=sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        ).count()
        
        # Tiempo estimado = turnos en espera * tiempo promedio de atención del servicio
        tiempo_espera = turnos_en_espera * servicio.tiempo_estimado_atencion
        
        return tiempo_espera

    @staticmethod
    def verificar_disponibilidad(servicio, sucursal):
        """
        Verifica si el servicio está disponible en la sucursal
        """
        return (
            servicio.activo and 
            sucursal.activa and 
            servicio.sucursales.filter(id=sucursal.id).exists()
        )

    @staticmethod
    def verificar_turnos_activos(usuario, servicio, sucursal):
        """
        Verifica si el usuario ya tiene turnos activos en el servicio y sucursal
        """
        if not usuario:
            return True  # Usuarios anónimos pueden crear turnos
            
        estados_activos = [
            Turno.EstadoTurno.EN_ESPERA,
            Turno.EstadoTurno.LLAMADO,
            Turno.EstadoTurno.EN_ATENCION
        ]
        
        turno_activo = Turno.objects.filter(
            usuario=usuario,
            servicio=servicio,
            sucursal=sucursal,
            estado__in=estados_activos
        ).exists()
        
        if turno_activo:
            raise ValueError(
                "Ya tiene un turno activo para este servicio en esta sucursal. "
                "Debe esperar a que sea atendido o cancelarlo."
            )
        
        return True

    @classmethod
    @transaction.atomic
    def crear_turno(cls, usuario, servicio, sucursal, es_agendado=False, fecha_agendada=None):
        """
        Crea un nuevo turno y lo asigna a la cola correspondiente
        """
        # Verificar disponibilidad
        if not cls.verificar_disponibilidad(servicio, sucursal):
            raise ValueError("El servicio no está disponible en esta sucursal")
            
        # Verificar turnos activos del usuario
        cls.verificar_turnos_activos(usuario, servicio, sucursal)
        
        # Si es agendado, verificar que no tenga otros turnos agendados para la misma fecha
        if es_agendado and fecha_agendada and usuario:
            turnos_agendados = Turno.objects.filter(
                usuario=usuario,
                es_agendado=True,
                fecha_agendada__date=fecha_agendada.date(),
                estado__in=[
                    Turno.EstadoTurno.EN_ESPERA,
                    Turno.EstadoTurno.LLAMADO
                ]
            ).exists()
            
            if turnos_agendados:
                raise ValueError(
                    "Ya tiene un turno agendado para esta fecha. "
                    "Por favor seleccione otra fecha o cancele el turno existente."
                )

        # Generar número de turno
        numero_turno = cls.generar_numero_turno(servicio, sucursal)
        
        # Calcular tiempo de espera estimado
        tiempo_espera = cls.calcular_tiempo_espera(servicio, sucursal)
        
        # Crear el turno
        turno = Turno.objects.create(
            numero_turno=numero_turno,
            servicio=servicio,
            sucursal=sucursal,
            usuario=usuario,
            estado=Turno.EstadoTurno.EN_ESPERA,
            es_agendado=es_agendado,
            fecha_agendada=fecha_agendada,
            tiempo_espera_estimado=timezone.timedelta(minutes=tiempo_espera)
        )
        
        # Crear entrada en la cola
        posicion = ColaTurnos.objects.filter(
            servicio=servicio,
            sucursal=sucursal,
            activo=True
        ).count() + 1
        
        ColaTurnos.objects.create(
            turno=turno,
            servicio=servicio,
            posicion_cola=posicion,
            tiempo_espera_estimado=tiempo_espera
        )
        
        return turno

    @staticmethod
    def obtener_siguiente_turno(empleado):
        """
        Obtiene el siguiente turno en espera para los servicios del empleado
        """
        servicios_empleado = empleado.servicios.filter(activo=True)
        
        # Obtener el siguiente turno basado en prioridad y tiempo de espera
        siguiente_turno = Turno.objects.filter(
            servicio__in=servicios_empleado,
            sucursal=empleado.sucursal,
            estado=Turno.EstadoTurno.EN_ESPERA
        ).select_related(
            'servicio', 'sucursal'
        ).order_by(
            'servicio__prioridad',  # Primero por prioridad del servicio
            'fecha_creacion'        # Luego por orden de llegada
        ).first()
        
        return siguiente_turno

    @staticmethod
    @transaction.atomic
    def asignar_turno_empleado(turno, empleado):
        """
        Asigna un turno a un empleado y actualiza su estado
        """
        # Actualizar el turno
        turno.estado = Turno.EstadoTurno.EN_ATENCION
        turno.empleado = empleado
        turno.fecha_inicio_atencion = timezone.now()
        turno.ventanilla = empleado.ventanilla_asignada
        turno.save()

        # Actualizar la cola
        try:
            cola_turno = ColaTurnos.objects.get(turno=turno, activo=True)
            cola_turno.activo = False
            cola_turno.save()

            # Reordenar la cola
            ColaTurnos.objects.filter(
                servicio=turno.servicio,
                sucursal=turno.sucursal,
                activo=True,
                posicion_cola__gt=cola_turno.posicion_cola
            ).update(posicion_cola=F('posicion_cola') - 1)

        except ColaTurnos.DoesNotExist:
            pass

        return turno