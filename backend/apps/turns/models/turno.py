from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models.usuario import Usuario
from apps.users.models.empleado import Empleado  # Importar Empleado desde users
from apps.core.models.servicio import Servicio
from apps.core.models.sucursal import Sucursal
from apps.turns.services.logic import GestorTurnos
from django.core.exceptions import ValidationError
from django.utils import timezone

class Turno(models.Model):
    class EstadoTurno(models.TextChoices):
        EN_ESPERA = 'en_espera', 'En Espera'
        LLAMADO = 'llamado', 'Llamado'
        EN_ATENCION = 'en_atencion', 'En Atención'
        FINALIZADO = 'finalizado', 'Finalizado'
        CANCELADO = 'cancelado', 'Cancelado'
        AUSENTE = 'ausente', 'Ausente'

    numero_turno = models.CharField(_('número de turno'), max_length=20)
    servicio = models.ForeignKey(
        'core.Servicio',
        on_delete=models.CASCADE,
        verbose_name=_('servicio')
    )

    sucursal = models.ForeignKey(
        'core.Sucursal',
        on_delete=models.CASCADE,
        verbose_name=_('sucursal')
    )

    nombre_cliente = models.CharField('nombre del cliente', max_length=100, default="", blank=True)

    numero_cedula = models.CharField('número de cédula', max_length=20, default="", blank=True)

    estado = models.CharField(
        max_length=20,
        choices=EstadoTurno.choices,
        default=EstadoTurno.EN_ESPERA,
        verbose_name=_('estado')
    )
    
    fecha_creacion = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    fecha_inicio_atencion = models.DateTimeField(_('fecha de inicio de atención'), null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(_('fecha de finalización'), null=True, blank=True)
    empleado = models.ForeignKey(
        'users.Empleado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='turnos_atendidos'
    )

    class Meta:
        db_table = 'turnos'
        verbose_name = _('turno')
        verbose_name_plural = _('turnos')
        ordering = ['-fecha_creacion']
    def __str__(self):
        return f"Turno {self.numero_turno} - {self.servicio.nombre}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.numero_turno:
            self.numero_turno = GestorTurnos.generar_numero_turno(self.servicio, self.sucursal)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.numero_cedula:
            hoy = timezone.now().date()
            existe = Turno.objects.filter(
                numero_cedula=self.numero_cedula,
                servicio=self.servicio,
                sucursal=self.sucursal,
                fecha_creacion__date=hoy
            ).exclude(
                estado=Turno.EstadoTurno.FINALIZADO
            ).exclude(
                pk=self.pk
            ).exists()
            if existe:
                raise ValidationError(
                    "Ya existe un turno para esta cédula, servicio y sucursal en el día de hoy. "
                    "Solo puede sacar otro si el anterior está FINALIZADO."
                )
