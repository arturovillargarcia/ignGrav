# Generated by Django 4.0.1 on 2022-01-06 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntoobs',
            name='descripcion',
            field=models.TextField(blank=True, max_length=400, null=True, verbose_name='Descripción'),
        ),
    ]
