# Generated by Django 4.0.1 on 2022-01-30 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0011_alter_mantenimiento_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='observacion',
            name='observaciones_medida',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observaciones relativas a la medida'),
        ),
        migrations.AddField(
            model_name='observacion',
            name='observaciones_procesado',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observaciones relativas al procesado'),
        ),
    ]
