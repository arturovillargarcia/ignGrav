# Generated by Django 4.0.1 on 2022-11-24 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hojasmtn', '0002_alter_hojamtn25_hoja_alter_hojamtn25_nombre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hojamtn25',
            name='hoja',
            field=models.CharField(max_length=128, verbose_name='Número de hoja'),
        ),
    ]
