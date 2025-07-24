from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models.empleado import Empleado

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