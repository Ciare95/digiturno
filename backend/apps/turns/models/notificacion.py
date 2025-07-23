from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.turns.models.turno import Turno
from apps.users.models.usuario import Usuario

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