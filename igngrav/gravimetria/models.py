from audioop import reverse
from dataclasses import fields
from datetime import datetime, date
from dateutil import relativedelta
from random import choices
from tabnanny import verbose
from django.contrib.admin.decorators import display
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, MultiPoint
from django.core import validators
from django.db.models import Q
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from gravimetria.auxiliary_functions import extracción_fichero_project, \
    ruta_ficheros_g, ruta_manuales, ruta_imagenes, ruta_mantenimiento, \
    extraccion_fecha_observacion
from hojasmtn.models import HojaMtn25, HojaMtn50
from math import sqrt
from smart_selects.db_fields import ChainedForeignKey
from unidadmin.models import Pais, ComAutonoma, Provincia, Isla, Municipio


# Create your models here.
class Institucion(models.Model):
    nombre = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="Institución o empresa"
    )
    nombre_completo = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Nombre completo"

    )    
    web = models.URLField(
        verbose_name="Página web",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "institución"
        verbose_name_plural = "\t\t\t\t\tInstituciones"

    @display(description="Operadores")
    def operadores_link(self):
        num_operadores = len(self.operador_set.all())
        if num_operadores == 1:
            return format_html(
                f"<a href='/admin/gravimetria/operador/?institucion__id__exact={self.pk}'>\
                Ver operador</a>"
            )
        elif num_operadores > 1:
            return format_html(
                f"<a href='/admin/gravimetria/operador/?institucion__id__exact={self.pk}'>\
                Ver sus {num_operadores} operadores</a>"
            )
        else:
            pass

    @display(description="Página web")
    def web_link(self):
        if self.web:
            return format_html(f"<a href='{self.web}'>{self.web}</a>")
        else:
            pass

    def __str__(self):
        return self.nombre


class Red(models.Model):
    nombre = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="Red"
    )
    nombre_completo = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Nombre completo"
    )
    web = models.URLField(
        verbose_name="Página web",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "red"
        verbose_name_plural = "\t\t\t\tRedes"

    @display(description="Estaciones como red primaria")
    def estaciones_red_primaria_link(self):
        num_estaciones = len(Estacion.objects.filter(red_primaria=self))
        if num_estaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?red_primaria__id__exact={self.pk}'>\
                Ver estación</a>"
            )
        elif num_estaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?red_primaria__id__exact={self.pk}'>\
                Ver sus {num_estaciones} estaciones</a>"
            )
        else:
            pass

    @display(description="Estaciones como red secundaria")
    def estaciones_red_secundaria_link(self):
        num_estaciones = len(Estacion.objects.filter(red_secundaria=self))
        if num_estaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?red_secundaria__id__exact={self.pk}'>\
                Ver estación</a>"
            )
        elif num_estaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?red_secundaria__id__exact={self.pk}'>\
                Ver sus {num_estaciones} estaciones</a>"
            )
        else:
            pass

    @display(description="Página web")
    def web_link(self):
        if self.web:
            return format_html(f"<a href='{self.web}'>{self.web}</a>")
        else:
            pass

    def __str__(self):
        return self.nombre


