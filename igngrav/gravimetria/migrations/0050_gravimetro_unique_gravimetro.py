# Generated by Django 4.0.1 on 2022-11-28 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0049_alter_gravimetro_unique_together'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='gravimetro',
            constraint=models.UniqueConstraint(fields=('modelo', 'numero_serie'), name='unique_gravimetro'),
        ),
    ]
