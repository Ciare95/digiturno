from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import Usuario, Empleado  # Importar Empleado desde users
from apps.core.models import Servicio, Sucursal

class Turno(models.Model):
    class EstadoTurno(models.TextChoices):
        EN_ESPERA = 'en_espera', 'En Espera'
        LLAMADO = 'llamado', 'Llamado'
        EN_ATENCION = 'en_atencion', 'En Atención'
        FINALIZADO = 'finalizado', 'Finalizado'
        CANCELADO = 'cancelado', 'Cancelado'
        AUSENTE = 'ausente', 'Ausente'

    numero_turno = models.CharField(_('número de turno'), max_length=20)
    servicio = models.ForeignKey(
        'core.Servicio',
        on_delete=models.CASCADE,
        verbose_name=_('servicio')
    )
    sucursal = models.ForeignKey(
        'core.Sucursal',
        on_delete=models.CASCADE,
        verbose_name=_('sucursal')
    )
    usuario = models.ForeignKey(
        'users.Usuario',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('usuario')
    )
    empleado = models.ForeignKey(
        'users.Empleado',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='turnos_atendidos',
        verbose_name=_('empleado')
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoTurno.choices,
        default=EstadoTurno.EN_ESPERA,
        verbose_name=_('estado')
    )
    fecha_creacion = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    fecha_llamado = models.DateTimeField(_('fecha de llamado'), null=True, blank=True)
    fecha_inicio_atencion = models.DateTimeField(_('fecha de inicio de atención'), null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(_('fecha de finalización'), null=True, blank=True)
    es_agendado = models.BooleanField(_('es agendado'), default=False)
    fecha_agendada = models.DateTimeField(_('fecha agendada'), null=True, blank=True)
    tiempo_espera_estimado = models.DurationField(_('tiempo de espera estimado'), null=True, blank=True)
    observaciones = models.TextField(_('observaciones'), blank=True)

    class Meta:
        db_table = 'turnos'
        verbose_name = _('turno')
        verbose_name_plural = _('turnos')
        ordering = ['-fecha_creacion']
    def __str__(self):
        return f"Turno {self.numero_turno} - {self.servicio}"

class CalificacionServicio(models.Model):
    turno = models.OneToOneField(
        Turno,
        on_delete=models.CASCADE,
        verbose_name=_('turno')
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('usuario')
    )
    empleado = models.ForeignKey(
        'users.Empleado',  
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('empleado')
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        verbose_name=_('servicio')
    )
    calificacion = models.IntegerField(_('calificación'))
    comentario = models.TextField(_('comentario'), blank=True, null=True)
    aspectos_evaluados = models.JSONField(_('aspectos evaluados'), default=dict, blank=True)
    fecha_calificacion = models.DateTimeField(_('fecha de calificación'), auto_now_add=True)
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)

    class Meta:
        db_table = 'calificaciones_servicio'
        verbose_name = _('calificación de servicio')
        verbose_name_plural = _('calificaciones de servicio')
        ordering = ['-fecha_calificacion']

    def __str__(self):
        return f"Calificación {self.calificacion} - Turno {self.turno.numero_turno}"

class ColaTurnos(models.Model):
    turno = models.OneToOneField(
        Turno,
        on_delete=models.CASCADE,
        verbose_name=_('turno')
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        verbose_name=_('servicio')
    )
    posicion_cola = models.IntegerField(_('posición en cola'))
    fecha_ingreso_cola = models.DateTimeField(_('fecha de ingreso a cola'), auto_now_add=True)
    tiempo_espera_estimado = models.IntegerField(_('tiempo de espera estimado (min)'), null=True, blank=True)
    activo = models.BooleanField(_('activo'), default=True)
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado el'), auto_now=True)

    class Meta:
        db_table = 'cola_turnos'
        verbose_name = _('cola de turnos')
        verbose_name_plural = _('colas de turnos')
        ordering = ['posicion_cola']

    def __str__(self):
        return f"Posición {self.posicion_cola} - {self.turno.numero_turno}"

class Notificacion(models.Model):
    TIPOS_NOTIFICACION = [
        ('llamado_turno', _('Llamado de turno')),
        ('turno_finalizado', _('Turno finalizado')),
        ('turno_cancelado', _('Turno cancelado')),
        ('turno_transferido', _('Turno transferido')),
        ('sistema', _('Sistema')),
    ]

    CANALES_NOTIFICACION = [
        ('websocket', _('WebSocket')),
        ('email', _('Email')),
        ('sms', _('SMS')),
        ('push', _('Push')),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name=_('usuario'),
        null=True,
        blank=True
    )
    turno = models.ForeignKey(
        Turno,
        on_delete=models.CASCADE,
        verbose_name=_('turno'),
        null=True,
        blank=True
    )
    tipo = models.CharField(_('tipo'), max_length=30, choices=TIPOS_NOTIFICACION)
    titulo = models.CharField(_('título'), max_length=100)
    mensaje = models.TextField(_('mensaje'))
    leida = models.BooleanField(_('leída'), default=False)
    fecha_envio = models.DateTimeField(_('fecha de envío'), auto_now_add=True)
    fecha_lectura = models.DateTimeField(_('fecha de lectura'), null=True, blank=True)
    canal = models.CharField(
        _('canal'),
        max_length=20,
        choices=CANALES_NOTIFICACION,
        default='websocket'
    )
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)

    class Meta:
        db_table = 'notificaciones'
        verbose_name = _('notificación')
        verbose_name_plural = _('notificaciones')
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

class EstadisticaEmpleado(models.Model):
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        verbose_name=_('empleado')
    )
    fecha = models.DateField(_('fecha'))
    turnos_atendidos = models.IntegerField(_('turnos atendidos'), default=0)
    tiempo_promedio_atencion = models.IntegerField(_('tiempo promedio de atención (min)'), default=0)
    calificacion_promedio = models.DecimalField(
        _('calificación promedio'),
        max_digits=3,
        decimal_places=2,
        default=0
    )
    tiempo_conectado = models.IntegerField(_('tiempo conectado (min)'), default=0)
    turnos_transferidos = models.IntegerField(_('turnos transferidos'), default=0)
    created_at = models.DateTimeField(_('creado el'), auto_now_add=True)
    updated_at = models.DateTimeField(_('actualizado el'), auto_now=True)

    class Meta:
        db_table = 'estadisticas_empleado'
        verbose_name = _('estadística de empleado')
        verbose_name_plural = _('estadísticas de empleados')
        ordering = ['-fecha']
        unique_together = ['empleado', 'fecha']

    def __str__(self):
        return f"Estadísticas {self.empleado} - {self.fecha}"


