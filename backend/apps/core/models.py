from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo_sucursal = models.CharField(max_length=20, unique=True, verbose_name='Código Sucursal')
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
    codigo_servicio = models.CharField(max_length=20, verbose_name='Código Servicio')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursal')
    tiempo_estimado_atencion = models.PositiveIntegerField(default=15, verbose_name='Tiempo Estimado (min)')
    color_identificacion = models.CharField(max_length=7, blank=True, null=True, verbose_name='Color')
    icono = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ícono')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'


class Configuracion(models.Model):
    clave = models.CharField(_('clave'), max_length=100, unique=True)
    valor = models.JSONField(_('valor'), default=dict)
    descripcion = models.TextField(_('descripción'), blank=True, null=True)
    categoria = models.CharField(_('categoría'), max_length=50, default='general')
    es_global = models.BooleanField(_('es global'), default=True)
    sucursal = models.ForeignKey(
        Sucursal, 
        on_delete=models.CASCADE, 
        verbose_name=_('sucursal'),
        null=True,
        blank=True,
        related_name='configuraciones_sucursal'
    )
    fecha_creacion = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        db_table = 'configuraciones'
        verbose_name = _('configuración')
        verbose_name_plural = _('configuraciones')
        unique_together = ['clave', 'sucursal']

    def __str__(self):
        return f"{self.clave} - {self.categoria}"