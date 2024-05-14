# Generated by Django 4.0.1 on 2022-02-02 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravimetria', '0019_alter_observacion_dispersion_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='gravimetro',
            index=models.Index(fields=['tipo_gravimetro'], name='gravimetria_tipo_gr_50d6c2_idx'),
        ),
        migrations.AddIndex(
            model_name='observacion',
            index=models.Index(fields=['publicable'], name='gravimetria_publica_60c366_idx'),
        ),
        migrations.AddIndex(
            model_name='observacion',
            index=models.Index(fields=['dispersion'], name='gravimetria_dispers_d01bd3_idx'),
        ),
        migrations.AddIndex(
            model_name='observacion',
            index=models.Index(fields=['incertidumbre_total'], name='gravimetria_incerti_ca499c_idx'),
        ),
        migrations.AddIndex(
            model_name='observacion',
            index=models.Index(fields=['gravimetro_observacion'], name='gravimetria_gravime_95b975_idx'),
        ),
        migrations.AddIndex(
            model_name='observacion',
            index=models.Index(fields=['gravimetro_gradiente'], name='gravimetria_gravime_7e0106_idx'),
        ),
        migrations.AddIndex(
            model_name='observacion',
            index=models.Index(fields=['operador_procesado'], name='gravimetria_operado_330d1c_idx'),
        ),
        migrations.AddIndex(
            model_name='observacion',
            index=models.Index(fields=['estacion'], name='gravimetria_estacio_be6c9f_idx'),
        ),
    ]
