# Generated by Django 4.0.1 on 2022-01-30 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0012_observacion_observaciones_medida_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='incertidumbre_instrumental',
            field=models.FloatField(blank=True, null=True, verbose_name='Incertidumbre sistemática [μGal]'),
        ),
    ]