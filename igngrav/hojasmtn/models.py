from django.contrib.gis.db import models


# Create your models here.
class HojaMtn25(models.Model):
    hoja = models.CharField(
        max_length=128,
        verbose_name="Número de hoja",
    )
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
        ordering = ["hoja"]
        verbose_name = "hoja MTN25"
        verbose_name_plural = "\tHojas MTN25"

    def __str__(self):
        return f"{self.hoja} - {self.nombre}"


class HojaMtn50(models.Model):
    hoja = models.CharField(
        max_length=128,
        verbose_name="Número de hoja"
    )
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
        ordering = ["hoja"]
        verbose_name = "hoja MTN50"
        verbose_name_plural = "\t\tHojas MTN50"

    def __str__(self):
        return f"{self.hoja} - {self.nombre}"
