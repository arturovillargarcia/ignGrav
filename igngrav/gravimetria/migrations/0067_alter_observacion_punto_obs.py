# Generated by Django 4.1.5 on 2023-02-01 13:19

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0066_remove_observacion_new_punto_obs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='punto_obs',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='estacion', chained_model_field='estacion', help_text='Se debe guardar la estación para que aparezcan             los puntos de observación asociados', null=True, on_delete=django.db.models.deletion.CASCADE, sort=False, to='gravimetria.puntoobs', verbose_name='Punto de observación'),
        ),
    ]