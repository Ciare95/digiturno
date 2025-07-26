from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    telefono = models.CharField(_("teléfono"), max_length=15, blank=True, null=True)
    cedula = models.CharField(_("cédula"), max_length=20, unique=True, blank=True, null=True)
    ultimo_acceso = models.DateTimeField(_("último acceso"), blank=True, null=True)

    class Meta:
        db_table = 'usuarios' 
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        ordering = ['id']

    def __str__(self):
        return self.username

    def get_nombre_completo(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def nombre_completo(self):
        return self.get_nombre_completo()