class Gravimetro(models.Model):
    MODELOS = [
        (1, "A10"),
        (2, "FG5"),
        (3, "LRG"),
        (4, "gPhone"),
        (5, "gPhoneX"),
        (6, "CG5"),
        (7, "B"),
        (8, "LRD"),
        (9, "JILAG")
    ]
    TIPOS = [
        (1, "Absoluto"),
        (2, "Relativo")
    ]
    modelo = models.IntegerField(
        verbose_name="Modelo",
        choices=MODELOS
    )
    numero_serie = models.CharField(
        max_length=8,
        verbose_name="Número de serie"
    )
    tipo_gravimetro = models.IntegerField(
        choices=TIPOS,
        verbose_name="Tipo de gravímetro"
    )
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_DEFAULT,
        default=None,
        verbose_name="Institución",
    )
    manual = models.FileField(
        max_length=200,
        upload_to=ruta_manuales,
        verbose_name="Manual del gravímetro",
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["modelo", "numero_serie"],
                name="unique_gravimetro"
                )
        ]
        indexes = [
            models.Index(fields=["tipo_gravimetro"])
        ]
        ordering = ["institucion", "modelo", "numero_serie"]
        verbose_name = "gravímetro"
        verbose_name_plural = "\t\t\tGravímetros"

    @display(description="Institución")
    def institucion_link(self):
        if self.institucion:
            return format_html(
                f"<a href='/admin/gravimetria/institucion/{self.institucion.pk}/change/'>\
                {self.institucion}</a>"
            )
        else:
            pass

    @display(description="Manual")
    def manual_modelo_link(self):
        if self.manual:
            return format_html(
                f"<a href='/media/MANUALES/{self.get_modelo_display()}%23{self.numero_serie}/{self.manual.name.split('/')[-1]}'>{self.manual.name.split('/')[-1]}</a>"
            )
        else:
            pass

    def __str__(self):
        return f"{self.get_modelo_display()}#{self.numero_serie}"

    @display(description="Mantenimiento")
    def mantenimiento_link(self):
        tareas_mantenimiento = len(self.mantenimiento_set.all())
        if tareas_mantenimiento == 1:
            return format_html(
                f"<a href='/admin/gravimetria/mantenimiento/?gravimetro__id__exact={self.pk}'>\
                Ver tarea realizada</a>"                
            )
        elif tareas_mantenimiento > 1:
            return format_html(
                f"<a href='/admin/gravimetria/mantenimiento/?gravimetro__id__exact={self.pk}'>\
                Ver {tareas_mantenimiento} tareas realizadas</a>"                
            )
        else:
            pass

    @display(description="Último cambio de la correa")
    def cambio_correa_display(self):
        ultimo_cambio_correa = Mantenimiento.objects.filter(gravimetro=self.pk).filter(
            tipo_mantenimiento=1).latest("fecha_mantenimiento")
        if ultimo_cambio_correa:
            fecha_mantenimiento = ultimo_cambio_correa.fecha_mantenimiento
            fecha_actual = date.today()
            fecha_delta = relativedelta.relativedelta(fecha_actual, fecha_mantenimiento)
            años = fecha_delta.years
            meses = fecha_delta.months
            dias = fecha_delta.days
            observaciones = Observacion.objects.filter(gravimetro_observacion=self.pk).filter(
                fecha_observacion__gte=fecha_mantenimiento
            )
            total_caidas = 0
            for observacion in observaciones:
                sets_observados = observacion.sets_observados
                drops_por_set = observacion.drops_por_set
                caidas = sets_observados * drops_por_set
                total_caidas += caidas
            if años > 0:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {años} años y {meses} meses)"
            elif meses > 0: 
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {meses} meses)"
            else:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {dias} dias)"
        else:
            pass

    @display(description="Último cambio de la bomba iónica")
    def cambio_bomba_display(self):
        ultimo_cambio_bomba = Mantenimiento.objects.filter(gravimetro=self.pk).filter(
            tipo_mantenimiento=2).latest("fecha_mantenimiento")
        if ultimo_cambio_bomba:
            fecha_mantenimiento = ultimo_cambio_bomba.fecha_mantenimiento
            fecha_actual = date.today()
            fecha_delta = relativedelta.relativedelta(fecha_actual, fecha_mantenimiento)
            años = fecha_delta.years
            meses = fecha_delta.months
            dias = fecha_delta.days
            observaciones = Observacion.objects.filter(gravimetro_observacion=self.pk).filter(
                fecha_observacion__gte=fecha_mantenimiento
            )
            total_caidas = 0
            for observacion in observaciones:
                sets_observados = observacion.sets_observados
                drops_por_set = observacion.drops_por_set
                caidas = sets_observados * drops_por_set
                total_caidas += caidas
            if años > 0:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {años} años y {meses} meses)"
            elif meses > 0: 
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {meses} meses)"
            else:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {dias} dias)"
        else:
            pass

    @display(description="Último mantenimiento del láser")
    def mantenimiento_laser_display(self):
        ultimo_mantenimiento_laser = Mantenimiento.objects.filter(gravimetro=self.pk).filter(
            tipo_mantenimiento=3).latest("fecha_mantenimiento")
        if ultimo_mantenimiento_laser:
            fecha_mantenimiento = ultimo_mantenimiento_laser.fecha_mantenimiento
            fecha_actual = date.today()
            fecha_delta = relativedelta.relativedelta(fecha_actual, fecha_mantenimiento)
            años = fecha_delta.years
            meses = fecha_delta.months
            dias = fecha_delta.days
            observaciones = Observacion.objects.filter(gravimetro_observacion=self.pk).filter(
                fecha_observacion__gte=fecha_mantenimiento
            )
            total_caidas = 0
            for observacion in observaciones:
                sets_observados = observacion.sets_observados
                drops_por_set = observacion.drops_por_set
                caidas = sets_observados * drops_por_set
                total_caidas += caidas
            if años > 0:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {años} años y {meses} meses)"
            elif meses > 0: 
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {meses} meses)"
            else:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {dias} dias)"        
        else:
            pass

    @display(description="Última calibración del láser")
    def calibracion_laser_display(self):
        ultima_calibracion_laser = Mantenimiento.objects.filter(gravimetro=self.pk).filter(
            tipo_mantenimiento=4).latest("fecha_mantenimiento")
        if ultima_calibracion_laser:
            fecha_mantenimiento = ultima_calibracion_laser.fecha_mantenimiento
            fecha_actual = date.today()
            fecha_delta = relativedelta.relativedelta(fecha_actual, fecha_mantenimiento)
            años = fecha_delta.years
            meses = fecha_delta.months
            dias = fecha_delta.days
            observaciones = Observacion.objects.filter(gravimetro_observacion=self.pk).filter(
                fecha_observacion__gte=fecha_mantenimiento
            )
            total_caidas = 0
            for observacion in observaciones:
                sets_observados = observacion.sets_observados
                drops_por_set = observacion.drops_por_set
                caidas = sets_observados * drops_por_set
                total_caidas += caidas
            if años > 0:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {años} años y {meses} meses)"
            elif meses > 0: 
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {meses} meses)"
            else:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {dias} dias)"        
        else:
            pass

    @display(description="Última calibración del reloj")
    def calibracion_reloj_display(self):
        ultima_calibracion_reloj = Mantenimiento.objects.filter(gravimetro=self.pk).filter(
            tipo_mantenimiento=5).latest("fecha_mantenimiento")
        if ultima_calibracion_reloj:
            fecha_mantenimiento = ultima_calibracion_reloj.fecha_mantenimiento
            fecha_actual = date.today()
            fecha_delta = relativedelta.relativedelta(fecha_actual, fecha_mantenimiento)
            años = fecha_delta.years
            meses = fecha_delta.months
            dias = fecha_delta.days
            observaciones = Observacion.objects.filter(gravimetro_observacion=self.pk).filter(
                fecha_observacion__gte=fecha_mantenimiento
            )
            total_caidas = 0
            for observacion in observaciones:
                sets_observados = observacion.sets_observados
                drops_por_set = observacion.drops_por_set
                caidas = sets_observados * drops_por_set
                total_caidas += caidas
            if años > 0:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {años} años y {meses} meses)"
            elif meses > 0: 
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {meses} meses)"
            else:
                return f"{datetime.strftime(fecha_mantenimiento, '%d/%m/%Y')} " \
                    + f"({total_caidas} caídas; {dias} dias)"        
        else:
            pass


