# from ctypes import alignment
# from dataclasses import field
import io
import locale
from turtle import position
import matplotlib
matplotlib.use('svg')
from matplotlib.axis import YAxis
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator
import numpy as np
from django.contrib.auth.models import User, Group
from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.forms import CheckboxSelectMultiple, NullBooleanSelect
from django.http import FileResponse
from django.urls import path
from gravimetria.auxiliary_functions import extracción_fichero_set, extraccion_datos_observaciones
from gravimetria.exports import exportar_csv, exportar_xlsx
from gravimetria.filters import *
from gravimetria.models import Red, Estacion, \
    PuntoObs, Observacion, Institucion, Operador, Gravimetro, Mantenimiento
from gravimetria.serializers import exportar_geojson
from leaflet.admin import LeafletGeoAdmin
from PIL import Image
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.axes import XTimeValueAxis, XValueAxis, YValueAxis
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import *
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, Image, \
    Table, TableStyle, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.rl_config import defaultPageSize
from svglib.svglib import svg2rlg


locale.setlocale(locale.LC_ALL, '')

PAGE_HEIGHT=defaultPageSize[1]; PAGE_WIDTH=defaultPageSize[0]


admin.site.disable_action('delete_selected')


class InstitucionAdmin(admin.ModelAdmin):
    list_display = (
        "nombre", "nombre_completo", "operadores_link", "web_link"
    )

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return ("nombre", "nombre_completo", "web",)
        else:
            return super().get_readonly_fields(request, obj)


class RedAdmin(admin.ModelAdmin):
    list_display = (
        "nombre", "nombre_completo", "estaciones_red_primaria_link", 
        "estaciones_red_secundaria_link", "web_link"
    )

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context) 

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return ("nombre", "nombre_completo", "web",)
        else:
            return super().get_readonly_fields(request, obj)


class GravimetroAdmin(admin.ModelAdmin):
    list_display = (
        "modelo", "numero_serie", "tipo_gravimetro", "institucion_link",
        "manual_modelo_link", "mantenimiento_link", "cambio_correa_display",
        "cambio_bomba_display", "mantenimiento_laser_display", "calibracion_laser_display",
        "calibracion_reloj_display"
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(GravimetroAdmin, self).get_form(request, obj, **kwargs)
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            pass
        else:
            form.base_fields['institucion'].widget.can_add_related = False
            form.base_fields['institucion'].widget.can_change_related = False
            form.base_fields['institucion'].widget.can_delete_related = False
        return form

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context) 

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return (
                "modelo", "numero_serie", "tipo_gravimetro", "institucion", "manual"
            )
        else:
            return super().get_readonly_fields(request, obj)


class MantenimientoAdmin(admin.ModelAdmin):
    list_display = (
        "gravimetro_link", "tipo_mantenimiento", "fecha_mantenimiento_display",
        "fichero_mantenimiento_link"
    )
    list_display_links = ("tipo_mantenimiento",)
    list_filter = (
        GravimetroListFilterForMantenimiento, TipoMantenimientoListFilterForMantenimiento
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(MantenimientoAdmin, self).get_form(request, obj, **kwargs)
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            pass
        else:
            form.base_fields['gravimetro'].widget.can_add_related = False
            form.base_fields['gravimetro'].widget.can_change_related = False
            form.base_fields['gravimetro'].widget.can_delete_related = False
        return form

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context) 

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return (
                "gravimetro", "tipo_mantenimiento", "fecha_mantenimiento",
                "observaciones", "fichero_mantenimiento"
            )
        else:
            return super().get_readonly_fields(request, obj)


class OperadorAdmin(admin.ModelAdmin):
    list_display = (       
        "nombre", "apellidos", "institucion_link",
        "observaciones_realizadas_link", "observaciones_procesadas_link"
    )
    search_fields = ("nombre", "apellidos")

    def get_form(self, request, obj=None, **kwargs):
        form = super(OperadorAdmin, self).get_form(request, obj, **kwargs)
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            pass
        else:
            form.base_fields['institucion'].widget.can_add_related = False
            form.base_fields['institucion'].widget.can_change_related = False
            form.base_fields['institucion'].widget.can_delete_related = False
        return form

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context) 

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return (
                "nombre", "apellidos", "institucion",
            )
        else:
            return super().get_readonly_fields(request, obj)


class EstacionAdmin(LeafletGeoAdmin):
    actions = [exportar_csv, exportar_xlsx]
    fieldsets = (
        (None, {
            "fields": ("id_estacion", "nombre", "geom")
        }),
        ("Redes gravimétricas y geodésicas", {
            "classes": ("collapse", "wide"),
            "fields": ("red_primaria", "red_secundaria")
        }),
        ("Datos geográficos", {
            "classes": ("collapse", "wide"),
            "fields": (
                "pais", "com_autonoma", "provincia", "isla", "municipio", 
                "direccion", "hoja_mtn50", "hoja_mtn25"
            )
        }),        
    )
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple}
    }
    list_display = (
        "id_estacion", "nombre", "punto_obs_link", "observaciones_link",
        "com_autonoma_link", "provincia_link", "isla_link", "municipio_link"
    )    
    list_filter = (
        RedPrimariaListFilterForEstacion, RedSecundariaListFilterForEstacion,
        ComAutonomaListFilterForEstacion, ProvinciaListFilterForEstacion,
        IslaListFilterForEstacion, MunicipioListFilterForEstacion
    )
    list_max_show_all = 10000
    readonly_fields = (
        "pais", "com_autonoma", "provincia", "isla", "municipio", \
        "hoja_mtn50", "hoja_mtn25"
    )
    search_fields = ("id_estacion", "nombre")
    show_full_result_count = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(EstacionAdmin, self).get_form(request, obj, **kwargs)
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            pass
        else:
            form.base_fields['red_primaria'].widget.can_add_related = False
            form.base_fields['red_primaria'].widget.can_change_related = False
            form.base_fields['red_primaria'].widget.can_delete_related = False
            form.base_fields['red_secundaria'].widget.can_add_related = False
        return form

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)            

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return (
                "id_estacion", "nombre", "red_primaria", "red_secundaria", "pais",
                "com_autonoma", "provincia", "isla", "municipio", "direccion",
                "hoja_mtn50", "hoja_mtn25"
            )
        else:
            return super().get_readonly_fields(request, obj)


