# Generated by Django 4.0.10 on 2024-07-15 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0069_alter_observacion_punto_obs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimiento',
            name='tipo_mantenimiento',
            field=models.IntegerField(choices=[(1, 'Cambio de la correa'), (2, 'Cambio de la bomba iónica'), (3, 'Mantenimiento del láser'), (4, 'Calibración del láser'), (5, 'Calibración del reloj'), (6, 'Electrónica'), (7, 'Comparación'), (8, 'Deriva de gravímetro relativo'), (9, 'Offset de los inclinómetros'), (10, 'Sensibilidad de los inclinómetros'), (11, 'Acoplamiento transversal del trípode'), (0, 'Otra')], verbose_name='Tipo de tarea realizada'),
        ),
    ]
