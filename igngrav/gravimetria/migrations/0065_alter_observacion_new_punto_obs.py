# Generated by Django 4.1.5 on 2023-02-01 13:07

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0064_observacion_new_punto_obs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='new_punto_obs',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='estacion', chained_model_field='estacion', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newpuntoobs', sort=False, to='gravimetria.puntoobs'),
        ),
    ]