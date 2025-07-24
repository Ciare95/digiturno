from django.db import models

class DiasSemana(models.Model):
    nombre = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'dias_semana'
        verbose_name = 'dia de la semana'
        verbose_name_plural = 'dias de la semana'