class Mantenimiento(models.Model):
    TIPO_MANTENIMIENTO = [
        (1, "Cambio de la correa"),
        (2, "Cambio de la bomba iónica"),
        (3, "Mantenimiento del láser"),
        (4, "Calibración del láser"),
        (5, "Calibración del reloj"),
        (6, "Electrónica"),
        (7, "Comparación"),
        (8, "Deriva de gravímetro relativo"),
        (9, "Offset de los inclinómetros"),
        (10, "Sensibilidad de los inclinómetros"),
        (11, "Acoplamiento transversal del trípode"),
        (0, "Otra")
    ]
    gravimetro = models.ForeignKey(
        Gravimetro, 
        on_delete=models.CASCADE,
        verbose_name="Gravímetro"
    )
    tipo_mantenimiento = models.IntegerField(
        choices=TIPO_MANTENIMIENTO,
        verbose_name="Tipo de tarea realizada"
    )
    fecha_mantenimiento = models.DateField(
        verbose_name="Fecha"
    )
    observaciones = models.TextField(
        verbose_name="Observaciones",
        blank=True,
        null=True
    )
    fichero_mantenimiento =  models.FileField(
        max_length=200,
        upload_to=ruta_mantenimiento,
        verbose_name="Fichero",
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gravimetro", "tipo_mantenimiento", "fecha_mantenimiento"],
                name="unique_mantenimiento"
                )
        ]
        indexes = [
            models.Index(fields=["gravimetro"]),
            models.Index(fields=["tipo_mantenimiento"])
        ]
        ordering = ["gravimetro", "-fecha_mantenimiento", "tipo_mantenimiento"]
        verbose_name = "tarea de mantenimiento"
        verbose_name_plural = "\t\tMantenimiento"

    @display(description="Gravímetro")
    def gravimetro_link(self):
        if self.gravimetro:
            return format_html(
                f"<a href='/admin/gravimetria/gravimetro/{self.gravimetro.pk}/change/'>\
                {self.gravimetro}</a>"                
            )
        else:
            pass

    @display(description="Fecha")
    def fecha_mantenimiento_display(self):
        return datetime.strftime(self.fecha_mantenimiento, "%d/%m/%Y")

    @display(description="Fichero")
    def fichero_mantenimiento_link(self):
        if self.fichero_mantenimiento:
            return format_html(
                f"<a href='/media/MANTENIMIENTO/{self.gravimetro.get_modelo_display()}%23{self.gravimetro.numero_serie}/{self.fichero_mantenimiento.name.split('/')[-1]}'>{self.fichero_mantenimiento.name.split('/')[-1]}</a>"
            )

    def __str__(self):
        return ""

