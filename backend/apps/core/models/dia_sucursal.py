from django.db import models
from django.utils.translation import gettext_lazy as _
from .sucursal import Sucursal
from .dias_semana import DiasSemana

class DiaSucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursal')
    dia_semana = models.ForeignKey(DiasSemana, on_delete=models.CASCADE, verbose_name='Día de la semana')
    hora_apertura = models.TimeField(verbose_name='Hora de apertura')
    hora_cierre = models.TimeField(verbose_name='Hora de cierre')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'dia_sucursales'
        verbose_name = 'Dia Sucursal'
        verbose_name_plural = 'Dia Sucursales'
        unique_together = ('sucursal', 'dia_semana')

    def __str__(self):
        return f"{self.sucursal.nombre} - {self.dia_semana.nombre}"