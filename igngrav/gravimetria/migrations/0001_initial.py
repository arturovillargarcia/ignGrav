# Generated by Django 4.0.1 on 2022-01-05 12:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import gravimetria.auxiliary_functions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hojasmtn', '0001_initial'),
        ('unidadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_estacion', models.CharField(help_text='Identificador de la estación siguiendo el formato PROV_MUNI', max_length=16, unique=True, verbose_name='ID estación')),
                ('nombre', models.CharField(help_text='Denominación descriptiva de la estación', max_length=128, verbose_name='Nombre')),
                ('direccion', models.CharField(blank=True, max_length=254, null=True, verbose_name='Dirección postal')),
                ('geom', django.contrib.gis.db.models.fields.MultiPointField(blank=True, null=True, srid=4326, verbose_name='Localización')),
                ('com_autonoma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidadmin.comautonoma', verbose_name='Comunidad autónoma')),
                ('hoja_mtn25', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hojasmtn.hojamtn25', verbose_name='Hoja MTN25')),
                ('hoja_mtn50', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hojasmtn.hojamtn50', verbose_name='Hoja MTN50')),
                ('isla', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidadmin.isla', verbose_name='Isla')),
                ('municipio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidadmin.municipio', verbose_name='Municipio')),
                ('pais', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidadmin.pais', verbose_name='País')),
                ('provincia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidadmin.provincia', verbose_name='Provincia')),
            ],
            options={
                'verbose_name': 'estación',
                'verbose_name_plural': '\t\t\t\t\t\t\tEstaciones',
                'ordering': ['id_estacion'],
            },
        ),
        migrations.CreateModel(
            name='Gravimetro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.IntegerField(choices=[(1, 'A10'), (2, 'FG5'), (3, 'LRG'), (4, 'gPhone'), (5, 'gPhoneX'), (6, 'CG5')], verbose_name='Modelo')),
                ('numero_serie', models.CharField(max_length=4, verbose_name='Número de serie')),
                ('tipo_gravimetro', models.IntegerField(choices=[(1, 'Absoluto'), (2, 'Relativo')], verbose_name='Tipo de gravímetro')),
                ('manual', models.FileField(blank=True, max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_manuales, verbose_name='Manual del gravímetro')),
                ('ultimo_mantenimiento', models.DateField(blank=True, help_text='Fecha en la que se envió el gravímetro para realizar             tareas de mantenimiento por última vez', null=True, verbose_name='Último mantenimiento')),
            ],
            options={
                'verbose_name': 'gravímetro',
                'verbose_name_plural': '\t\tGravímetros',
                'ordering': ['institucion', 'modelo', 'numero_serie'],
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=16, unique=True, verbose_name='Institución o empresa')),
                ('nombre_completo', models.CharField(max_length=128, unique=True, verbose_name='Nombre completo')),
                ('web', models.URLField(blank=True, null=True, verbose_name='Página web')),
            ],
            options={
                'verbose_name': 'institución',
                'verbose_name_plural': '\t\t\t\tInstituciones',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Red',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=16, unique=True, verbose_name='Red')),
                ('nombre_completo', models.CharField(max_length=128, unique=True, verbose_name='Nombre completo')),
                ('web', models.URLField(blank=True, null=True, verbose_name='Página web')),
            ],
            options={
                'verbose_name': 'red',
                'verbose_name_plural': '\t\t\tRedes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='PuntoObs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_punto_obs', models.CharField(help_text='AA, BB... para puntos no monumentalizados; P1, Pn... para pilares', max_length=3, verbose_name='ID Punto de observación')),
                ('nombre', models.CharField(blank=True, help_text='Indicar únicamente en estaciones con múltiples puntos de observación', max_length=128, null=True, verbose_name='Nombre')),
                ('tipo_senal', models.IntegerField(choices=[(1, 'Pilar'), (2, 'Clavo'), (3, 'Marca'), (4, 'Sin señalizar'), (5, 'Desconocido')], verbose_name='Tipo de señalización')),
                ('estado_senal', models.IntegerField(choices=[(1, 'Buen estado'), (2, 'Mal estado'), (3, 'Desconocido')], verbose_name='Estado de la señal')),
                ('fecha_revision', models.DateField(blank=True, null=True, verbose_name='Fecha de revisión')),
                ('tipo_acceso', models.IntegerField(choices=[(1, 'Público'), (2, 'Privado'), (3, 'Desconocido')], verbose_name='Tipo de acceso')),
                ('latitud', models.FloatField(blank=True, null=True, verbose_name='Latitud [º]')),
                ('longitud', models.FloatField(blank=True, null=True, verbose_name='Longitud [º]')),
                ('altitud', models.FloatField(blank=True, null=True, verbose_name='Altitud ortométrica [m]')),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Localización')),
                ('utm_x', models.FloatField(blank=True, null=True, verbose_name='UTM X [m]')),
                ('utm_y', models.FloatField(blank=True, null=True, verbose_name='UTM Y [m]')),
                ('utm_zona', models.CharField(blank=True, max_length=3, null=True, verbose_name='Zona UTM')),
                ('descripcion', models.TextField(max_length=400, verbose_name='Descripción')),
                ('imagen_nw', models.ImageField(blank=True, max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_imagenes, verbose_name='Imagen superior izquierda')),
                ('imagen_ne', models.ImageField(blank=True, max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_imagenes, verbose_name='Imagen superior derecha')),
                ('imagen_sw', models.ImageField(blank=True, max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_imagenes, verbose_name='Imagen inferior izquierda')),
                ('imagen_se', models.ImageField(blank=True, max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_imagenes, verbose_name='Imagen inferior derecha')),
                ('estacion', models.ForeignKey(help_text='ID de la estación a la que pertenece', on_delete=django.db.models.deletion.CASCADE, to='gravimetria.estacion')),
            ],
            options={
                'verbose_name': 'punto de observación',
                'verbose_name_plural': '\t\t\t\t\t\tPuntos de observación',
                'ordering': ['estacion', 'id_punto_obs'],
                'unique_together': {('estacion', 'id_punto_obs')},
            },
        ),
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=16, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('institucion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gravimetria.institucion', verbose_name='Institución o empresa a la que pertenece')),
            ],
            options={
                'verbose_name': 'operador',
                'verbose_name_plural': '\tOperadores',
                'ordering': ['nombre', 'apellidos'],
            },
        ),
        migrations.CreateModel(
            name='Observacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publicable', models.BooleanField(verbose_name='Publicable')),
                ('fichero_project', models.FileField(blank=True, help_text='Se debe guardar y continuar para que rellene             automaticamente los campos asociados', max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_ficheros_g, verbose_name='Fichero project')),
                ('fichero_set', models.FileField(blank=True, max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_ficheros_g, verbose_name='Fichero set')),
                ('fichero_drop', models.FileField(blank=True, max_length=200, null=True, upload_to=gravimetria.auxiliary_functions.ruta_ficheros_g, verbose_name='Fichero drop')),
                ('fecha_observacion', models.DateField(blank=True, null=True, verbose_name='Fecha de observación')),
                ('fecha_procesado', models.DateField(blank=True, null=True, verbose_name='Fecha de procesado')),
                ('observaciones', models.TextField(blank=True, max_length=400, null=True, verbose_name='Observaciones')),
                ('gradiente_vertical', models.FloatField(blank=True, null=True, verbose_name='Gradiente vertical de la gravedad [μGal/cm]')),
                ('gravedad', models.FloatField(blank=True, null=True, verbose_name='Gravedad [μGal]')),
                ('dispersion', models.FloatField(blank=True, null=True, verbose_name='Dispersión entre sets [μGal]')),
                ('incertidumbre_medida', models.FloatField(blank=True, null=True, verbose_name='Incertidumbre de la observación [μGal]')),
                ('incertidumbre_instrumental', models.FloatField(blank=True, null=True, verbose_name='Incertidumbre instrumental [μGal]')),
                ('incertidumbre_total', models.FloatField(blank=True, null=True, verbose_name='Incertidumbre total [μGal]')),
                ('sets_observados', models.IntegerField(blank=True, null=True, verbose_name='Número de sets observados')),
                ('sets_procesados', models.IntegerField(blank=True, null=True, verbose_name='Número de sets procesados')),
                ('drops_por_set', models.IntegerField(blank=True, null=True, verbose_name='Número de caídas por set')),
                ('altura_de_montaje', models.FloatField(blank=True, null=True, verbose_name='Altura de montaje [cm]')),
                ('altura_de_observacion', models.FloatField(blank=True, null=True, verbose_name='Altura de observación [cm]')),
                ('altura_de_procesado', models.FloatField(blank=True, null=True, verbose_name='Altura de procesado [cm]')),
                ('gravedad_cero', models.FloatField(blank=True, null=True, verbose_name='Gravedad a 0 cm [μGal]')),
                ('estacion', models.ForeignKey(help_text='ID de la estación a la que pertenece', on_delete=django.db.models.deletion.CASCADE, to='gravimetria.estacion', verbose_name='Estación')),
                ('gravimetro_gradiente', models.ForeignKey(blank=True, limit_choices_to={'tipo_gravimetro': 2}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gravimetro_gradiente', to='gravimetria.gravimetro', verbose_name='Gravímetro empleado en la observación del gradiente')),
                ('gravimetro_observacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gravimetro_observacion', to='gravimetria.gravimetro', verbose_name='Gravímetro')),
                ('operador_observacion', models.ManyToManyField(blank=True, related_name='operador_observacion', to='gravimetria.Operador', verbose_name='Operadores que realizaron la observación')),
                ('operador_procesado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operador_procesado', to='gravimetria.operador', verbose_name='Operador que realizó el último procesado')),
                ('punto_obs', models.ForeignKey(blank=True, help_text='Se debe guardar la estación para que aparezcan             los puntos de observación asociados', null=True, on_delete=django.db.models.deletion.CASCADE, to='gravimetria.puntoobs', verbose_name='Punto de observación')),
            ],
            options={
                'verbose_name': 'observación',
                'verbose_name_plural': '\t\t\t\t\tObservaciones',
                'ordering': ['estacion', 'punto_obs', '-fecha_observacion'],
            },
        ),
        migrations.AddField(
            model_name='gravimetro',
            name='institucion',
            field=models.ForeignKey(default=None, help_text='Institución o empresa a la que pertenece el gravímetro', on_delete=django.db.models.deletion.SET_DEFAULT, to='gravimetria.institucion', verbose_name='Institución'),
        ),
        migrations.AddField(
            model_name='estacion',
            name='red_primaria',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('nombre', 'REGA')), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='red_primaria', to='gravimetria.red', verbose_name='Red primaria'),
        ),
        migrations.AddField(
            model_name='estacion',
            name='red_secundaria',
            field=models.ManyToManyField(blank=True, help_text='Otras redes a las que pertenece o con las que enlaza la estación', limit_choices_to=models.Q(('nombre', 'REGA'), _negated=True), related_name='red_secundaria', to='gravimetria.Red', verbose_name='Redes secundarias'),
        ),
        migrations.AlterUniqueTogether(
            name='gravimetro',
            unique_together={('modelo', 'numero_serie')},
        ),
    ]
