from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models.usuario import Usuario
from apps.users.models.empleado import Empleado  # Importar Empleado desde users
from apps.core.models.servicio import Servicio
from apps.core.models.sucursal import Sucursal

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
        return f"Turno {self.numero_turno} - {self.servicio.nombre}"
