from dataclasses import fields
from django.contrib.admin.decorators import display
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.utils.html import format_html


# Create your models here.
class Pais(models.Model):
    nombre = models.CharField(
        max_length=128,
        verbose_name="Nombre"
    )
    geom = models.MultiPolygonField(
        srid=4326,
        verbose_name="Localización",
        spatial_index=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "país"
        verbose_name_plural = "\t\t\t\t\tPaíses"

    def __str__(self):
        return self.nombre


class ComAutonoma(models.Model):
    nombre = models.CharField(
        max_length=128,
        verbose_name="Nombre"
    )
    geom = models.MultiPolygonField(
        srid=4326,
        verbose_name="Localización",
        spatial_index=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "comunidad autónoma"
        verbose_name_plural = "\t\t\t\tComunidades autónomas"

    @display(description="Estaciones")
    def estaciones_link(self):
        num_estaciones = len(self.estacion_set.all())
        if num_estaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?com_autonoma__id__exact={self.pk}'>Ver estación</a>"
            )
        elif num_estaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?com_autonoma__id__exact={self.pk}'>Ver sus {num_estaciones} estaciones</a>"
            )
        else:
            pass

    @display(description="Cobertura [estaciones/área]")
    def cobertura_estaciones(self):
        latitud_centroide = self.geom.centroid.coords[0]
        if latitud_centroide < -18.0 and latitud_centroide > -24.0:
            area = self.geom.transform(4082, clone=True).area
        elif latitud_centroide < -12.0 and latitud_centroide > -18.0:
            area = self.geom.transform(4083, clone=True).area
        elif latitud_centroide < -6.0 and latitud_centroide > -12.0:
            area = self.geom.transform(25829, clone=True).area
        elif latitud_centroide < 0.0 and latitud_centroide > -6.0:
            area = self.geom.transform(25830, clone=True).area
        elif latitud_centroide < 6.0 and latitud_centroide > 0.0:
            area = self.geom.transform(25831, clone=True).area
        else:
            pass
        return round(len(self.estacion_set.all()) / (area * 1e-12), 1)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(
        max_length=128,
        verbose_name="Nombre"
    )
    geom = models.MultiPolygonField(
        srid=4326,
        verbose_name="Localización",
        spatial_index=True
    )
    com_autonoma = models.ForeignKey(
        ComAutonoma,
        on_delete=models.SET_NULL,
        verbose_name="Comunidad autónoma",
        null=True  
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "provincia"
        verbose_name_plural = "\t\t\tProvincias"
        indexes = [
            models.Index(fields=["com_autonoma"])
        ]

    @display(description="Estaciones")
    def estaciones_link(self):
        num_estaciones = len(self.estacion_set.all())
        if num_estaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?provincia__id__exact={self.pk}'>Ver estación</a>"
            )
        elif num_estaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?provincia__id__exact={self.pk}'>Ver sus {num_estaciones} estaciones</a>"
            )
        else:
            pass

    @display(description="Cobertura")
    def cobertura_estaciones(self):
        latitud_centroide = self.geom.centroid.coords[0]
        if latitud_centroide < -18.0 and latitud_centroide > -24.0:
            area = self.geom.transform(4082, clone=True).area
        elif latitud_centroide < -12.0 and latitud_centroide > -18.0:
            area = self.geom.transform(4083, clone=True).area
        elif latitud_centroide < -6.0 and latitud_centroide > -12.0:
            area = self.geom.transform(25829, clone=True).area
        elif latitud_centroide < 0.0 and latitud_centroide > -6.0:
            area = self.geom.transform(25830, clone=True).area
        elif latitud_centroide < 6.0 and latitud_centroide > 0.0:
            area = self.geom.transform(25831, clone=True).area
        else:
            pass
        return round(len(self.estacion_set.all()) / (area * 1e-12), 1)

    def save(self, *args, **kwargs):
        self.com_autonoma = ComAutonoma.objects.get(geom__contains=self.geom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Isla(models.Model):
    nombre = models.CharField(
        max_length=128,
        verbose_name="Nombre"
    )
    geom = models.MultiPolygonField(
        srid=4326,
        verbose_name="Localización",
        spatial_index=True
    )
    com_autonoma = models.ForeignKey(
        ComAutonoma,
        on_delete=models.SET_NULL,
        verbose_name="Comunidad autónoma",
        null=True  
    )    
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.SET_NULL,
        verbose_name="Provincia",
        null=True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "isla"
        verbose_name_plural = "\t\tIslas"
        indexes = [
            models.Index(fields=["provincia"]),
            models.Index(fields=["com_autonoma", "provincia"])
        ]

    @display(description="Estaciones")
    def estaciones_link(self):
        num_estaciones = len(self.estacion_set.all())
        if num_estaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?isla__id__exact={self.pk}'>Ver estación</a>"
            )
        elif num_estaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?isla__id__exact={self.pk}'>Ver sus {num_estaciones} estaciones</a>"
            )
        else:
            pass

    def save(self, *args, **kwargs):
        self.com_autonoma = ComAutonoma.objects.get(geom__contains=self.geom)
        self.provincia = Provincia.objects.get(geom__contains=self.geom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(
        max_length=128,
        verbose_name="Nombre"
    )
    geom = models.MultiPolygonField(
        srid=4326,
        verbose_name="Localización",
        spatial_index=True
    )
    com_autonoma = models.ForeignKey(
        ComAutonoma,
        on_delete=models.SET_NULL,
        verbose_name="Comunidad autónoma",
        null=True        
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.SET_NULL,
        verbose_name="Provincia",
        null=True        
    )
    isla = models.ForeignKey(
        Isla,
        on_delete=models.SET_NULL,
        verbose_name="Isla",
        null = True
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "municipio"
        verbose_name_plural = "\tMunicipios"
        indexes = [
            models.Index(fields=["isla"]),
            models.Index(fields=["provincia", "isla"]),
            models.Index(fields=["com_autonoma", "provincia", "isla"])
        ]

    @display(description="Estaciones")
    def estaciones_link(self):
        num_estaciones = len(self.estacion_set.all())
        if num_estaciones == 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?municipio__id__exact={self.pk}'>Ver estación</a>"
            )
        elif num_estaciones > 1:
            return format_html(
                f"<a href='/admin/gravimetria/estacion/?municipio__id__exact={self.pk}'>Ver sus {num_estaciones} estaciones</a>"
            )
        else:
            pass

    def save(self, *args, **kwargs):
        self.com_autonoma = ComAutonoma.objects.get(geom__contains=self.geom)
        self.provincia = Provincia.objects.get(geom__contains=self.geom)
        try:
            self.isla = Isla.objects.get(geom__contains=self.geom)
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
