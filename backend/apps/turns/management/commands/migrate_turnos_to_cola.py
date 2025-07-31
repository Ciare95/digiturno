from django.core.management.base import BaseCommand
from apps.turns.models import Turno, ColaTurnos
from django.utils import timezone

class Command(BaseCommand):
    help = 'Migra turnos existentes a la tabla ColaTurnos'

    def handle(self, *args, **options):
        # Obtener turnos en espera que no tienen entrada en ColaTurnos
        turnos = Turno.objects.filter(
            estado=Turno.EstadoTurno.EN_ESPERA
        ).exclude(
            colaturnos__isnull=False
        ).select_related('servicio', 'sucursal')

        total = turnos.count()
        self.stdout.write(f'Migrando {total} turnos a ColaTurnos...')

        for i, turno in enumerate(turnos, 1):
            # Calcular posición en cola para este servicio/sucursal
            posicion = ColaTurnos.objects.filter(
                servicio=turno.servicio,
                turno__sucursal=turno.sucursal,
                activo=True
            ).count() + 1

            # Crear entrada en cola
            ColaTurnos.objects.create(
                turno=turno,
                servicio=turno.servicio,
                posicion_cola=posicion,
                tiempo_espera_estimado=5,  # Valor por defecto
                activo=True
            )

            if i % 10 == 0:
                self.stdout.write(f'Procesados {i}/{total} turnos...')

        self.stdout.write(self.style.SUCCESS(f'Migración completada. {total} turnos procesados.'))
