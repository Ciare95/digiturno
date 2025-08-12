from django.db import migrations

def seed_dias(apps, schema_editor):
    DiaSemana = apps.get_model('core', 'DiasSemana')
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    for dia in dias:
        DiaSemana.objects.get_or_create(nombre=dia)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_diassemana_sucursal_descripcion'),  # ajusta al nombre de tu migración inicial
    ]

    operations = [
        migrations.RunPython(seed_dias),
    ]