class Operador(models.Model):
    nombre = models.CharField(
        max_length=16,
        verbose_name="Nombre"
    )
    apellidos = models.CharField(
        max_length=50,
        verbose_name="Apellidos"
    )
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.SET_NULL,
        verbose_name="Institución o empresa a la que pertenece",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["nombre", "apellidos"]
        verbose_name = "operador"
        verbose_name_plural = "\tOperadores"

    @display(description="Institución")
    def institucion_link(self):
        if self.institucion:
            return format_html(
                f"<a href='/admin/gravimetria/institucion/{self.institucion.pk}/change/'>\
                {self.institucion}</a>"
            )
        else:
            pass

    @display(description="Observaciones realizadas")
    def observaciones_realizadas_link(self):
        num_observaciones = len(Observacion.objects.filter(operador_observacion=self))
        if num_observaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?operador_observacion__id__exact={self.pk}'>\
                Ver observación realizada</a>"
            )
        elif num_observaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?operador_observacion__id__exact={self.pk}'>\
                Ver observaciones realizadas</a>"
            )            
        else:
            pass

    @display(description="Observaciones procesadas")
    def observaciones_procesadas_link(self):
        num_observaciones = len(Observacion.objects.filter(operador_procesado=self))
        if num_observaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?operador_procesado__id__exact={self.pk}'>\
                Ver observación procesada</a>"
            )
        elif num_observaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?operador_procesado__id__exact={self.pk}'>\
                Ver observaciones procesadas</a>"
            )            
        else:
            pass

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Estacion(models.Model):
    id_estacion = models.CharField(
        max_length=16,
        unique=True,
        verbose_name="ID estación"
    )
    nombre = models.CharField(
        max_length=128,
        verbose_name="Nombre",
        help_text="Denominación descriptiva de la estación"
    )
    direccion = models.CharField(
        max_length=254,
        verbose_name="Dirección postal",
        blank=True,
        null=True
    )
    red_primaria = models.ForeignKey(
        Red,
        limit_choices_to=Q(nombre="REGA"),
        on_delete=models.SET_NULL,
        verbose_name="Red primaria",
        blank=True,
        null=True,
        related_name="red_primaria"
    )
    red_secundaria = models.ManyToManyField(
        Red,
        limit_choices_to=~Q(nombre="REGA"),
        verbose_name="Redes secundarias",
        help_text="Otras redes a las que pertenece o con las que enlaza la estación",
        blank=True,
        related_name="red_secundaria"
    )
    geom = models.MultiPointField(
        srid=4326,
        verbose_name="Localización",
        blank=True,
        null=True,
        spatial_index=True
    )
    pais = models.ForeignKey(
        Pais,
        on_delete=models.SET_NULL,
        verbose_name="País",
        blank=True,
        null=True
    )
    com_autonoma = models.ForeignKey(
        ComAutonoma,
        on_delete=models.SET_NULL,
        verbose_name="Comunidad autónoma",
        blank=True,
        null=True
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.SET_NULL,
        verbose_name="Provincia",
        blank=True,
        null=True       
    )
    isla = models.ForeignKey(
        Isla,
        on_delete=models.SET_NULL,
        verbose_name="Isla",
        blank=True,
        null=True        
    )
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.SET_NULL,
        verbose_name="Municipio",
        blank=True,
        null=True
    )
    hoja_mtn25 = models.ForeignKey(
        HojaMtn25,
        on_delete=models.SET_NULL,
        verbose_name="Hoja MTN25",
        blank=True,
        null=True
    )
    hoja_mtn50 = models.ForeignKey(
        HojaMtn50,
        on_delete=models.SET_NULL,
        verbose_name="Hoja MTN50",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["red_primaria", "id_estacion"]
        verbose_name = "estación"
        verbose_name_plural = "\t\t\t\t\t\t\t\tEstaciones"
        indexes = [
            models.Index(fields=["com_autonoma", "provincia", "isla", "municipio"]),
            models.Index(fields=["com_autonoma", "provincia", "municipio"]),
            models.Index(fields=["com_autonoma", "isla", "municipio"]),
            models.Index(fields=["provincia", "isla", "municipio"]),
            models.Index(fields=["com_autonoma", "municipio"]),
            models.Index(fields=["provincia", "isla"]),
            models.Index(fields=["provincia", "municipio"]),
            models.Index(fields=["isla", "municipio"]),
            models.Index(fields=["red_primaria"]),
            models.Index(fields=["municipio"]),
            models.Index(fields=["id_estacion"]),
        ]

    @display(description="Puntos de observación")
    def punto_obs_link(self):
        puntos = self.puntoobs_set.all()
        if len(puntos) > 0:
            try:
                return format_html(
                    f"<a href='/admin/gravimetria/puntoobs/?estacion__id__exact={self.pk}'>\
                    {', '.join(punto.id_punto_obs for punto in self.puntoobs_set.all())}</a>"
                )
            except TypeError:
                if len(puntos) > 1:
                    return format_html(
                        f"<a href='/admin/gravimetria/puntoobs/?estacion__id__exact={self.pk}'>\
                        Ver puntos</a>"
                    )
                else:
                    return format_html(
                        f"<a href='/admin/gravimetria/puntoobs/?estacion__id__exact={self.pk}'>\
                        Ver punto</a>"
                    )                                            
        else:
            pass

    @display(description="Observaciones")
    def observaciones_link(self):
        puntos = self.puntoobs_set.all()
        observaciones = 0
        for punto in puntos:
            observaciones += len(punto.observacion_set.all())
        if observaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?estacion__id__exact={self.pk}'>\
                Ver observación</a>"
            )
        elif observaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?estacion__id__exact={self.pk}'>\
                Ver sus {observaciones} observaciones</a>"
            )            
        else:
            pass

    @display(description="Comunidad autónoma")
    def com_autonoma_link(self):
        if self.com_autonoma:
            return format_html(
                f"<a href='/admin/unidadmin/comautonoma/{self.com_autonoma.pk}/change/'>\
                {self.com_autonoma}</a>"
            )
        else:
            pass

    @display(description="Provincia")
    def provincia_link(self):
        if self.provincia:
            return format_html(
                f"<a href='/admin/unidadmin/provincia/{self.provincia.pk}/change/'>\
                {self.provincia}</a>"
            )
        else:
            pass

    @display(description="Isla")
    def isla_link(self):
        if self.isla:
            return format_html(
                f"<a href='/admin/unidadmin/isla/{self.isla.pk}/change/'>{self.isla}</a>"
            )
        else:
            pass

    @display(description="Municipio")
    def municipio_link(self):
        if self.municipio:
            return format_html(
                f"<a href='/admin/unidadmin/municipio/{self.municipio.pk}/change/'>\
                {self.municipio}</a>"
            )
        else:
            pass

    def save(self, *args, **kwargs):
        if len(self.puntoobs_set.all()) > 0:
            try:
                punto_geom = []
                for punto in self.puntoobs_set.all():
                    if punto.geom:
                        punto_geom.append(punto.geom)
                self.geom = MultiPoint(punto_geom)
            except TypeError:
                self.geom = None
        else:
            self.geom = None            
        if self.geom:
            try:
                self.pais = Pais.objects.get(geom__contains=self.geom)
            except Pais.DoesNotExist:
                if self.geom.within(Pais.objects.get(pk=53).geom.buffer(width=0.01)):
                    self.pais = Pais.objects.get(pk=53)
                else:
                    pass
            if self.pais and self.pais == Pais.objects.get(pk=53):
                self.municipio = Municipio.objects.get(geom__contains=self.geom.centroid)
                self.isla = self.municipio.isla
                self.provincia = self.municipio.provincia
                self.com_autonoma = self.municipio.com_autonoma
                self.hoja_mtn25 = HojaMtn25.objects.get(geom__contains=self.geom.centroid)
                self.hoja_mtn50 = HojaMtn50.objects.get(geom__contains=self.geom.centroid)
            else:
                pass
        else:
            self.pais = None
            self.com_autonoma = None
            self.provincia = None
            self.isla = None
            self.municipio = None
            self.hoja_mtn25 = None
            self.hoja_mtn50 = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id_estacion


