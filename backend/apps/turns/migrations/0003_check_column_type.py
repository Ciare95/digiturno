from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0002_alter_calificacionservicio_empleado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='tiempo_espera_estimado',
            field=models.DurationField(blank=True, null=True, verbose_name='tiempo de espera estimado'),
        ),
    ]
