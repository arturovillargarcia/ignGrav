# Generated by Django 4.0.1 on 2022-02-15 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0026_alter_observacion_observaciones_procesado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='observaciones_medida',
            field=models.TextField(blank=True, max_length=700, null=True, verbose_name='Observaciones relativas a la medida'),
        ),
    ]
