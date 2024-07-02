# Generated by Django 4.1.5 on 2023-02-02 10:15

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0068_alter_observacion_punto_obs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='punto_obs',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='estacion', chained_model_field='estacion', default=None, on_delete=django.db.models.deletion.CASCADE, sort=False, to='gravimetria.puntoobs', verbose_name='Punto de observación'),
        ),
    ]