class PuntoObsAdmin(LeafletGeoAdmin):
    actions = [exportar_csv, exportar_xlsx]
    fieldsets = (
        (None, {
            "fields": (
                "estacion", "id_punto_obs", "nombre", "geom"
            )
        }),
        ("Señalización", {
            "classes": ("collapse", "wide"),
            "fields": (
                "tipo_senal", "estado_senal", "fecha_revision", "tipo_acceso"
            )
        }),
        ("Coordenadas", {
            "classes": ("collapse", "wide"),
            "fields": (
                "latitud", "longitud", "altitud",
                "utm_x", "utm_y", "utm_zona"
            )
        }),
        ("Reseña", {
            "classes": ("collapse", "wide"),
            "fields": (
                "descripcion", ("imagen_nw", "imagen_ne"),
                ("imagen_sw", "imagen_se")
            )
        }),
    )
    list_display = (
        "estacion_link", "punto_obs_link", "nombre", "resena_link", "observaciones_link",
        "tipo_senal", "estado_senal", "fecha_revision", "tipo_acceso", "latitud", "longitud", "altitud",
        "utm_x", "utm_y", "utm_zona"
    )
    list_display_links = ("punto_obs_link",)
    list_filter = (
        RedPrimariaListFilterForPuntoObs, RedSecundariaListFilterForPuntoObs,
        TipoSenalListFilterForPuntoObs, EstadoSenalListFilterForPuntoObs,
        TipoAccesoListFilterForPuntoObs, DescripcionListFilterForPuntoObs,
        NumeroFotosListFilterForPuntoObs, EstacionListFilterForPuntoObs,
        ProvinciaListFilterForPuntoObs, IslaListFilterForPuntoObs,
        MunicipioListFilterForPuntoObs, ComAutonomaListFilterForPuntoObs
    )
    list_max_show_all = 10000
    readonly_fields = ("utm_x", "utm_y", "utm_zona")
    autocomplete_fields = ["estacion"]
    search_fields = ("nombre", "estacion__id_estacion")
    show_full_result_count = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('resena/<int:pk>/', self.exportar_pdf, name="exportar_pdf"),
        ]
        return my_urls + urls

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context) 

    def exportar_pdf(self, request, pk):
        # print(PAGE_WIDTH / cm)
        # print(PAGE_HEIGHT / cm)

        buffer = io.BytesIO()

        # selección del punto de observación
        punto_obs = PuntoObs.objects.get(pk=pk)

        # selección de la observación
        if Observacion.objects.filter(punto_obs=punto_obs).filter(resenable=True):
            observacion = Observacion.objects.filter(punto_obs=punto_obs).get(resenable=True)
        elif Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=True):
            if  Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=True).filter(
                gravimetro_observacion__modelo=2):
                observacion = Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=True).filter(
                    gravimetro_observacion__modelo=2).latest("fecha_observacion")
            elif Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=True).filter(
                gravimetro_observacion__modelo=1):
                observacion = Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=True).filter(
                    gravimetro_observacion__modelo=1).latest("fecha_observacion")
            else:
                observacion = Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=True).latest(
                    "fecha_observacion")
        elif Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=False):
            if  Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=False).filter(
                gravimetro_observacion__modelo=2):
                observacion = Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=False).filter(
                    gravimetro_observacion__modelo=2).latest("fecha_observacion")
            elif Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=False).filter(
                gravimetro_observacion__modelo=1):
                observacion = Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=False).filter(
                    gravimetro_observacion__modelo=1).latest("fecha_observacion")
            else:
                observacion = Observacion.objects.filter(punto_obs=punto_obs).filter(publicable=False).latest(
                    "fecha_observacion")
        else:
            observacion = None

        p = canvas.Canvas(buffer)

        # estilos
        style1 = ParagraphStyle(
            "style1",
            fontName="Times-Roman",
            fontSize=10,
            alignment=1,
        )
        style2 = ParagraphStyle(
            "style2",
            fontName="Times-Roman",
            fontSize=10,
            alignment=1,
        )
        style3 = ParagraphStyle(
            "style3",
            fontName="Times-Roman",
            fontSize=10,
            alignment=1,
            backColor="#cfe6ff",
            borderPadding = (0.19 * cm, 0.19 * cm, 0.215 * cm, 0.19 * cm)
        )
        style4 = ParagraphStyle(
            "style4",
            fontName="Times-Roman",
            fontSize=9,
            alignment=0,
            spaceBefore=0.5
        )
        style5 = ParagraphStyle(
            "style5",
            fontName="Times-Roman",
            fontSize=10,
            alignment=0,
            # backColor="#cfe6ff",
            backColor="#ffffff",
            borderPadding = (0.05 * cm, 0.075 * cm, 0.05 * cm,  0.075 * cm),
        )
        style6 = ParagraphStyle(
            "style6",
            fontName="Times-Roman",
            fontSize=6,
            alignment=1,
        )        

        p.setFont("Times-Roman", 10)

        logo = "C:\ignGrav\igngrav\media\RESENA\logo_mitma.jpg"

        pageinfo = ("www.ign.es", "gravimetria@mitma.es")

        # primera página

        # cabecera
        p.drawImage(logo, cm, 27 * cm, 9.5 * cm, 1.75 * cm, preserveAspectRatio=True, anchor="c")

        story = []
        story.append(Paragraph("INSTITUTO GEOGRÁFICO NACIONAL", style1))
        story.append(Spacer(0.25 * cm, 0.25 * cm))
        story.append(Paragraph("Servicio de Gravimetría", style2))
        f = Frame(10.5 * cm, 27.02 * cm, 9.5 * cm, 1.715 * cm, showBoundary=0)
        f.addFromList(story, p)
        p.line(11.625 * cm, 28.735 * cm, 18.875 * cm, 28.735 * cm)
        p.line(11.625 * cm, 27.0 * cm, 18.875 * cm, 27.0 * cm)


        # datos de la estación y del punto de observación
        story = []
        if punto_obs.estacion:
            story.append(Paragraph(f"<b>ID estación:</b> {punto_obs.estacion}", style4))
            story.append(Paragraph(f"<b>Nombre:</b> {punto_obs.estacion.nombre}", style4))
            story.append(Paragraph(f"<b>Punto de observación:</b> {punto_obs.id_punto_obs}", style4))
            if punto_obs.nombre:
                story.append(Paragraph(f"<b>Nombre del punto:</b> {punto_obs.nombre}", style4))
            story.append(Paragraph("<b>Tipo de señalización:</b> " + f"{punto_obs.get_tipo_senal_display()}".lower(), style4))
            story.append(Paragraph("<b>Tipo de acceso:</b> " + f"{punto_obs.get_tipo_acceso_display()}".lower(), style4))
        else:
            story.append(Paragraph("No hay datos disponibles", style4))
        f = Frame(cm, 22 * cm, 9.5 * cm, 3 * cm, showBoundary=1)
        f.addFromList(story, p)    

        story = []
        story.append(Paragraph("Datos de la estación y del punto de observación", style5))
        f = Frame(1.25 * cm, 24.6* cm, 7.15 * cm, 0.85 * cm, showBoundary=0)
        f.addFromList(story, p)

        # datos geográficos
        story = []
        if punto_obs.estacion.pais:
            story.append(Paragraph(f"<b>País:</b> {punto_obs.estacion.pais}", style4))
            if punto_obs.estacion.pais.nombre == "España":
                story.append(Paragraph(f"<b>Comunidad autónoma:</b> {punto_obs.estacion.com_autonoma}", style4))
                story.append(Paragraph(f"<b>Provincia:</b> {punto_obs.estacion.provincia}", style4))
                if punto_obs.estacion.isla:
                    story.append(Paragraph(f"<b>Isla:</b> {punto_obs.estacion.isla}", style4))
                story.append(Paragraph(f"<b>Municipio:</b> {punto_obs.estacion.municipio}", style4))
                story.append(Paragraph(f"<b>Hoja MTN25:</b> {punto_obs.estacion.hoja_mtn25}", style4))
        else:
            story.append(Paragraph("No hay datos disponibles", style4))
        f = Frame(10.5 * cm, 22 * cm, 9.5 * cm, 3 * cm, showBoundary=1)
        f.addFromList(story, p)

        story = []
        story.append(Paragraph("Datos geográficos", style5))
        f = Frame(10.75 * cm, 24.6* cm, 3 * cm, 0.85 * cm, showBoundary=0)
        f.addFromList(story, p)
        
        # datos de la observación
        story = []
        if observacion and observacion.gravimetro_observacion.tipo_gravimetro == 1:
            story.append(Paragraph(f"<b>Gravedad:</b> {observacion.gravedad_observada} μGal", style4))
            story.append(Paragraph(f"<b>Altura de observación:</b> {observacion.altura_de_observacion} cm", style4))
            story.append(Paragraph(f"<b>Incertidumbre total:</b> {observacion.incertidumbre_total} μGal", style4))
            story.append(Paragraph(f"<b>Gravímetro empleado:</b> {observacion.gravimetro_observacion}", style4))
            story.append(Paragraph(f"<b>Gradiente vertical " + f"({observacion.get_tipo_gradiente_display()}):</b> ".lower() + f"{observacion.gradiente_vertical} μGal/cm", style4))
            story.append(Paragraph(f"<b>Gravedad a 0 cm:</b> {observacion.gravedad_cero} μGal", style4))
            fecha_observacion = observacion.fecha_observacion.strftime("%d-%m-%Y")
            story.append(Paragraph(f"<b>Fecha de observación:</b> {fecha_observacion}", style4))
        elif observacion and observacion.gravimetro_observacion.tipo_gravimetro == 2:
            story.append(Paragraph(f"<b>Gravedad:</b> {observacion.gravedad_observada} μGal", style4))
            story.append(Paragraph(f"<b>Incertidumbre total:</b> {observacion.incertidumbre_total} μGal", style4))
            story.append(Paragraph(f"<b>Gravímetro empleado:</b> {observacion.gravimetro_observacion}", style4))
            fecha_observacion = observacion.fecha_observacion.strftime("%d-%m-%Y")
            story.append(Paragraph(f"<b>Fecha de observación:</b> {fecha_observacion}", style4))
        else:
            story.append(Paragraph("No hay datos disponibles", style4))
        f = Frame(cm, 17.75 * cm, 9.5 * cm, 3.5 * cm, showBoundary=1)
        f.addFromList(story, p)

        story = []
        story.append(Paragraph("Datos de la observación", style5))
        f = Frame(1.25 * cm, 20.85 * cm, 3.8 * cm, 0.85 * cm, showBoundary=0)
        f.addFromList(story, p)

        # datos geodésicos
        story = []
        if punto_obs.latitud and punto_obs.longitud and punto_obs.altitud:
            if punto_obs.estacion.pais.nombre == "España":
                if punto_obs.estacion.com_autonoma.nombre == "Canarias":
                    geom = punto_obs.geom.transform(4081, clone=True)
                    latitud = geom.coords[1]
                    longitud = geom.coords[0]
                    story.append(Paragraph(f"<b>Latitud:</b> {latitud} º", style4))
                    story.append(Paragraph(f"<b>Longitud:</b> {longitud} º", style4))
                    story.append(Paragraph(f"<b>Altitud ortométrica:</b> {punto_obs.altitud} m", style4))                    
                    story.append(Paragraph(f"<b>UTM X:</b> {punto_obs.utm_x} m", style4))
                    story.append(Paragraph(f"<b>UTM Y:</b> {punto_obs.utm_y} m", style4))
                    story.append(Paragraph(f"<b>Zona UTM:</b> {punto_obs.utm_zona}", style4))
                    story.append(Paragraph(f"<b>Sistema de referencia:</b> REGCAN95", style4))
                else:
                    geom = punto_obs.geom.transform(4258, clone=True)
                    latitud = geom.coords[1]
                    longitud = geom.coords[0]
                    story.append(Paragraph(f"<b>Latitud:</b> {latitud} º", style4))
                    story.append(Paragraph(f"<b>Longitud:</b> {longitud} º", style4))
                    story.append(Paragraph(f"<b>Altitud ortométrica:</b> {punto_obs.altitud} m", style4))
                    story.append(Paragraph(f"<b>UTM X:</b> {punto_obs.utm_x} m", style4))
                    story.append(Paragraph(f"<b>UTM Y:</b> {punto_obs.utm_y} m", style4))
                    story.append(Paragraph(f"<b>Zona UTM:</b> {punto_obs.utm_zona}", style4))
                    story.append(Paragraph(f"<b>Sistema de referencia:</b> ETRS89", style4))
            else:
                story.append(Paragraph(f"<b>Latitud:</b> {punto_obs.latitud} º", style4))
                story.append(Paragraph(f"<b>Longitud:</b> {punto_obs.longitud} º", style4))
                story.append(Paragraph(f"<b>Altitud ortométrica:</b> {punto_obs.altitud} m", style4))
                story.append(Paragraph(f"<b>Sistema de referencia:</b> WGS84", style4))              
        else:
            story.append(Paragraph("No hay datos disponibles", style4))
        f = Frame(10.5 * cm, 17.75 * cm, 9.5 * cm, 3.5 * cm, showBoundary=1)
        f.addFromList(story, p)

        story = []
        story.append(Paragraph("Datos geodésicos", style5))
        f = Frame(10.75 * cm, 20.85 * cm, 2.90 * cm, 0.85 * cm, showBoundary=0)
        f.addFromList(story, p)

        # datos del lugar observado
        story = []
        if punto_obs.descripcion and punto_obs.estacion.direccion:
            story.append(Paragraph(f"<b>Descripción:</b> {punto_obs.descripcion}", style4))
            story.append(Paragraph(f"<b>Dirección: </b>{punto_obs.estacion.direccion}", style4))
        elif punto_obs.descripcion:
            story.append(Paragraph(f"<b>Descripción:</b> {punto_obs.descripcion}", style4))
        elif punto_obs.estacion.direccion:
            story.append(Paragraph(f"<b>Dirección: </b>{punto_obs.estacion.direccion}", style4))
        else:
            story.append(Paragraph("No hay datos disponibles", style4))
        f = Frame(cm, 14.75 * cm, 19 * cm, 2.25 * cm, showBoundary=1)
        f.addFromList(story, p)

        story = []
        story.append(Paragraph("Datos del lugar observado", style5))
        f = Frame(1.255 * cm, 16.60 * cm, 4.125 * cm, 0.85 * cm, showBoundary=0)
        f.addFromList(story, p)

        # imágenes
        story = []
        if punto_obs.imagen_nw or punto_obs.imagen_ne or punto_obs.imagen_sw or punto_obs.imagen_se:          
            if punto_obs.imagen_nw:
                imagen_nw = punto_obs.imagen_nw
                if imagen_nw.width > imagen_nw.height:
                    p.drawImage(imagen_nw.path, cm, 7.75 * cm, 9.5 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)
                else:
                    p.drawImage(imagen_nw.path, 3.41 * cm, 7.75 * cm, 4.68 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)
            f = Frame(cm, 7.75 * cm, 9.5 * cm, 6.25 * cm, showBoundary=1)
            f.addFromList(story, p)

            if punto_obs.imagen_ne:
                imagen_ne = punto_obs.imagen_ne
                if imagen_ne.width > imagen_ne.height:
                    p.drawImage(imagen_ne.path, 10.5 * cm, 7.75 * cm, 9.5 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)
                else:
                    p.drawImage(imagen_ne.path, 12.91 * cm, 7.75 * cm, 4.68 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)
            f = Frame(10.5 * cm, 7.75 * cm, 9.5 * cm, 6.25 * cm, showBoundary=1)
            f.addFromList(story, p)

            if punto_obs.imagen_sw:
                imagen_sw = punto_obs.imagen_sw
                if imagen_sw.width > imagen_sw.height:
                    p.drawImage(imagen_sw.path, cm, 1.5 * cm, 9.5 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)    
                else:
                    p.drawImage(imagen_sw.path, 3.41 * cm, 1.5 * cm, 4.68 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)
            f = Frame(cm, 1.5 * cm, 9.5 * cm, 6.25 * cm, showBoundary=1)
            f.addFromList(story, p)

            if punto_obs.imagen_se:
                imagen_se = punto_obs.imagen_se
                if imagen_se.width > imagen_se.height:
                    p.drawImage(imagen_se.path, 10.5 * cm, 1.5 * cm, 9.5 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)
                else:
                    p.drawImage(imagen_se.path, 12.91 * cm, 1.5 * cm, 4.68 * cm, 6.25 * cm, showBoundary=0, anchor="c", preserveAspectRatio=True)
            f = Frame(10.5 * cm, 1.5 * cm, 9.5 * cm, 6.25 * cm, showBoundary=1)
            f.addFromList(story, p)

            story = []
            story.append(Paragraph("Imágenes", style5))
            f = Frame(1.255 * cm, 13.6 * cm, 1.8 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

        story = []
        if observacion.gravimetro_observacion.tipo_gravimetro == 1:
            story.append(Paragraph("RESEÑA GRAVIMÉTRICA DE OBSERVACIÓN ABSOLUTA", style3))
        elif observacion.gravimetro_observacion.tipo_gravimetro == 2:
            story.append(Paragraph("RESEÑA GRAVIMÉTRICA DE OBSERVACIÓN RELATIVA", style3))
        else:
            story.append(Paragraph("RESEÑA GRAVIMÉTRICA", style3))
        f = Frame(cm, 25.75 * cm, 19 * cm, 0.875 * cm, showBoundary=1)
        f.addFromList(story, p)      

        p.setFillColorRGB(0, 0, 255)
        p.setFont("Times-Roman", 9)
        p.drawString(cm, 0.75 * cm, pageinfo[0])
        p.drawString(17 * cm, 0.75 * cm, pageinfo[1])

        p.showPage()

        # segunda página

        if observacion.fichero_set and observacion.gravimetro_observacion.tipo_gravimetro == 1:
            cm_plt = 1/2.54

            datos_set = extracción_fichero_set(observacion.fichero_set)

            # cabecera    
            p.drawImage(logo, cm, 27 * cm, 9.5 * cm, 1.75 * cm, preserveAspectRatio=True, anchor="c")

            story = []
            story.append(Paragraph("INSTITUTO GEOGRÁFICO NACIONAL", style1))
            story.append(Spacer(0.25 * cm, 0.25 * cm))
            story.append(Paragraph("Servicio de Gravimetría", style2))
            f = Frame(10.5 * cm, 27.02 * cm, 9.5 * cm, 1.715 * cm, showBoundary=0)
            f.addFromList(story, p)
            p.line(11.625 * cm, 28.735 * cm, 18.875 * cm, 28.735 * cm)
            p.line(11.625 * cm, 27.0 * cm, 18.875 * cm, 27.0 * cm)

            story = []
            story.append(Paragraph("DATOS DETALLADOS DE LA OBSERVACIÓN", style3))
            f = Frame(cm, 25.75 * cm, 19 * cm, 0.875 * cm, showBoundary=1)
            f.addFromList(story, p)

            # gráfica de gravedad
            fig, ax = plt.subplots(
                figsize=(19.615 * cm_plt, 4 * cm_plt), frameon=False
            )
            x = datos_set["fecha_observacion"]
            y = datos_set["gravedad"]
            yerr = datos_set["dispersion"]
            mean = np.mean(y)
            plt.errorbar(
                x, y, yerr, ecolor="steelblue", color="steelblue",
                marker="o", markeredgewidth=0.5, markeredgecolor="black",
                linestyle="None", capsize=2
            )
            plt.axis(ymin=mean - 70, ymax=mean + 70)

            locator = AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(
                locator, show_offset=False
            )
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            minor_locator = ticker.AutoMinorLocator(2)
            ax.yaxis.set_minor_locator(minor_locator)

            plt.xticks(
                fontname="Times New Roman", fontsize=6, visible=False
            )
            plt.yticks(
                np.arange(mean - 60, mean + 80, step = 20),
                np.arange(-60, 80, step=20),
                fontname="Times New Roman", fontsize=6
                )
            ax.tick_params("x", length=0)
            ax.tick_params("y", pad=2, direction="out")

            plt.grid(True)
            plt.grid(True, "minor", "y", linestyle=":")

            imgdata = io.BytesIO()
            fig.savefig(imgdata, format="svg")
            imgdata.seek(0)  # rewind the data
            drawing = svg2rlg(imgdata)
            drawing.drawOn(p, - 2.065 * cm, 20.475 * cm)

            story = []
            story.append(Paragraph(
                f"Gravedad ({observacion.altura_de_observacion} cm): {observacion.gravedad_observada} ± {observacion.incertidumbre_total} μGal", style5)
            )
            f = Frame(1.25 * cm, 24.75* cm, 8 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

            story = []
            story.append(
                Paragraph(f"{observacion.sets_procesados} sets procesados ({observacion.drops_por_set} caídas por set)", style5)
            )
            f = Frame(13.75 * cm, 24.75* cm, 6.25 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

            # gráfica de temperatura
            fig, ax = plt.subplots(
                figsize=(19.615 * cm_plt, 4 * cm_plt), frameon=False
            )
            y = datos_set["temperatura"]
            plt.plot(
                x, y, color="lightcoral",
                marker="o", markeredgewidth=0.5, markeredgecolor="black",
                linestyle="--"
            )

            locator = AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(
                locator, show_offset=False
            )
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            minor_locator = ticker.AutoMinorLocator()
            ax.yaxis.set_minor_locator(minor_locator)

            plt.xticks(
                fontname="Times New Roman", fontsize=6, visible=False
            )
            plt.yticks(
                fontname="Times New Roman", fontsize=6
                )
            ax.tick_params("x", length=0)
            ax.tick_params("y", pad=2, direction="out")

            plt.grid(True)
            plt.grid(True, "minor", "y", linestyle=":")

            imgdata = io.BytesIO()
            fig.savefig(imgdata, format="svg")
            imgdata.seek(0)  # rewind the data
            drawing = svg2rlg(imgdata)
            drawing.drawOn(p, - 2.065 * cm, 15.725 * cm)

            story = []
            story.append(Paragraph("Temperatura [ºC]", style5))
            f = Frame(1.25 * cm, 20 * cm, 2.95 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

            # gráfica de presión
            fig, ax = plt.subplots(
                figsize=(19.615 * cm_plt, 4 * cm_plt), frameon=False
            )
            y = datos_set["presion"]
            plt.plot(
                x, y, color="mediumorchid",
                marker="o", markeredgewidth=0.5, markeredgecolor="black",
                linestyle="--"
            )

            locator = AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(
                locator, show_offset=False
            )
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            minor_locator = ticker.AutoMinorLocator()
            ax.yaxis.set_minor_locator(minor_locator)

            plt.xticks(
                fontname="Times New Roman", fontsize=6, visible=False
            )
            plt.yticks(
                fontname="Times New Roman", fontsize=6
                )
            ax.tick_params("x", length=0)
            ax.tick_params("y", pad=2, direction="out")
            plt.ticklabel_format(axis="y", style="plain", useOffset=False)

            plt.grid(True)
            plt.grid(True, "minor", "y", linestyle=":")

            imgdata = io.BytesIO()
            fig.savefig(imgdata, format="svg")
            imgdata.seek(0)  # rewind the data
            drawing = svg2rlg(imgdata)
            drawing.drawOn(p, - 2.065 * cm, 10.975 * cm)

            story = []
            story.append(Paragraph("Presión [mBar]", style5))
            f = Frame(1.25 * cm, 15.25 * cm, 2.6 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

            # gráfica de marea terrestre
            fig, ax = plt.subplots(
                figsize=(19.615 * cm_plt, 4 * cm_plt), frameon=False
            )
            y = datos_set["marea_terrestre"]
            plt.plot(
                x, y, color="mediumaquamarine",
                marker="o", markeredgewidth=0.5, markeredgecolor="black",
                linestyle="--"
            )

            locator = AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(
                locator, show_offset=False
            )
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            minor_locator = ticker.AutoMinorLocator()
            ax.yaxis.set_minor_locator(minor_locator)

            plt.xticks(
                fontname="Times New Roman", fontsize=6, visible=False
            )
            plt.yticks(
                fontname="Times New Roman", fontsize=6
                )
            ax.tick_params("x", length=0)
            ax.tick_params("y", pad=2, direction="out")

            plt.grid(True)
            plt.grid(True, "minor", "y", linestyle=":")

            imgdata = io.BytesIO()
            fig.savefig(imgdata, format="svg")
            imgdata.seek(0)  # rewind the data
            drawing = svg2rlg(imgdata)
            drawing.drawOn(p, - 2.065 * cm, 6.225 * cm)

            story = []
            story.append(Paragraph("Marea terrestre [μGal]", style5))
            f = Frame(1.25 * cm, 10.5 * cm, 3.6 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

            # gráfica de carga oceánica
            fig, ax = plt.subplots(
                figsize=(19.615 * cm_plt, 4 * cm_plt), frameon=False
            )
            y = datos_set["carga_oceanica"]
            plt.plot(
                x, y, color="chocolate",
                marker="o", markeredgewidth=0.5, markeredgecolor="black",
                linestyle="--"
            )

            locator = AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(
                locator, show_offset=False
            )
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            minor_locator = ticker.AutoMinorLocator()
            ax.yaxis.set_minor_locator(minor_locator)

            plt.xticks(
                fontname="Times New Roman", fontsize=6
            )
            plt.yticks(
                fontname="Times New Roman", fontsize=6
                )
            ax.tick_params("y", pad=2, direction="out")

            plt.grid(True)
            plt.grid(True, "minor", "y", linestyle=":")

            imgdata = io.BytesIO()
            fig.savefig(imgdata, format="svg")
            imgdata.seek(0)  # rewind the data
            drawing = svg2rlg(imgdata)
            drawing.drawOn(p, - 2.065 * cm, 1.475 * cm)

            story = []
            story.append(Paragraph("Carga oceánica [μGal]", style5))
            f = Frame(1.25 * cm, 5.75 * cm, 3.65 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

            # pie de página
            p.setFillColorRGB(0, 0, 255)
            p.setFont("Times-Roman", 9)
            p.drawString(cm, 0.75 * cm, pageinfo[0])
            p.drawString(17 * cm, 0.75 * cm, pageinfo[1])

            p.showPage()

            # tercera página

        observaciones = Observacion.objects.filter(punto_obs=punto_obs).order_by("-fecha_observacion")
        if len(observaciones) > 1:
            cm_plt = 1/2.54
            datos_observaciones = extraccion_datos_observaciones(observaciones)

            # cabecera
            p.drawImage(logo, cm, 27 * cm, 9.5 * cm, 1.75 * cm, preserveAspectRatio=True, anchor="c")

            story = []
            story.append(Paragraph("INSTITUTO GEOGRÁFICO NACIONAL", style1))
            story.append(Spacer(0.25 * cm, 0.25 * cm))
            story.append(Paragraph("Servicio de Gravimetría", style2))
            f = Frame(10.5 * cm, 27.02 * cm, 9.5 * cm, 1.715 * cm, showBoundary=0)
            f.addFromList(story, p)
            p.line(11.625 * cm, 28.735 * cm, 18.875 * cm, 28.735 * cm)
            p.line(11.625 * cm, 27.0 * cm, 18.875 * cm, 27.0 * cm)

            story = []
            story.append(Paragraph("HISTORIAL DE OBSERVACIONES", style3))
            f = Frame(cm, 25.75 * cm, 19 * cm, 0.875 * cm, showBoundary=1)
            f.addFromList(story, p)

            # gráfica de gravedad
            fig, ax = plt.subplots(
                figsize=(19.615 * cm_plt, 4 * cm_plt), frameon=False
            )

            # mean = np.mean(y) revisar por qué estaba este valor así
            for i in range(len(observaciones)):
                x = i
                y = datos_observaciones["gravedad_cero"][i]
                yerr = datos_observaciones["dispersion"][i]
                if datos_observaciones["publicable"][i] == True:
                    plt.errorbar(
                        x, y, yerr, ecolor="black", color="limegreen",
                        marker=".", markeredgewidth=0.2, markeredgecolor="black",
                        linestyle="None", capsize=1, elinewidth=1, markersize=7.5
                    )
                else:
                    plt.errorbar(
                        x, y, yerr, ecolor="black", color="crimson",
                        marker=".", markeredgewidth=0.2, markeredgecolor="black",
                        linestyle="None", capsize=1, elinewidth=1, markersize=7.5
                    )

            default_xticks = set([int(i) for i in list(plt.xticks()[0]) if i >= 0])
            xlabels = []
            xticks = []
            for i in default_xticks:
                try:
                    xlabels.append(datos_observaciones["fecha_observacion"][i])
                    xticks.append(i)
                except IndexError:
                    pass

            plt.xticks(
                ticks=xticks, labels=xlabels, fontname="Times New Roman", fontsize=6
            )

            plt.yticks(
                fontname="Times New Roman", fontsize=5, rotation=45
                )
            # ax.tick_params("y", which="both", pad=2, direction="in")
            ax.tick_params(axis="y", which="both", pad=1, direction="in")

            ax.ticklabel_format(style="plain", axis="y", useOffset=False)

            major_locator = ticker.AutoLocator()
            minor_locator = ticker.AutoMinorLocator()
            ax.yaxis.set_major_locator(major_locator)
            ax.yaxis.set_minor_locator(minor_locator)

            story = []
            story.append(Paragraph(
                f"Gravedad a 0 cm [μGal]", style5)
            )
            f = Frame(1.25 * cm, 24.75* cm, 19.5 * cm, 0.85 * cm, showBoundary=0)
            f.addFromList(story, p)

            # offset_text = ax.yaxis.get_offset_text()
            # if offset_text:
            #     fig.canvas.draw() # muestra el offset

            #     plt.setp(
            #         offset_text, fontname="Times New Roman", visible=False,
            #         fontsize=6, backgroundcolor="red",
            #     )

            #     offset_number = offset_text.get_text().strip("+")
            #     story = []
            #     story.append(Paragraph(
            #         f"Gravedad a 0 cm: {offset_number} μGal", style5)
            #     )
            #     f = Frame(1.25 * cm, 24.75* cm, 19.5 * cm, 0.85 * cm, showBoundary=0)
            #     f.addFromList(story, p)
            # else:
            #     story = []
            #     story.append(Paragraph(
            #         f"Gravedad a 0 cm [μGal]", style5)
            #     )
            #     f = Frame(1.25 * cm, 24.75* cm, 19.5 * cm, 0.85 * cm, showBoundary=0)
            #     f.addFromList(story, p)

            plt.grid(True)
            plt.grid(True, "minor", "y", linestyle=":")

            # tabla de datos
            estilo_tabla = [
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 1), (-1, -1), 6),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                # ('BOX', (0,0), (-1,-1), 1, colors.black),
                ('VALIGN',(0,-1),(-1,-1),'MIDDLE')
            ]

            if len (observaciones) < 26:
                datos_tabla = [
                    [
                        Paragraph("<b>Fecha de observación</b>", style6), Paragraph("<b>Gravedad observada [μGal]</b>", style6),
                        Paragraph("<b>Altura de observación [cm]</b>", style6), Paragraph("<b>Sets procesados [μGal]</b>", style6),
                        Paragraph("<b>Caídas por set [μGal]</b>", style6), Paragraph("<b>Dispersión entre sets [μGal]</b>", style6),                            
                        Paragraph("<b>Incertidumbre de la medida [μGal]</b>", style6), Paragraph("<b>Incertidumbre sistemática [μGal]</b>", style6),
                        Paragraph("<b>Incertidumbre total [μGal]</b>", style6), Paragraph("<b>Gravedad a 0 cm [μGal]</b>", style6),
                        Paragraph("<b>Gravímetro</b>", style6)
                    ],
                ]
                story = []
                for observacion in observaciones:
                    datos = []
                    datos.append(observacion.fecha_observacion)
                    datos.append(observacion.gravedad_observada)
                    datos.append(observacion.altura_de_observacion)
                    datos.append(observacion.sets_procesados)
                    datos.append(observacion.drops_por_set)
                    datos.append(observacion.dispersion)                        
                    datos.append(observacion.incertidumbre_medida)
                    datos.append(observacion.incertidumbre_sistematica)
                    datos.append(observacion.incertidumbre_total)
                    datos.append(observacion.gravedad_cero)
                    datos.append(observacion.gravimetro_observacion)

                    datos_tabla.append(datos)

                # tabla = Table(datos_tabla, style=estilo_tabla, colWidths=67.3)
                tabla = Table(datos_tabla, style=estilo_tabla)


                story.append(tabla)
                f = Frame(cm, 1.5 * cm, 19 * cm, 18.5 * cm, showBoundary=0)
                # t_keep = KeepInFrame()
                f.addFromList(story, p)

                imgdata = io.BytesIO()
                fig.savefig(imgdata, format="svg")
                imgdata.seek(0)  # rewind the data
                drawing = svg2rlg(imgdata)
                drawing.drawOn(p, - 2.065 * cm, 20.475 * cm)

                # pie de página
                p.setFillColorRGB(0, 0, 255)
                p.setFont("Times-Roman", 9)
                p.drawString(cm, 0.75 * cm, pageinfo[0])
                p.drawString(17 * cm, 0.75 * cm, pageinfo[1])

                p.showPage()

            else:
                datos_tabla = [
                    [
                        Paragraph("<b>Fecha de observación</b>", style6), Paragraph("<b>Gravedad observada [μGal]</b>", style6),
                        Paragraph("<b>Altura de observación [cm]</b>", style6), Paragraph("<b>Sets procesados [μGal]</b>", style6),
                        Paragraph("<b>Caídas por set [μGal]</b>", style6), Paragraph("<b>Dispersión entre sets [μGal]</b>", style6),                            
                        Paragraph("<b>Incertidumbre de la medida [μGal]</b>", style6), Paragraph("<b>Incertidumbre sistemática [μGal]</b>", style6),
                        Paragraph("<b>Incertidumbre total [μGal]</b>", style6), Paragraph("<b>Gravedad a 0 cm [μGal]</b>", style6),
                        Paragraph("<b>Gravímetro</b>", style6)
                    ],
                ]
                story = []
                for observacion in observaciones[:26]:
                    datos = []
                    datos.append(observacion.fecha_observacion)
                    datos.append(observacion.gravedad_observada)
                    datos.append(observacion.altura_de_observacion)
                    datos.append(observacion.sets_procesados)
                    datos.append(observacion.drops_por_set)
                    datos.append(observacion.dispersion)                        
                    datos.append(observacion.incertidumbre_medida)
                    datos.append(observacion.incertidumbre_sistematica)
                    datos.append(observacion.incertidumbre_total)
                    datos.append(observacion.gravedad_cero)
                    datos.append(observacion.gravimetro_observacion)

                    datos_tabla.append(datos)

                # tabla = Table(datos_tabla, style=estilo_tabla, colWidths=67.3)
                tabla = Table(datos_tabla, style=estilo_tabla)


                story.append(tabla)
                f = Frame(cm, 1.5 * cm, 19 * cm, 18.5 * cm, showBoundary=0)
                # t_keep = KeepInFrame()
                f.addFromList(story, p)

                imgdata = io.BytesIO()
                fig.savefig(imgdata, format="svg")
                imgdata.seek(0)  # rewind the data
                drawing = svg2rlg(imgdata)
                drawing.drawOn(p, - 2.065 * cm, 20.475 * cm)

                # pie de página
                p.setFillColorRGB(0, 0, 255)
                p.setFont("Times-Roman", 9)
                p.drawString(cm, 0.75 * cm, pageinfo[0])
                p.drawString(17 * cm, 0.75 * cm, pageinfo[1])

                p.showPage()

                # cabecera
                p.drawImage(logo, cm, 27 * cm, 9.5 * cm, 1.75 * cm, preserveAspectRatio=True, anchor="c")

                story = []
                story.append(Paragraph("INSTITUTO GEOGRÁFICO NACIONAL", style1))
                story.append(Spacer(0.25 * cm, 0.25 * cm))
                story.append(Paragraph("Servicio de Gravimetría", style2))
                f = Frame(10.5 * cm, 27.02 * cm, 9.5 * cm, 1.715 * cm, showBoundary=0)
                f.addFromList(story, p)
                p.line(11.625 * cm, 28.735 * cm, 18.875 * cm, 28.735 * cm)
                p.line(11.625 * cm, 27.0 * cm, 18.875 * cm, 27.0 * cm)

                story = []
                story.append(Paragraph("HISTORIAL DE OBSERVACIONES", style3))
                f = Frame(cm, 25.75 * cm, 19 * cm, 0.875 * cm, showBoundary=1)
                f.addFromList(story, p)

                datos_tabla = [
                    [
                        Paragraph("<b>Fecha de observación</b>", style6), Paragraph("<b>Gravedad observada [μGal]</b>", style6),
                        Paragraph("<b>Altura de observación [cm]</b>", style6), Paragraph("<b>Sets procesados [μGal]</b>", style6),
                        Paragraph("<b>Caídas por set [μGal]</b>", style6), Paragraph("<b>Dispersión entre sets [μGal]</b>", style6),                            
                        Paragraph("<b>Incertidumbre de la medida [μGal]</b>", style6), Paragraph("<b>Incertidumbre sistemática [μGal]</b>", style6),
                        Paragraph("<b>Incertidumbre total [μGal]</b>", style6), Paragraph("<b>Gravedad a 0 cm [μGal]</b>", style6),
                        Paragraph("<b>Gravímetro</b>", style6)
                    ],
                ]
                story = []
                for observacion in observaciones[26:]:
                    datos = []
                    datos.append(observacion.fecha_observacion)
                    datos.append(observacion.gravedad_observada)
                    datos.append(observacion.altura_de_observacion)
                    datos.append(observacion.sets_procesados)
                    datos.append(observacion.drops_por_set)
                    datos.append(observacion.dispersion)                        
                    datos.append(observacion.incertidumbre_medida)
                    datos.append(observacion.incertidumbre_sistematica)
                    datos.append(observacion.incertidumbre_total)
                    datos.append(observacion.gravedad_cero)
                    datos.append(observacion.gravimetro_observacion)

                    datos_tabla.append(datos)

                # tabla = Table(datos_tabla, style=estilo_tabla, colWidths=67.3)
                tabla = Table(datos_tabla, style=estilo_tabla)


                story.append(tabla)
                f = Frame(cm, 1.5 * cm, 19 * cm, 23.4 * cm, showBoundary=0)
                # t_keep = KeepInFrame()
                f.addFromList(story, p)

                # pie de página
                p.setFillColorRGB(0, 0, 255)
                p.setFont("Times-Roman", 9)
                p.drawString(cm, 0.75 * cm, pageinfo[0])
                p.drawString(17 * cm, 0.75 * cm, pageinfo[1])

                p.showPage()


        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=f'{punto_obs.estacion}_{punto_obs.id_punto_obs}.pdf')

    def get_form(self, request, obj=None, **kwargs):
        form = super(PuntoObsAdmin, self).get_form(request, obj, **kwargs)
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            pass
        else:
            form.base_fields['estacion'].widget.can_add_related = False
            form.base_fields['estacion'].widget.can_change_related = False
        return form

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return (
                "estacion", "id_punto_obs", "nombre", "tipo_senal", "estado_senal",
                "fecha_revision", "tipo_acceso", "latitud", "longitud", "altitud",
                "utm_x", "utm_y", "utm_zona", "descripcion", "imagen_nw", "imagen_ne",
                "imagen_sw", "imagen_se"
            )
        else:
            return super().get_readonly_fields(request, obj)



class ObservacionAdmin(admin.ModelAdmin):
    actions = [exportar_csv, exportar_xlsx]
    fieldsets = (
        (None, {
            "fields": (
                "estacion", "punto_obs", "publicable", "resenable"
            )
        }),
        ("Ficheros g", {
            "classes": ("collapse", "wide"),
            "fields": (
                "fichero_project", "fichero_set", "fichero_drop"
            )
        }),
        ("Observación y procesado", {
            "classes": ("collapse", "wide"),
            "fields": (
                ("fecha_observacion", "fecha_procesado"),
                ("operador_observacion", "operador_procesado"), "tipo_gradiente",
                "observaciones_medida", "observaciones_procesado"
            )
        }),
            ("Instrumentación", {
            "classes": ("collapse", "wide"),
            "fields": (
                "gravimetro_observacion", "gravimetro_gradiente",
            )
        }),  
            ("Resultados de la observación", {
            "classes": ("collapse", "wide"),
            "fields": (
                ("gravedad_procesada", "altura_de_procesado"), ("gravedad_observada",
                "altura_de_observacion", "altura_de_montaje"), "gravedad_cero",
                ("gradiente_vertical", "incertidumbre_gradiente"), "dispersion",
                "incertidumbre_medida", "incertidumbre_sistematica", "incertidumbre_total",
                "sets_observados", "sets_procesados", "drops_por_set"
            )
        }),  
    )
    autocomplete_fields = ["estacion", "operador_procesado"]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    list_display = (
        "estacion_link", "punto_obs_link", "fecha_observacion", 
        "fecha_procesado", "gravimetro_link", "gravedad_procesada_display", 
        "altura_de_procesado", "gravedad_observada_display", "altura_de_observacion", 
        "altura_de_montaje", "gravedad_cero_display", "dispersion_display", 
        "incertidumbre_medida_display", "incertidumbre_sistematica_display", "incertidumbre_total_display", 
        "sets_observados", "sets_procesados", "drops_por_set",
        "tipo_gradiente", "gradiente_display", "incertidumbre_gradiente_display", 
        "gravimetro_gradiente_link",
        )
    list_display_links = ("gravedad_procesada_display",)
    list_filter = (
        TipoObsListFilterForObservacion, GravimetroListFilterForObservacion,
        GravimetroGradienteListFilterForObservacion, TipoGradienteListFilterForObservacion,
        PublicableListFilterForObservacion, DispersionListFilterForObservacion,
        IncertidumbreTotalListFilterForObservacion, OperadorObservacionListFilterForObservacion,
        OperadorProcesadoListFilterForObservacion, FicheroListFilterForObservacion,
        ComAutonomaListFilterForObservacion, ProvinciaListFilterForObservacion,
        IslaListFilterForObservacion, MunicipioListFilterForObservacion,
        EstacionListFilterForObservacion
    )
    list_max_show_all = 1000
    search_fields = ("estacion__id_estacion",)
    search_help_text = "Búqueda por ID estación"
    show_full_result_count = True


    def get_form(self, request, obj=None, **kwargs):
        form = super(ObservacionAdmin, self).get_form(request, obj, **kwargs)
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            pass
        else:
            form.base_fields['estacion'].widget.can_add_related = False
            form.base_fields['estacion'].widget.can_change_related = False
            form.base_fields['punto_obs'].widget.can_add_related = False
            form.base_fields['punto_obs'].widget.can_change_related = False
            form.base_fields['operador_observacion'].widget.can_add_related = False
            form.base_fields['operador_procesado'].widget.can_add_related = False
            form.base_fields['operador_procesado'].widget.can_change_related = False
            form.base_fields['operador_procesado'].widget.can_delete_related = False
            form.base_fields['gravimetro_observacion'].widget.can_add_related = False
            form.base_fields['gravimetro_observacion'].widget.can_change_related = False
            form.base_fields['gravimetro_observacion'].widget.can_delete_related = False
            form.base_fields['gravimetro_gradiente'].widget.can_add_related = False
            form.base_fields['gravimetro_gradiente'].widget.can_change_related = False
            form.base_fields['gravimetro_gradiente'].widget.can_delete_related = False  
        return form

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            extra_context = extra_context or {}
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context) 

    def get_readonly_fields(self, request, obj=None):
        usuario = User.objects.get(pk=request.user.pk)
        if usuario.is_superuser == False and "Administradores" not in usuario.groups.values_list('name', flat=True):
            return (
                "estacion", "punto_obs", "publicable", "fichero_project", "fichero_set",
                "fichero_drop", "fecha_observacion", "fecha_procesado", "operador_observacion",
                "operador_procesado", "tipo_gradiente", "observaciones_medida",
                "observaciones_procesado", "gravimetro_observacion", "gravimetro_gradiente",
                "gravedad", "dispersion", "incertidumbre_medida", "incertidumbre_sistematica",
                "incertidumbre_total", "sets_observados", "sets_procesados", "drops_por_set",
                "gradiente_vertical", "incertidumbre_gradiente", "altura_de_montaje",
                "altura_de_observacion", "altura_de_procesado", "gravedad_cero"
            )
        else:
            return super().get_readonly_fields(request, obj)


# Register your models here.
admin.site.register(Red, RedAdmin)
admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(Gravimetro, GravimetroAdmin)
admin.site.register(Mantenimiento, MantenimientoAdmin)
admin.site.register(Operador, OperadorAdmin)
admin.site.register(Estacion, EstacionAdmin)
admin.site.register(PuntoObs, PuntoObsAdmin)
admin.site.register(Observacion, ObservacionAdmin)