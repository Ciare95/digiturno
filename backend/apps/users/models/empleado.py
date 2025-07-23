from django.db import models
from django.utils.translation import gettext_lazy as _
from .usuario import Usuario

class Empleado(models.Model):
    """Modelo que representa a un empleado del sistema, vinculado a un usuario.
    Este modelo extiende las funcionalidades del usuario para incluir información específica del empleado."""
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='perfil_empleado'
    )
    codigo_empleado = models.CharField(_("código de empleado"), max_length=20, unique=True)
    
    sucursal = models.ForeignKey(
        'core.Sucursal',
        on_delete=models.SET_NULL,  
        verbose_name=_("sucursal"),
        null=True,
        blank=True
    )
    
    servicios = models.ManyToManyField(
        'core.Servicio',
        through='EmpleadoServicio',  
        related_name='empleados',
        verbose_name=_("servicios asignados"),
        blank=True
    )
    
    ventanilla_asignada = models.CharField(_("ventanilla asignada"), max_length=10)
    estado_conexion = models.CharField(
        _("estado de conexión"),
        max_length=20,
        choices=[('desconectado', 'Desconectado'), ('conectado', 'Conectado')],
        default='desconectado'
    )
    fecha_ingreso = models.DateField(_("fecha de ingreso"), blank=True, null=True)
    configuracion_ui = models.JSONField(_("configuración UI"), default=dict, blank=True)

    class Meta:
        db_table = 'empleados'
        verbose_name = _('empleado')
        verbose_name_plural = _('empleados')
        ordering = ['usuario__username']

    def __str__(self):
        return f"{self.usuario.username} ({self.codigo_empleado})" 