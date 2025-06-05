from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    # AbstractUser ya incluye: username, first_name, last_name, email, password,
    # is_staff, is_active, date_joined.
    # Campos de tu tabla 'usuarios' que no están directamente en AbstractUser o que queremos añadir:
    telefono = models.CharField(_("teléfono"), max_length=15, blank=True, null=True)
    cedula = models.CharField(_("cédula"), max_length=20, unique=True, blank=True, null=True)
    ultimo_acceso = models.DateTimeField(_("último acceso"), blank=True, null=True)

    # Si deseas usar el email como campo de login principal:
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username'] # O solo ['first_name', 'last_name'] si email es username

    class Meta:
        db_table = 'usuarios' # Para mapear a tu tabla PostgreSQL existente
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
    # Usamos OneToOneField para extender el modelo Usuario.
    # 'usuario_id' en tu SQL se convierte en una relación OneToOne.
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        primary_key=True, # Esto hace que el ID del empleado sea el mismo que el ID del usuario
        related_name='perfil_empleado'
    )
    codigo_empleado = models.CharField(_("código de empleado"), max_length=20, unique=True)
    # La sucursal_id es una ForeignKey. Usamos la forma de string 'app_label.ModelName'
    # para evitar importaciones circulares si 'core' también importa 'users'.
    sucursal = models.ForeignKey(
        'core.Sucursal',
        on_delete=models.SET_NULL, # O models.PROTECT, models.CASCADE según tu lógica de negocio
        null=True,
        blank=True,
        verbose_name=_("sucursal")
    )
    ventanilla_asignada = models.CharField(_("ventanilla asignada"), max_length=10, blank=True, null=True)
    estado_conexion = models.CharField(
        _("estado de conexión"),
        max_length=20,
        choices=[('desconectado', 'Desconectado'), ('conectado', 'Conectado')],
        default='desconectado'
    )
    fecha_ingreso = models.DateField(_("fecha de ingreso"), blank=True, null=True)
    # El campo 'activo' de tu tabla 'empleados' puede ser manejado por el 'is_active' del Usuario,
    # o puedes añadir un campo booleano específico aquí si tiene un significado diferente.
    # activo_empleado = models.BooleanField(default=True)
    configuracion_ui = models.JSONField(_("configuración UI"), default=dict, blank=True)
    # created_at y updated_at pueden ser añadidos con auto_now_add=True y auto_now=True

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
    # 'usuario_id' en tu SQL.
    nivel_acceso = models.CharField(_("nivel de acceso"), max_length=20, default='admin')
    permisos = models.JSONField(_("permisos"), default=dict, blank=True)
    sucursal = models.ForeignKey(
        'core.Sucursal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("sucursal")
    )
    # El campo 'activo' de tu tabla 'administradores'.
    # activo_admin = models.BooleanField(default=True)

    class Meta:
        db_table = 'administradores'
        verbose_name = _('administrador')
        verbose_name_plural = _('administradores')
        ordering = ['usuario__username']

    def __str__(self):
        return f"{self.usuario.username} (Admin)"
