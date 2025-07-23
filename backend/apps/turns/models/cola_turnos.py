from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.turns.models.turno import Turno
from apps.core.models.servicio import Servicio

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