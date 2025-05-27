from django.db import models
from django.contrib.auth.models import AbstractUser


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo_sucursal = models.CharField(max_length=10, unique=True, verbose_name='Código Sucursal')
    direccion = models.TextField(verbose_name='Dirección')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    ciudad = models.CharField(max_length=50, verbose_name='Ciudad')
    departamento = models.CharField(max_length=50, verbose_name='Departamento')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    configuracion = models.JSONField(default=dict, verbose_name='Configuración')

    class Meta:
        db_table = 'sucursales'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo_servicio = models.CharField(max_length=10, verbose_name='Código Servicio')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursal')
    tiempo_estimado_atencion = models.PositiveIntegerField(default=15, verbose_name='Tiempo Estimado (min)')
    color_identificacion = models.CharField(max_length=7, blank=True, null=True, verbose_name='Color')
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ícono')

    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'