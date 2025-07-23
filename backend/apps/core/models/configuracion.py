from django.db import models
from django.utils.translation import gettext_lazy as _
from .sucursal import Sucursal

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