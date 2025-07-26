from django.core.management.base import BaseCommand
from apps.core.models import DiasSemana

class Command(BaseCommand):
    help = 'Crea los días de la semana si no existen'

    def handle(self, *args, **kwargs):
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        creados = 0

        for nombre in dias:
            DiasSemana.objects.get_or_create(nombre=nombre)
            creados += 1

        self.stdout.write(self.style.SUCCESS(f'Se insertaron {creados} días de la semana.'))
