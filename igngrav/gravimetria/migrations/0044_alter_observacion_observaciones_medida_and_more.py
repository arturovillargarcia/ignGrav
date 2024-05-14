# Generated by Django 4.0.1 on 2022-08-16 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0043_alter_gravimetro_modelo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='observaciones_medida',
            field=models.TextField(blank=True, null=True, verbose_name='Comentarios del fichero project'),
        ),
        migrations.AlterField(
            model_name='observacion',
            name='observaciones_procesado',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Observaciones'),
        ),
    ]
