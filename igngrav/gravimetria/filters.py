# from datetime import datetime
# from django.db.models import TextField, query
# from django.db.models.functions import Length
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from gravimetria.models import *
from unidadmin.models import *


class GravimetroListFilterForMantenimiento(admin.SimpleListFilter):
    title = _("gravímetro")
    parameter_name = "gravimetro"

    def lookups(self, request, model_admin):
        gravimetros = Gravimetro.objects.all()
        mis_lookups = [
            (gravimetro.pk, _(f"{gravimetro.get_modelo_display()}#{gravimetro.numero_serie}")) for gravimetro in gravimetros
        ]
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(gravimetro=self.value())
        else:
            return queryset


class TipoMantenimientoListFilterForMantenimiento(admin.SimpleListFilter):
    title = _("tipo de tarea realizada")
    parameter_name = "tipo_mantenimiento"

    def lookups(self, request, model_admin):
        mis_lookups = (
        (1, _("Cambio de la correa")),
        (2, _("Cambio de la bomba iónica")),
        (3, _("Mantenimiento del láser")),
        (4, _("Calibración del láser")),
        (5, _("Calibración del reloj")),
        (6, _("Electrónica")),
        (7, _("Comparación")),
        (8, _("Deriva de gravímetro relativo")),
        (9, _("Offset de los inclinómetros")),
        (10, _("Sensibilidad de los inclinómetros")),
        (11, _("Acoplamiento transversal del trípode")),
        (0, _("Otra"))
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(tipo_mantenimiento=self.value())
        else:
            return queryset


class RedPrimariaListFilterForEstacion(admin.SimpleListFilter):
    title = _("pertenencia a REGA")
    parameter_name = "red_primaria"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("Sí")),
            ("0", _("No"))
        )
        return mis_lookups

    def queryset(self, request, queryset):        
        if self.value() == "1":
            return queryset.filter(red_primaria__isnull=False)
        elif self.value() == "0":
            return queryset.filter(red_primaria__isnull=True)
        else:
            return queryset


