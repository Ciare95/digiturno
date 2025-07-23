import random
import string
from django.utils import timezone
from django.db import transaction
from django.db import models
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
        Genera un número de turno único con el formato: LETRA-CÓDIGO
        donde LETRA corresponde al servicio y CÓDIGO es una combinación
        aleatoria de 3 números y 1 letra.
        """
        # Obtener la letra del servicio
        letra_servicio = servicio.codigo_servicio[0].upper()

        # Generar código aleatorio de 3 números y 1 letra
        while True:
            # 3 números aleatorios
            numeros = [str(random.randint(0, 9)) for _ in range(3)]
            # 1 letra aleatoria
            letra_aleatoria = random.choice(string.ascii_uppercase)

            # Combinar y barajar
            componentes = numeros + [letra_aleatoria]
            random.shuffle(componentes)
            sufijo_turno = "".join(componentes)

            numero_turno = f"{letra_servicio}{sufijo_turno}"

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
        Calcula el tiempo estimado de espera para un nuevo turno basado en:
        - Cantidad de turnos en espera para el servicio
        - Tiempo promedio real de atención del servicio
        - Cantidad de empleados activos atendiendo ese servicio
        """
        from django.db.models import Avg, Count, Q
        from django.utils import timezone
        from datetime import timedelta

        # 1. Obtener turnos en espera para este servicio en esta sucursal
        turnos_en_espera = ColaTurnos.objects.filter(
            servicio=servicio,
            turno__sucursal=sucursal,
            activo=True
        ).count()

        # 2. Calcular tiempo promedio real de atención (últimas 24 horas)
        ayer = timezone.now() - timedelta(days=1)
        tiempo_promedio_atencion = Turno.objects.filter(
            servicio=servicio,
            sucursal=sucursal,
            estado=Turno.EstadoTurno.FINALIZADO,
            fecha_finalizacion__gte=ayer,
            fecha_inicio_atencion__isnull=False,
            fecha_finalizacion__isnull=False
        ).aggregate(
            promedio=Avg(
                models.F('fecha_finalizacion') - models.F('fecha_inicio_atencion')
            )
        )['promedio']

        # Si no hay datos históricos, usar el tiempo estimado configurado
        if not tiempo_promedio_atencion:
            tiempo_promedio_atencion = timedelta(minutes=servicio.tiempo_estimado_atencion)

        # 3. Contar empleados activos atendiendo este servicio
        empleados_activos = servicio.empleados.filter(
            estado_conexion='ACTIVO',
            sucursal=sucursal
        ).exclude(
            turnos_atendidos__estado=Turno.EstadoTurno.EN_ATENCION
        ).count()

        # Si no hay empleados activos, asumir al menos 1 para evitar división por cero
        empleados_activos = max(empleados_activos, 1)

        # 4. Calcular tiempo estimado total
        tiempo_espera = (
            (turnos_en_espera * tiempo_promedio_atencion.total_seconds()) / 
            (empleados_activos * 60)  # Convertir a minutos
        )

        # 5. Aplicar factor de seguridad (10% adicional)
        tiempo_espera *= 1.1

        # Redondear al minuto más cercano
        return round(tiempo_espera)

    @staticmethod
    def verificar_disponibilidad(servicio, sucursal):
        """
        Verifica si el servicio está disponible en la sucursal
        """
        return (
            servicio.activo and 
            sucursal.activa and 
            servicio.sucursal == sucursal
        )

    @staticmethod
    def verificar_turnos_activos(usuario, servicio, sucursal):
        """
        Verifica si el usuario ya tiene turnos activos en el servicio y sucursal
        """
        if not usuario:
            return True  
            
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
            turno__sucursal=sucursal,
            activo=True
        ).count() + 1
        
        ColaTurnos.objects.create(
            turno=turno,
            servicio=servicio,
            posicion_cola=posicion,
            tiempo_espera_estimado=tiempo_espera,
            activo=True
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
            'fecha_creacion'        # Ordenar por orden de llegada
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
                turno__sucursal=turno.sucursal,
                activo=True,
                posicion_cola__gt=cola_turno.posicion_cola
            ).update(posicion_cola=F('posicion_cola') - 1)

        except ColaTurnos.DoesNotExist:
            pass

        return turno

    @staticmethod
    @transaction.atomic
    def transferir_turno(turno, nuevo_servicio, empleado):
        """
        Transfiere un turno a otro servicio y lo coloca en la cola correspondiente
        """
        # Verificar que el turno esté en atención por el empleado
        if turno.estado != Turno.EstadoTurno.EN_ATENCION or turno.empleado != empleado:
            raise ValueError("El turno debe estar en atención por el empleado actual")

        # Actualizar el turno
        turno.servicio = nuevo_servicio
        turno.estado = Turno.EstadoTurno.EN_ESPERA
        turno.empleado = None
        turno.fecha_inicio_atencion = None
        turno.save()

        # Actualizar cola
        ColaTurnos.objects.filter(turno=turno, activo=True).update(activo=False)

        # Calcular nueva posición en cola
        nueva_posicion = ColaTurnos.objects.filter(
            servicio=nuevo_servicio,
            activo=True
        ).count() + 1

        # Crear nueva entrada en la cola
        ColaTurnos.objects.create(
            turno=turno,
            servicio=nuevo_servicio,
            posicion_cola=nueva_posicion,
            tiempo_espera_estimado=nuevo_servicio.tiempo_estimado_atencion * nueva_posicion,
            activo=True
        )

        return turno
