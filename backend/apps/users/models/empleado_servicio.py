from django.db import models
from django.utils.translation import gettext_lazy as _

class EmpleadoServicio(models.Model):
    empleado = models.ForeignKey('users.Empleado', on_delete=models.CASCADE)
    servicio = models.ForeignKey('core.Servicio', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'empleados_servicios'
        verbose_name = _('servicio de empleado')
        verbose_name_plural = _('servicios de empleado')
        unique_together = ('empleado', 'servicio')

    def __str__(self):
        return f"{self.empleado} - {self.servicio}"