class RedSecundariaListFilterForEstacion(admin.SimpleListFilter):
    title = "otras redes con las que enlaza"
    parameter_name = "red_secundaria"

    def lookups(self, request, model_admin):
        redes = Red.objects.exclude(nombre="REGA")
        mis_lookups = [
            (red.pk, _(red.nombre)) for red in redes
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(red_secundaria=self.value())
        else:
            return queryset   


class ComAutonomaListFilterForEstacion(admin.SimpleListFilter):
    title = _("comunidad autónoma")
    parameter_name = "com_autonoma"

    def lookups(self, request, model_admin):
        comunidades = ComAutonoma.objects.exclude(estacion__isnull=True)
        mis_lookups = [
            (comunidad.pk, _(comunidad.nombre)) for comunidad in comunidades
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(com_autonoma=self.value())
        else:
            return queryset


class ProvinciaListFilterForEstacion(admin.SimpleListFilter):
    title = _("provincia")
    parameter_name = "provincia"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincias = Provincia.objects.exclude(estacion__isnull=True)
        if com_autonoma != None:
            provincias = provincias.filter(com_autonoma=com_autonoma)
        else:
            pass
        mis_lookups = [
            (provincia.pk, _(provincia.nombre)) for provincia in provincias
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(provincia=self.value())
        else:
            return queryset


class IslaListFilterForEstacion(admin.SimpleListFilter):
    title = _("isla")
    parameter_name = "isla"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        islas = Isla.objects.exclude(estacion__isnull=True)
        if com_autonoma != None and provincia != None:
            islas = islas.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif com_autonoma != None:
            islas = islas.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            islas = islas.filter(provincia=provincia)
        else:
            pass
        mis_lookups = [
            (isla.pk, _(isla.nombre)) for isla in islas
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(isla=self.value())
        else:
            return queryset


class MunicipioListFilterForEstacion(admin.SimpleListFilter):
    title = _("municipio")
    parameter_name = "municipio"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        isla = request.GET.get("isla")
        municipios = Municipio.objects.exclude(estacion__isnull=True)
        if com_autonoma != None and provincia != None and isla != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and provincia != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif provincia != None and isla != None:
            municipios = municipios.filter(provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and isla != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(isla=isla)
        elif com_autonoma != None:
            municipios = municipios.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            municipios = municipios.filter(provincia=provincia)
        elif isla != None:
            municipios = municipios.filter(isla=isla)
        else:
            pass
        mis_lookups = [
            (municipio.pk, _(municipio.nombre)) for municipio in municipios
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(municipio=self.value())
        else:
            return queryset


class RedPrimariaListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("pertenencia a REGA")
    parameter_name = "red_primaria"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("Sí")),
            ("0", _("No"))
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(estacion__red_primaria__isnull=False)
        elif self.value() == "0":
            return queryset.filter(estacion__red_primaria__isnull=True)
        else:
            return queryset


class RedSecundariaListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("otras redes con las que enlaza")
    parameter_name = "red_secundaria"

    def lookups(self, request, model_admin):
        redes = Red.objects.exclude(nombre="REGA")
        mis_lookups = [
            (red.pk, _(red.nombre)) for red in redes
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__red_secundaria=self.value())
        else:
            return queryset


class TipoSenalListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("tipo de señalización")
    parameter_name = "tipo_senal"

    def lookups(self, request, model_admin):
        mis_lookups = (
        (1, _("Pilar")),
        (2, _("Clavo")),
        (3, _("Marca")),
        (4, _("Sin señalizar")),
        (5, _("Desconocido"))
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(tipo_senal=self.value())
        else:
            return queryset


class EstadoSenalListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("estado de la señal")
    parameter_name = "estado_senal"

    def lookups(self, request, model_admin):
        mis_lookups = (
            (1, _("Buen estado")),
            (2, _("Mal estado")),
            (3, _("Desconocido"))
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estado_senal=self.value())
        else:
            return queryset


class TipoAccesoListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("tipo de acceso")
    parameter_name = "tipo_acceso"

    def lookups(self, request, model_admin):
        mis_lookups = (
            (1, _("Público")),
            (2, _("Privado")),
            (3, _("Desconocido"))
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(tipo_acceso=self.value())
        else:
            return queryset


class DescripcionListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("incluir descripción del punto")
    parameter_name = "descripcion"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("Sí")),
            ("0", _("No"))
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(tiene_descripcion=True)
        elif self.value() == "0":
            return queryset.filter(tiene_descripcion=False)
        else:
            return queryset


class NumeroFotosListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("número de fotos para la reseña")
    parameter_name = "num_fotos"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("4", _("4")),
            ("3", _("3")),
            ("2", _("2")),
            ("1", _("1")),
            ("0", _("Ninguna"))
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() == "4":
            return queryset.filter(num_fotos=4)
        elif self.value() == "3":
            return queryset.filter(num_fotos=3)
        elif self.value() == "2":
            return queryset.filter(num_fotos=2)
        elif self.value() == "1":
            return queryset.filter(num_fotos=1)
        elif self.value() == "0":
            return queryset.filter(num_fotos=0)
        else:
            return queryset


class ComAutonomaListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("comunidad autónoma")
    parameter_name = "com_autonoma"

    def lookups(self, request, model_admin):
        comunidades = ComAutonoma.objects.exclude(estacion__isnull=True)
        mis_lookups = [
            (comunidad.pk, _(comunidad.nombre)) for comunidad in comunidades
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__com_autonoma=self.value())
        else:
            return queryset


class ProvinciaListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("provincia")
    parameter_name = "provincia"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincias = Provincia.objects.exclude(estacion__isnull=True)
        if com_autonoma != None:
            provincias = provincias.filter(com_autonoma=com_autonoma)
        else:
            pass
        mis_lookups = [
            (provincia.pk, _(provincia.nombre)) for provincia in provincias
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__provincia=self.value())
        else:
            return queryset


class IslaListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("isla")
    parameter_name = "isla"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        islas = Isla.objects.exclude(estacion__isnull=True)
        if com_autonoma != None and provincia != None:
            islas = islas.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif com_autonoma != None:
            islas = islas.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            islas = islas.filter(provincia=provincia)
        else:
            pass
        mis_lookups = [
            (isla.pk, _(isla.nombre)) for isla in islas
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__isla=self.value())
        else:
            return queryset


class MunicipioListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("municipio")
    parameter_name = "municipio"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        isla = request.GET.get("isla")
        municipios = Municipio.objects.exclude(estacion__isnull=True)
        if com_autonoma != None and provincia != None and isla != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and provincia != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif provincia != None and isla != None:
            municipios = municipios.filter(provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and isla != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(isla=isla)
        elif com_autonoma != None:
            municipios = municipios.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            municipios = municipios.filter(provincia=provincia)
        elif isla != None:
            municipios = municipios.filter(isla=isla)
        else:
            pass
        mis_lookups = [
            (municipio.pk, _(municipio.nombre)) for municipio in municipios
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__municipio=self.value())
        else:
            return queryset


class EstacionListFilterForPuntoObs(admin.SimpleListFilter):
    title = _("estación")
    parameter_name = "estacion"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        isla = request.GET.get("isla")
        municipio = request.GET.get("municipio")
        estaciones = Estacion.objects.all()
        if com_autonoma != None and provincia != None and isla != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(isla=isla).filter(municipio=municipio)
        elif com_autonoma != None and provincia != None and isla != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and provincia != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(municipio=municipio)
        elif com_autonoma != None and isla != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                isla=isla).filter(municipio=municipio)
        elif provincia != None and isla != None and municipio != None:
            estaciones = estaciones.filter(provincia=provincia).filter(
                isla=isla).filter(municipio=municipio)
        elif com_autonoma != None and provincia != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif com_autonoma != None and isla != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(isla=isla)
        elif com_autonoma != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(municipio=municipio)
        elif provincia != None and isla != None:
            estaciones = estaciones.filter(provincia=provincia).filter(isla=isla)
        elif provincia != None and municipio != None:
            estaciones = estaciones.filter(provincia=provincia).filter(municipio=municipio)
        elif isla != None and municipio != None:
            estaciones = estaciones.filter(isla=isla).filter(municipio=municipio)
        elif com_autonoma != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            estaciones = estaciones.filter(provincia=provincia)
        elif isla != None:
            estaciones = estaciones.filter(isla=isla)
        elif municipio != None:
            estaciones = estaciones.filter(municipio=municipio)      
        else:
            pass
        mis_lookups = [
            (estacion.pk, _(estacion.id_estacion)) for estacion in estaciones
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion=self.value())
        else:
            return queryset


class PublicableListFilterForObservacion(admin.SimpleListFilter):
    title = _("si es o no publicable")
    parameter_name = "publicable"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("Sí")),
            ("0", _("No"))         
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(publicable=True)
        elif self.value() == "0":
            return queryset.filter(publicable=False)
        else:
            return queryset     


class DispersionListFilterForObservacion(admin.SimpleListFilter):
    title = _("dispersión entre sets [μGal]")
    parameter_name = "dispersion"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("< 2")),
            ("2", _("2 - 6")),
            ("3", _("6 - 12")),
            ("4", _("> 12")),            
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(dispersion__lt=2)
        elif self.value() == "2":
            return queryset.filter(dispersion__gte=2).filter(dispersion__lte=6)
        elif self.value() == "3":
            return queryset.filter(dispersion__gte=6).filter(dispersion__lte=12)
        elif self.value() == "4":
            return queryset.filter(dispersion__gt=12)
        else:
            return queryset


class IncertidumbreTotalListFilterForObservacion(admin.SimpleListFilter):
    title = _("incertidumbre total [μGal]")
    parameter_name = "incertidumbre_total"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("< 2")),
            ("2", _("2 - 6")),
            ("3", _("6 - 12")),
            ("4", _("> 12")),            
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(incertidumbre_total__lt=2)
        elif self.value() == "2":
            return queryset.filter(incertidumbre_total__gte=2).filter(incertidumbre_total__lte=6)
        elif self.value() == "3":
            return queryset.filter(incertidumbre_total__gte=6).filter(incertidumbre_total__lte=12)
        elif self.value() == "4":
            return queryset.filter(incertidumbre_total__gt=12)
        else:
            return queryset


class TipoObsListFilterForObservacion(admin.SimpleListFilter):
    title = _("tipo de observación")
    parameter_name = "tipo_observacion"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("Absoluta")),
            ("2", _("Relativa"))         
        )
        return mis_lookups

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.filter(gravimetro_observacion__tipo_gravimetro=1)
        elif self.value() == "2":
            return queryset.filter(gravimetro_observacion__tipo_gravimetro=2)
        else:
            return queryset


class GravimetroListFilterForObservacion(admin.SimpleListFilter):
    title = _("gravímetro empleado")
    parameter_name = "gravimetro_observacion"

    def lookups(self, request, model_admin):
        tipo_observacion = request.GET.get("tipo_observacion")
        gravimetros = Gravimetro.objects.exclude(gravimetro_observacion__isnull=True)
        if tipo_observacion != None:
            gravimetros = gravimetros.filter(tipo_gravimetro=tipo_observacion)
        else:
            pass
        mis_lookups = [
            (gravimetro.pk, _(f"{gravimetro.get_modelo_display()}#{gravimetro.numero_serie}")) for gravimetro in gravimetros
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(gravimetro_observacion=self.value())
        else:
            return queryset


class GravimetroGradienteListFilterForObservacion(admin.SimpleListFilter):
    title = _("gravímetro empleado en el gradiente")
    parameter_name = "gravimetro_gradiente"

    def lookups(self, request, model_admin):
        gravimetros = Gravimetro.objects.exclude(gravimetro_gradiente__isnull=True)
        mis_lookups = [
            (gravimetro.pk, _(f"{gravimetro.get_modelo_display()}#{gravimetro.numero_serie}")) for gravimetro in gravimetros
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(gravimetro_gradiente=self.value())
        else:
            return queryset


class TipoGradienteListFilterForObservacion(admin.SimpleListFilter):
    title = _("tipo de gradiente")
    parameter_name = "tipo_gradiente"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("Teórico")),
            ("2", _("Observado"))         
        )
        return mis_lookups

    def queryset(self, request, queryset):        
        if self.value() == "1":
            return queryset.filter(tipo_gradiente=1)
        elif self.value() == "2":
            return queryset.filter(tipo_gradiente=2)
        else:
            return queryset

class OperadorObservacionListFilterForObservacion(admin.SimpleListFilter):
    title = _("operador que participó en la observación")
    parameter_name = "operador_observacion"

    def lookups(self, request, model_admin):
        operadores = Operador.objects.exclude(operador_observacion__isnull=True)
        mis_lookups = [
            (operador.pk, _(operador.nombre)) for operador in operadores
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(operador_observacion=self.value())
        else:
            return queryset


class OperadorProcesadoListFilterForObservacion(admin.SimpleListFilter):
    title = _("operador realizó el procesado")
    parameter_name = "operador_procesado"

    def lookups(self, request, model_admin):
        operadores = Operador.objects.exclude(operador_procesado__isnull=True)
        mis_lookups = [
            (operador.pk, _(operador.nombre)) for operador in operadores
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(operador_procesado=self.value())
        else:
            return queryset


class FicheroListFilterForObservacion(admin.SimpleListFilter):
    title = _("tipo de fichero ausente")
    parameter_name = "fichero_ausente"

    def lookups(self, request, model_admin):
        mis_lookups = (
            ("1", _("Fichero project")),
            ("2", _("Fichero set")),
            ("3", _("Fichero drop"))
        )
        return mis_lookups
    
    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.exclude(fichero_project__contains="project")
        elif self.value() == "2":
            return queryset.exclude(fichero_set__contains="set")
        elif self.value() == "3":
            return queryset.exclude(fichero_drop__contains="drop")
        else:
            return queryset

class ComAutonomaListFilterForObservacion(admin.SimpleListFilter):
    title = _("comunidad autónoma")
    parameter_name = "com_autonoma"

    def lookups(self, request, model_admin):
        comunidades = ComAutonoma.objects.exclude(estacion__isnull=True)
        mis_lookups = [
            (comunidad.pk, _(comunidad.nombre)) for comunidad in comunidades
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__com_autonoma=self.value())
        else:
            return queryset


class ProvinciaListFilterForObservacion(admin.SimpleListFilter):
    title = _("provincia")
    parameter_name = "provincia"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincias = Provincia.objects.exclude(estacion__isnull=True)
        if com_autonoma != None:
            provincias = provincias.filter(com_autonoma=com_autonoma)
        else:
            pass
        mis_lookups = [
            (provincia.pk, _(provincia.nombre)) for provincia in provincias
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__provincia=self.value())
        else:
            return queryset


class IslaListFilterForObservacion(admin.SimpleListFilter):
    title = _("isla")
    parameter_name = "isla"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        islas = Isla.objects.exclude(estacion__isnull=True)
        if com_autonoma != None and provincia != None:
            islas = islas.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif com_autonoma != None:
            islas = islas.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            islas = islas.filter(provincia=provincia)
        else:
            pass
        mis_lookups = [
            (isla.pk, _(isla.nombre)) for isla in islas
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__isla=self.value())
        else:
            return queryset


class MunicipioListFilterForObservacion(admin.SimpleListFilter):
    title = _("municipio")
    parameter_name = "municipio"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        isla = request.GET.get("isla")
        municipios = Municipio.objects.exclude(estacion__isnull=True)
        if com_autonoma != None and provincia != None and isla != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and provincia != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif provincia != None and isla != None:
            municipios = municipios.filter(provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and isla != None:
            municipios = municipios.filter(com_autonoma=com_autonoma).filter(isla=isla)
        elif com_autonoma != None:
            municipios = municipios.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            municipios = municipios.filter(provincia=provincia)
        elif isla != None:
            municipios = municipios.filter(isla=isla)
        else:
            return municipios.none()
        mis_lookups = [
            (municipio.pk, _(municipio.nombre)) for municipio in municipios
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion__municipio=self.value())
        else:
            return queryset


class EstacionListFilterForObservacion(admin.SimpleListFilter):
    title = _("estación")
    parameter_name = "estacion"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        isla = request.GET.get("isla")
        municipio = request.GET.get("municipio")
        estaciones = Estacion.objects.all()
        if com_autonoma != None and provincia != None and isla != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(isla=isla).filter(municipio=municipio)
        elif com_autonoma != None and provincia != None and isla != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(isla=isla)
        elif com_autonoma != None and provincia != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                provincia=provincia).filter(municipio=municipio)
        elif com_autonoma != None and isla != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(
                isla=isla).filter(municipio=municipio)
        elif provincia != None and isla != None and municipio != None:
            estaciones = estaciones.filter(provincia=provincia).filter(
                isla=isla).filter(municipio=municipio)
        elif com_autonoma != None and provincia != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif com_autonoma != None and isla != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(isla=isla)
        elif com_autonoma != None and municipio != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma).filter(municipio=municipio)
        elif provincia != None and isla != None:
            estaciones = estaciones.filter(provincia=provincia).filter(isla=isla)
        elif provincia != None and municipio != None:
            estaciones = estaciones.filter(provincia=provincia).filter(municipio=municipio)
        elif isla != None and municipio != None:
            estaciones = estaciones.filter(isla=isla).filter(municipio=municipio)
        elif com_autonoma != None:
            estaciones = estaciones.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            estaciones = estaciones.filter(provincia=provincia)
        elif isla != None:
            estaciones = estaciones.filter(isla=isla)
        elif municipio != None:
            estaciones = estaciones.filter(municipio=municipio)      
        else:
            return estaciones.none()
        mis_lookups = [
            (estacion.pk, _(estacion.id_estacion)) for estacion in estaciones
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(estacion=self.value())
        else:
            return queryset
