# Generated by Django 4.0.1 on 2022-02-02 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unidadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='isla',
            index=models.Index(fields=['com_autonoma'], name='unidadmin_i_com_aut_cc7b99_idx'),
        ),
        migrations.AddIndex(
            model_name='isla',
            index=models.Index(fields=['provincia'], name='unidadmin_i_provinc_c7b9ac_idx'),
        ),
        migrations.AddIndex(
            model_name='isla',
            index=models.Index(fields=['com_autonoma', 'provincia'], name='unidadmin_i_com_aut_2aa654_idx'),
        ),
        migrations.AddIndex(
            model_name='municipio',
            index=models.Index(fields=['com_autonoma'], name='unidadmin_m_com_aut_164650_idx'),
        ),
        migrations.AddIndex(
            model_name='municipio',
            index=models.Index(fields=['provincia'], name='unidadmin_m_provinc_604a99_idx'),
        ),
        migrations.AddIndex(
            model_name='municipio',
            index=models.Index(fields=['isla'], name='unidadmin_m_isla_id_b00c0a_idx'),
        ),
        migrations.AddIndex(
            model_name='municipio',
            index=models.Index(fields=['com_autonoma', 'provincia', 'isla'], name='unidadmin_m_com_aut_86e377_idx'),
        ),
        migrations.AddIndex(
            model_name='provincia',
            index=models.Index(fields=['com_autonoma'], name='unidadmin_p_com_aut_7f2840_idx'),
        ),
    ]