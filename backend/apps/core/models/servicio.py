from django.db import models
from django.utils.translation import gettext_lazy as _
from .sucursal import Sucursal

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo_servicio = models.CharField(max_length=20, verbose_name='Código Servicio')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursal')
    tiempo_estimado_atencion = models.PositiveIntegerField(default=15, verbose_name='Tiempo Estimado (min)')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios' 