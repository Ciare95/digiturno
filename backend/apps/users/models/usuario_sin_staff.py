from django.db import models
from django.utils.translation import gettext_lazy as _

class UsuarioSinStaff(models.Model):
    """Modelo simplificado para usuarios que no necesitan autenticación"""
    cedula = models.CharField(_("cédula"), max_length=20, unique=True)
    telefono = models.CharField(_("teléfono"), max_length=15)
    email = models.EmailField(_("correo electrónico"), blank=True, null=True)

    class Meta:
        db_table = 'usuarios_sin_staff'
        verbose_name = _('usuario sin staff')
        verbose_name_plural = _('usuarios sin staff')
        ordering = ['id']

    def __str__(self):
        return self.cedula 