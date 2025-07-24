from django.db import models
from django.utils.translation import gettext_lazy as _
from .empleado import Empleado

class EmpleadoServicio(models.Model):
    """Tabla intermedia para la relación empleado-servicio"""
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='asignaciones_servicio'
    )
    servicio = models.ForeignKey(
        'core.Servicio',
        on_delete=models.CASCADE,
        related_name='asignaciones_empleado'
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'empleados_servicios'
        verbose_name = _('empleado servicio')
        verbose_name_plural = _('empleados servicios')
        unique_together = ('empleado', 'servicio')

    def __str__(self):
        return f"{self.empleado.codigo_empleado} - {self.servicio.nombre}" 