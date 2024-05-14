# Generated by Django 4.0.1 on 2022-11-28 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0050_gravimetro_unique_gravimetro'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='estacion',
            name='gravimetria_com_aut_c7b853_idx',
        ),
        migrations.RemoveIndex(
            model_name='estacion',
            name='gravimetria_provinc_5c31ab_idx',
        ),
        migrations.RemoveIndex(
            model_name='estacion',
            name='gravimetria_isla_id_1ad074_idx',
        ),
        migrations.RemoveIndex(
            model_name='estacion',
            name='gravimetria_com_aut_c1f3ac_idx',
        ),
        migrations.RemoveIndex(
            model_name='estacion',
            name='gravimetria_com_aut_aab528_idx',
        ),
        migrations.RemoveIndex(
            model_name='estacion',
            name='gravimetria_com_aut_aed226_idx',
        ),
    ]