class PuntoObs(models.Model):
    TIPO_SENAL = [
        (1, "Pilar"),
        (2, "Clavo"),
        (3, "Marca"),
        (4, "Sin señalizar"),
        (5, "Desconocido")
    ]
    ESTADO_SENAL = [
        (1, "Buen estado"),
        (2, "Mal estado"),
        (3, "Desconocido")
    ]
    TIPO_ACCESO = [
        (1, "Público"),
        (2, "Privado"),
        (3, "Desconocido")
    ]
    estacion = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        help_text="ID de la estación a la que pertenece el punto"
    )
    id_punto_obs = models.CharField(
        max_length=4,
        verbose_name="ID punto de observación",
        help_text="Indicar únicamente en puntos REGA",
        blank=True,
        default=None,
        null=True
    )
    nombre = models.CharField(
        max_length=128,
        verbose_name="Nombre",
        help_text="Indicar únicamente en estaciones con múltiples puntos de observación",
        blank=True,
        null=True
    )
    tipo_senal = models.IntegerField(
        choices=TIPO_SENAL,
        verbose_name="Tipo de señalización"
    )
    estado_senal = models.IntegerField(
        choices=ESTADO_SENAL,
        verbose_name="Estado de la señal"
    )
    fecha_revision = models.DateField(
        verbose_name="Fecha de revisión",
        blank=True,
        null=True
    )
    tipo_acceso = models.IntegerField(
        choices=TIPO_ACCESO,
        verbose_name="Tipo de acceso"
    )
    latitud = models.FloatField(
        verbose_name="Latitud [º]",
        validators=[
            validators.MaxValueValidator(
                limit_value=90,
                message="Introduzca un valor entre 90º y -90º"
            ),
            validators.MinValueValidator(
                limit_value=-90,
                message="Introduzca un valor entre 90º y -90º"
            )
        ]
    )
    longitud = models.FloatField(
        verbose_name="Longitud [º]",
        validators=[
            validators.MaxValueValidator(
                limit_value=180,
                message="Introduzca un valor entre 180º y -180º"
            ),
            validators.MinValueValidator(
                limit_value=-180,
                message="Introduzca un valor entre 180º y -180º"
            )
        ]
    )
    altitud = models.FloatField(
        verbose_name="Altitud ortométrica [m]"
    )
    geom = models.PointField(
        srid=4326,
        verbose_name="Localización",
        spatial_index=True,
        blank=True,
        null=True
    )
    utm_x = models.FloatField(
        verbose_name="UTM X [m]",
        blank=True,
        null=True
    )
    utm_y = models.FloatField(
        verbose_name="UTM Y [m]",
        blank=True,
        null=True
    )
    utm_zona = models.CharField(
        max_length=3,
        verbose_name="Zona UTM",
        blank=True,
        null=True
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        max_length=500,
        blank=True,
        null=True
    )
    tiene_descripcion = models.BooleanField(
        editable=False
    )
    imagen_nw = models.ImageField(
        max_length=200,
        upload_to=ruta_imagenes,
        verbose_name="Imagen superior izquierda",
        blank=True,
        null=True
    )
    imagen_ne = models.ImageField(
        max_length=200,
        upload_to=ruta_imagenes,
        verbose_name="Imagen superior derecha",
        blank=True,
        null=True
    )
    imagen_sw = models.ImageField(
        max_length=200,
        upload_to=ruta_imagenes,
        verbose_name="Imagen inferior izquierda",
        blank=True,
        null=True
    )
    imagen_se = models.ImageField(
        max_length=200,
        upload_to=ruta_imagenes,
        verbose_name="Imagen inferior derecha",
        blank=True,
        null=True
    )
    num_fotos = models.IntegerField(
        editable=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["estacion", "id_punto_obs"],
                name="unique_punto_obs"
            )
        ]
        indexes = [
            models.Index(fields=["tipo_senal"]),
            models.Index(fields=["estado_senal"]),
            models.Index(fields=["tipo_acceso"]),
            models.Index(fields=["tiene_descripcion"]),
            models.Index(fields=["num_fotos"]),
            models.Index(fields=["estacion"]),
        ]
        ordering = ["estacion__red_primaria", "estacion", "id_punto_obs"]
        verbose_name = "punto de observación"
        verbose_name_plural = "\t\t\t\t\t\t\tPuntos de observación"

    @display(description="Estación")
    def estacion_link(self):
        return format_html(
            f"<a href='/admin/gravimetria/estacion/{self.estacion.pk}/change/'>\
            {self.estacion}</a>"
        )

    @display(description="ID punto de observación")
    def punto_obs_link(self):
        if self.id_punto_obs:
            return format_html(
                f"<a href='/admin/gravimetria/puntoobs/{self.pk}/change/'>\
                {self.id_punto_obs}</a>"                
            )
        else:
            return format_html(
                f"<a href='/admin/gravimetria/puntoobs/{self.pk}/change/'>\
                Ver punto</a>"                
            )            

    @display(description="Reseña")
    def resena_link(self):
        # Genera reseñas para cualquier estación
        return format_html(
            "<a href='{}' class='link'>Ver reseña</a>",
            reverse_lazy("admin:exportar_pdf", args=[self.pk])
        )

        # Únicamente genera reseñas para estaciones REGA
    
        # if self.estacion.red_primaria == Red.objects.get(nombre="REGA"):
        #     return format_html(
        #         "<a href='{}' class='link'>Ver reseña</a>",
        #         reverse_lazy("admin:exportar_pdf", args=[self.pk])
        #     )
        # else:
        #     pass

    @display(description="Observaciones")
    def observaciones_link(self):
        observaciones = len(self.observacion_set.all())
        if observaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?punto_obs__id__exact={self.pk}'>\
                Ver observación</a>"
            )
        elif observaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/observacion/?punto_obs__id__exact={self.pk}'>\
                Ver sus {observaciones} observaciones</a>"
            )            
        else:
            pass

    def save(self, *args, **kwargs):
        num_fotos = 0
        if self.imagen_nw:
            num_fotos += 1
        if self.imagen_ne:
            num_fotos += 1
        if self.imagen_sw:
            num_fotos += 1
        if self.imagen_se:
            num_fotos += 1
        self.num_fotos = num_fotos
        if self.descripcion:
            self.tiene_descripcion = True
        elif not self.descripcion:
            self.tiene_descripcion = False
        if self.latitud and self.longitud:
            self.geom = Point(
                x=self.longitud,
                y=self.latitud,
                srid=4326
            )
            if self.geom.within(Pais.objects.get(pk=53).geom.buffer(width=0.01)):
                if self.longitud < -18.0 and self.longitud > -24.0:
                    self.utm_zona = "27N"
                    self.utm_x = round(self.geom.transform(4082, clone=True).coords[0], 3)
                    self.utm_y = round(self.geom.transform(4082, clone=True).coords[1], 3)
                elif self.longitud < -12.0 and self.longitud > -18.0:
                    self.utm_zona = "28N"
                    self.utm_x = round(self.geom.transform(4083, clone=True).coords[0], 3)
                    self.utm_y = round(self.geom.transform(4083, clone=True).coords[1], 3)
                elif self.longitud < -6.0 and self.longitud > -12.0:
                    self.utm_zona = "29N"
                    self.utm_x = round(self.geom.transform(25829, clone=True).coords[0], 3)
                    self.utm_y = round(self.geom.transform(25829, clone=True).coords[1], 3)
                elif self.longitud < 0.0 and self.longitud > -6.0:
                    self.utm_zona = "30N"
                    self.utm_x = round(self.geom.transform(25830, clone=True).coords[0], 3)
                    self.utm_y = round(self.geom.transform(25830, clone=True).coords[1], 3)
                elif self.longitud < 6.0 and self.longitud > 0.0:
                    self.utm_zona = "31N"
                    self.utm_x = round(self.geom.transform(25831, clone=True).coords[0], 3)
                    self.utm_y = round(self.geom.transform(25831, clone=True).coords[1], 3)
                else:
                    pass
            else:
                pass
        elif self.latitud == None or self.longitud == None:
            self.geom = None
            self.utm_zona = None
            self.utm_x = None
            self.utm_y = None
        else:
            pass
        super().save(*args, **kwargs)
        self.estacion.save()

    def __str__(self):
        if self.id_punto_obs:
            return f"{self.id_punto_obs}"
        else:
            return f"{self.estacion}"


