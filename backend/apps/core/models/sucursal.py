from django.db import models
from django.utils.translation import gettext_lazy as _

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    direccion = models.TextField(verbose_name='Dirección')
    descripcion = models.CharField(max_length=255, default="Sin descripción")
    #url_mapa = models.TextField(verbose_name='url_mapa')
    
    codigo_sucursal = models.CharField(max_length=20, unique=True, verbose_name='Código Sucursal')
    telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name='Teléfono')
    ciudad = models.CharField(max_length=50, verbose_name='Ciudad')
    departamento = models.CharField(max_length=50, verbose_name='Departamento')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        db_table = 'sucursales'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales' 