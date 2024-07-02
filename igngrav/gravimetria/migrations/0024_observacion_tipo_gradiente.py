# Generated by Django 4.0.1 on 2022-02-09 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0023_alter_puntoobs_latitud_alter_puntoobs_longitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='observacion',
            name='tipo_gradiente',
            field=models.IntegerField(choices=[(1, 'Teórico'), (2, 'Observado')], default=1, verbose_name='Tipo de gradiente empleado'),
            preserve_default=False,
        ),
    ]