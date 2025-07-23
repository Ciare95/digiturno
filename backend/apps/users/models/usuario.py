from django.contrib.auth.models import AbstractUser
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
    
    
class EmpleadoServicio(models.Model):
    """Tabla intermedia para la relación empleado-servicio"""
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        related_name='asignaciones_servicio'
    )
    servicio = models.ForeignKey(
        'core.Servicio',
        on_delete=models.CASCADE,
        related_name='asignaciones_empleado'
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'empleados_servicios'
        verbose_name = _('empleado servicio')
        verbose_name_plural = _('empleados servicios')
        unique_together = ('empleado', 'servicio')

    def __str__(self):
        return f"{self.empleado.codigo_empleado} - {self.servicio.nombre}"
