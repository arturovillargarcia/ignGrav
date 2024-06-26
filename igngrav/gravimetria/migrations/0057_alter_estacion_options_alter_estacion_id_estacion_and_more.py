# Generated by Django 4.0.1 on 2022-12-15 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0056_alter_puntoobs_id_punto_obs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estacion',
            options={'ordering': ['red_primaria', 'id_estacion'], 'verbose_name': 'estación', 'verbose_name_plural': '\t\t\t\t\t\t\t\tEstaciones'},
        ),
        migrations.AlterField(
            model_name='estacion',
            name='id_estacion',
            field=models.CharField(max_length=16, unique=True, verbose_name='ID estación'),
        ),
        migrations.AlterField(
            model_name='puntoobs',
            name='id_punto_obs',
            field=models.CharField(blank=True, default=None, help_text='Indicar únicamente en puntos REGA', max_length=4, null=True, verbose_name='ID Punto de observación'),
        ),
    ]
