from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.turns.models.turno import Turno
from apps.users.models.usuario import Usuario
from apps.users.models.empleado import Empleado
from apps.core.models.servicio import Servicio

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
        Empleado,  
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