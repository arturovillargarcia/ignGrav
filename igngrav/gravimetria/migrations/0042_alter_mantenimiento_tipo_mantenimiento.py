# Generated by Django 4.0.1 on 2022-07-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0041_alter_gravimetro_modelo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimiento',
            name='tipo_mantenimiento',
            field=models.IntegerField(choices=[(1, 'Cambio de la correa'), (2, 'Cambio de la bomba iónica'), (3, 'Mantenimiento del láser'), (4, 'Calibración del láser'), (5, 'Calibración del reloj'), (6, 'Electrónica'), (7, 'Comparación'), (8, 'Deriva de gravímetro relativo'), (9, 'Otra')], verbose_name='Tipo de tarea realizada'),
        ),
    ]
