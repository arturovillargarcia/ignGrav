# Generated by Django 4.0.1 on 2022-01-30 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0013_alter_observacion_incertidumbre_instrumental'),
    ]

    operations = [
        migrations.RenameField(
            model_name='observacion',
            old_name='incertidumbre_instrumental',
            new_name='incertidumbre_sistematica',
        ),
    ]