# Generated by Django 4.0.1 on 2022-12-22 11:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0057_alter_estacion_options_alter_estacion_id_estacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntoobs',
            name='id_punto_obs',
            field=models.CharField(blank=True, default=None, help_text='Indicar únicamente en puntos REGA', max_length=4, null=True, verbose_name='ID punto de observación'),
        ),
        migrations.AlterField(
            model_name='puntoobs',
            name='latitud',
            field=models.FloatField(validators=[django.core.validators.MaxValueValidator(limit_value=90, message='Introduzca un valor entre 90º y -90º'), django.core.validators.MinValueValidator(limit_value=-90, message='Introduzca un valor entre 90º y -90º')], verbose_name='Latitud [º]'),
        ),
    ]