# Generated by Django 4.1.5 on 2023-02-01 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0062_alter_observacion_new_punto_obs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observacion',
            name='new_punto_obs',
        ),
    ]
