# Generated by Django 4.0.1 on 2022-01-30 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0009_alter_estacion_options_alter_gravimetro_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mantenimiento',
            options={'ordering': ['gravimetro', '-fecha_mantenimiento'], 'verbose_name': 'mantenimiento', 'verbose_name_plural': '\t\tMantenimiento'},
        ),
        migrations.RenameField(
            model_name='mantenimiento',
            old_name='gravímetro',
            new_name='gravimetro',
        ),
    ]