class Observacion(models.Model):
    TIPO_GRADIENTE = [
        (1, "Teórico"),
        (2, "Observado")
    ]
    estacion = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        verbose_name="Estación",
        help_text="ID de la estación a la que pertenece"
    )
    punto_obs = ChainedForeignKey(
        PuntoObs,
        chained_field="estacion",
        chained_model_field="estacion",
        default=None,
        show_all=False,
        auto_choose=False,
        sort=False,
        on_delete=models.CASCADE,
        verbose_name="Punto de observación"
    )
    publicable = models.BooleanField(
        verbose_name="Publicable"
    )
    resenable = models.BooleanField(
        verbose_name="Reseña",
        help_text = "Marcar si se desea emplear en la reseña en vez de otras observaciones"
    )
    fichero_project = models.FileField(
        max_length=200,
        upload_to=ruta_ficheros_g,
        verbose_name="Fichero project",
        help_text="Se debe guardar y continuar para que rellene \
            automaticamente los campos asociados",
        blank=True,
        null=True
    )
    fichero_set = models.FileField(
        max_length=200,
        upload_to=ruta_ficheros_g,
        verbose_name="Fichero set",
        blank=True,
        null=True
    )
    fichero_drop = models.FileField(
        max_length=200,
        upload_to=ruta_ficheros_g,
        verbose_name="Fichero drop",
        blank=True,
        null=True
    )
    fecha_observacion = models.DateField(
        verbose_name="Fecha de observación",
        blank=True,
        null=True
    )
    fecha_procesado = models.DateField(
        verbose_name="Fecha de procesado",
        blank=True,
        null=True        
    )
    operador_observacion = models.ManyToManyField(
        Operador,
        verbose_name="Operadores que realizaron la observación",
        blank=True,
        related_name="operador_observacion"
    )
    operador_procesado = models.ForeignKey(
        Operador,
        on_delete=models.SET_NULL,
        verbose_name="Operador que realizó el último procesado",
        blank=True,
        null=True,
        related_name="operador_procesado"
    )
    tipo_gradiente = models.IntegerField(
        choices=TIPO_GRADIENTE,
        verbose_name="Tipo de gradiente empleado",
        blank=True,
        null=True
    )
    observaciones_medida = models.TextField(
        # verbose_name="Observaciones relativas a la medida",
        verbose_name="Comentarios del fichero project",
        blank=True,
        null=True
    )
    observaciones_procesado = models.TextField(
        # verbose_name="Observaciones relativas al procesado",
        verbose_name="Observaciones",
        max_length=1000,
        blank=True,
        null=True        
    )
    gravimetro_observacion = models.ForeignKey(
        Gravimetro,
        on_delete=models.SET_NULL,
        related_name="gravimetro_observacion",
        verbose_name="Gravímetro",
        blank=True,
        null=True
    )
    gravimetro_gradiente = models.ForeignKey(
        Gravimetro,
        limit_choices_to={"tipo_gravimetro": 2},
        on_delete=models.SET_NULL,
        related_name="gravimetro_gradiente",
        verbose_name="Gravímetro empleado en la observación del gradiente",
        blank=True,
        null=True
    )
    gradiente_vertical = models.FloatField(
        verbose_name="Gradiente vertical de la gravedad [μGal/cm]",
        blank=True,
        null=True
    )
    incertidumbre_gradiente = models.FloatField(
        verbose_name="Incertidumbre en la medida del gradiente [μGal]",
        blank=True,
        null=True
    )
    gravedad_procesada = models.FloatField(
        verbose_name="Gravedad procesada [μGal]",
        # help_text="Valor de la gravedad a la altura de procesado",
        blank=True,
        null=True        
    )
    gravedad_observada = models.FloatField(
        verbose_name="Gravedad observada [μGal]",
        # help_text="Valor de la gravedad a la altura de observación",
        blank=True,
        null=True        
    )
    gravedad_cero = models.FloatField(
        verbose_name="Gravedad a 0 cm [μGal]",
        blank=True,
        null=True        
    )
    dispersion = models.FloatField(
        verbose_name="Dispersión entre sets [μGal]",
        blank=True,
        null=True
    )
    incertidumbre_medida = models.FloatField(
        verbose_name="Incertidumbre de la observación [μGal]",
        blank=True,
        null=True
    )
    incertidumbre_sistematica = models.FloatField(
        verbose_name="Incertidumbre sistemática [μGal]",
        blank=True,
        null=True
    )
    incertidumbre_total = models.FloatField(
        verbose_name="Incertidumbre total [μGal]",
        blank=True,
        null=True
    )
    sets_observados = models.IntegerField(
        verbose_name="Número de sets observados",
        blank=True,
        null=True
    )
    sets_procesados = models.IntegerField(
        verbose_name="Número de sets procesados",
        blank=True,
        null=True
    )
    drops_por_set = models.IntegerField(
        verbose_name="Número de caídas por set",
        blank=True,
        null=True
    )
    altura_de_montaje = models.FloatField(
        verbose_name="Altura de montaje [cm]",
        blank=True,
        null=True
    )
    altura_de_observacion = models.FloatField(
        verbose_name="Altura de observación [cm]",
        blank=True,
        null=True
    )
    altura_de_procesado = models.FloatField(
        verbose_name="Altura de procesado [cm]",
        blank=True,
        null=True
    )
    frecuencia_reloj = models.FloatField(
        blank=True,
        null=True          
    )
    laser_blue_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_red_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_dpeak_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_epeak_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_fpeak_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_gpeak_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_hpeak_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_ipeak_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_jpeak_wlength = models.FloatField(
        blank=True,
        null=True           
    )
    laser_dpeak_volt = models.FloatField(
        blank=True,
        null=True           
    )
    laser_epeak_volt = models.FloatField(
        blank=True,
        null=True           
    )
    laser_fpeak_volt = models.FloatField(
        blank=True,
        null=True           
    )
    laser_gpeak_volt = models.FloatField(
        blank=True,
        null=True           
    )
    laser_hpeak_volt = models.FloatField(
        blank=True,
        null=True           
    )
    laser_ipeak_volt = models.FloatField(
        blank=True,
        null=True           
    )
    laser_jpeak_volt = models.FloatField(
        blank=True,
        null=True           
    )

    class Meta:
        ordering = ["estacion", "punto_obs", "-fecha_observacion"]
        verbose_name = "observación"
        verbose_name_plural = "\t\t\t\t\t\tObservaciones"
        indexes = [
            models.Index(fields=["publicable"]),
            models.Index(fields=["dispersion"]),
            models.Index(fields=["incertidumbre_total"]),
            models.Index(fields=["gravimetro_observacion"]),
            models.Index(fields=["gravimetro_gradiente"]),
            models.Index(fields=["operador_procesado"]),
            models.Index(fields=["estacion"])
        ]

    @display(description="Estación")
    def estacion_link(self):
        if self.estacion:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/{self.estacion.pk}/change/'>\
                {self.estacion}</a>"
            )
        else:
            pass

    @display(description="Punto de observación")
    def punto_obs_link(self):
        if self.punto_obs:
            return format_html(
                f"<a href='/admin/gravimetria/puntoobs/{self.punto_obs.pk}/change/'>\
                {self.punto_obs}</a>"
            )
        else:
            pass

    @display(description="Fecha de observación")
    def fecha_observacion_display(self):
        if self.fecha_observacion:
            return datetime.strftime(self.fecha_observacion, "%d/%m/%Y")
        else:
            pass

    @display(description="Gravímetro")
    def gravimetro_link(self):
        if self.gravimetro_observacion:
            return format_html(
                f"<a href='/admin/gravimetria/gravimetro/{self.gravimetro_observacion.pk}/change/'>\
                {self.gravimetro_observacion}</a>"
            )
        else:
            pass

    @display(description="Gravedad procesada [uGal]")
    def gravedad_procesada_display(self):
        if self.gravedad_procesada:
            return self.gravedad_procesada
        else:
            pass     

    @display(description="Gravedad observada [uGal]")
    def gravedad_observada_display(self):
        if self.gravedad_observada:
            return self.gravedad_observada
        else:
            pass    

    @display(description="Gravedad a 0 cm [uGal]")
    def gravedad_cero_display(self):
        if self.gravedad_cero:
            return self.gravedad_cero
        else:
            pass

    @display(description="Dispersión entre sets [uGal]")
    def dispersion_display(self):
        if self.dispersion:
            return self.dispersion
        else:
            pass

    @display(description="Incertidumbre de la observación [uGal]")
    def incertidumbre_medida_display(self):
        if self.incertidumbre_medida:
            return self.incertidumbre_medida
        else:
            pass

    @display(description="Incertidumbre sistemática [uGal]")
    def incertidumbre_sistematica_display(self):
        if self.incertidumbre_sistematica:
            return self.incertidumbre_sistematica
        else:
            pass

    @display(description="Incertidumbre total [uGal]")
    def incertidumbre_total_display(self):
        if self.incertidumbre_total:
            return self.incertidumbre_total
        else:
            pass

    @display(description="Gradiente [uGal]")
    def gradiente_display(self):
        if self.gradiente_vertical:
            return self.gradiente_vertical
        else:
            pass

    @display(description="Incertidumbre del gradiente [uGal]")
    def incertidumbre_gradiente_display(self):
        if self.incertidumbre_gradiente:
            return self.incertidumbre_gradiente
        else:
            pass

    @display(description="Gravímetro del gradiente")
    def gravimetro_gradiente_link(self):
        if self.gravimetro_gradiente:
            return format_html(
                f"<a href='/admin/gravimetria/gravimetro/{self.gravimetro_gradiente.pk}/change/'>\
                {self.gravimetro_gradiente}</a>"
            )
        else:
            pass

    @display(description="Fecha de procesado")
    def fecha_procesado_display(self):
        if self.fecha_procesado:
            return datetime.strftime(self.fecha_procesado, "%d/%m/%Y")
        else:
            pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.resenable == True:
            observaciones = Observacion.objects.filter(
                punto_obs=self.punto_obs
            ).exclude(pk=self.pk)
            for observacion in observaciones:
                observacion.resenable = False
        if self.fichero_project:
            valores = extracción_fichero_project(self.fichero_project)
            if valores["observaciones_medida"]:
                self.observaciones_medida = valores["observaciones_medida"]
            else:
                pass
            if valores["modelo"] == "A10":
                self.gravimetro_observacion = Gravimetro.objects.filter(
                    modelo=1).get(numero_serie=valores["numero_serie"])
                self.tipo_observacion = 1
                self.laser_blue_wlength = float(valores["laser_blue_wlength"])
                self.laser_red_wlength = float(valores["laser_red_wlength"])
            elif valores["modelo"] == "FG5":
                self.gravimetro_observacion = Gravimetro.objects.filter(
                    modelo=2).get(numero_serie=valores["numero_serie"])
                self.tipo_observacion = 1
                self.laser_dpeak_wlength = float(valores["laser_dpeak_wlength"])
                self.laser_epeak_wlength = float(valores["laser_epeak_wlength"])
                self.laser_fpeak_wlength = float(valores["laser_fpeak_wlength"])
                self.laser_gpeak_wlength = float(valores["laser_gpeak_wlength"])
                self.laser_hpeak_wlength = float(valores["laser_hpeak_wlength"])
                self.laser_ipeak_wlength = float(valores["laser_ipeak_wlength"])
                self.laser_jpeak_wlength = float(valores["laser_jpeak_wlength"])
                self.laser_dpeak_volt = float(valores["laser_dpeak_volt"])
                self.laser_epeak_volt = float(valores["laser_epeak_volt"])
                self.laser_fpeak_volt = float(valores["laser_fpeak_volt"])
                self.laser_gpeak_volt = float(valores["laser_gpeak_volt"])
                self.laser_hpeak_volt = float(valores["laser_hpeak_volt"])
                self.laser_ipeak_volt = float(valores["laser_ipeak_volt"])
                self.laser_jpeak_volt = float(valores["laser_jpeak_volt"])
            self.frecuencia_reloj = float(valores["frecuencia_reloj"])
            self.dispersion = float(valores["dispersion"])
            self.incertidumbre_medida = float(valores["incertidumbre_medida"])
            self.incertidumbre_total = float(valores["incertidumbre_total"])
            self.incertidumbre_sistematica = round(
                sqrt(self.incertidumbre_total ** 2 - self.incertidumbre_medida ** 2)
                , 2
            )           
            self.sets_observados = int(valores["sets_observados"])
            self.sets_procesados = int(valores["sets_procesados"])
            self.drops_por_set = int(valores["drops_por_set"])
            self.gradiente_vertical = float(valores["gradiente_vertical"])
            self.altura_de_montaje = float(valores["altura_de_montaje"])
            self.altura_de_observacion = float(valores["altura_de_observacion"])
            self.altura_de_procesado = float(valores["altura_de_procesado"])
            self.gravedad_procesada = float(valores["gravedad_procesada"])
            self.gravedad_observada = round(self.gravedad_procesada + (
                (self.altura_de_observacion - self.altura_de_procesado) * self.gradiente_vertical),
                2
            )
            self.gravedad_cero = round(
                self.gravedad_procesada - (self.gradiente_vertical * self.altura_de_procesado),
                2
            )
            self.fecha_procesado = datetime.strptime(
                valores["fecha_procesado"].strip(","), "%m/%d/%y"
            )
        else:
            pass
        if self.fichero_drop:
            self.fecha_observacion = extraccion_fecha_observacion(self.fichero_drop)
        else:
            pass
        super().save(*args, **kwargs)    

    def __str__(self):
        if self.punto_obs and self.fecha_observacion:
            return f"{self.estacion}_{self.punto_obs}_{self.fecha_observacion.strftime('%Y%m%d')}"
        else:
            return ""
