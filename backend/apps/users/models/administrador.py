from django.db import models
from django.utils.translation import gettext_lazy as _
from .usuario import Usuario

class Administrador(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='perfil_administrador'
    )
    nivel_acceso = models.CharField(_("nivel de acceso"), max_length=20, default='admin')
    permisos = models.JSONField(_("permisos"), default=dict, blank=True)
    sucursal = models.ForeignKey(
        'core.Sucursal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("sucursal")
    )

    class Meta:
        db_table = 'administradores'
        verbose_name = _('administrador')
        verbose_name_plural = _('administradores')
        ordering = ['usuario__username']

    def __str__(self):
        return f"{self.usuario.username} (Admin)" 