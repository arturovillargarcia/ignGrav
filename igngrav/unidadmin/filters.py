from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unidadmin.models import *


class ComAutonomaListFilter(admin.SimpleListFilter):
    title = _("comunidad autónoma")
    parameter_name = "com_autonoma"

    def lookups(self, request, model_admin):
        comunidades = ComAutonoma.objects.all()
        mis_lookups = [
            (comunidad.pk, _(comunidad.nombre)) for comunidad in comunidades
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(com_autonoma=self.value())
        else:
            return queryset


class ProvinciaListFilter(admin.SimpleListFilter):
    title = _("provincia")
    parameter_name = "provincia"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        if com_autonoma != None:
            provincias = Provincia.objects.filter(com_autonoma=com_autonoma)
        else:
            provincias = Provincia.objects.all()
        mis_lookups = [
            (provincia.pk, _(provincia.nombre)) for provincia in provincias
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(provincia=self.value())
        else:
            return queryset


class IslaListFilter(admin.SimpleListFilter):
    title = _("isla")
    parameter_name = "isla"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincia = request.GET.get("provincia")
        if com_autonoma != None and provincia != None:
            islas = Isla.objects.filter(com_autonoma=com_autonoma).filter(provincia=provincia)
        elif com_autonoma != None:
            islas = Isla.objects.filter(com_autonoma=com_autonoma)
        elif provincia != None:
            islas = Isla.objects.filter(provincia=provincia)
        else:
            islas = Isla.objects.all()
        mis_lookups = [
            (isla.pk, _(isla.nombre)) for isla in islas
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(isla=self.value())
        else:
            return queryset


class ComAutonomaListFilterForIsla(admin.SimpleListFilter):
    title = _("comunidad autónoma")
    parameter_name = "com_autonoma"

    def lookups(self, request, model_admin):
        comunidades = ComAutonoma.objects.exclude(isla__isnull=True)
        mis_lookups = [
            (comunidad.pk, _(comunidad.nombre)) for comunidad in comunidades
        ]
        return tuple(mis_lookups)

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(com_autonoma=self.value())
        else:
            return queryset


class ProvinciaListFilterForIsla(admin.SimpleListFilter):
    title = _("provincia")
    parameter_name = "provincia"

    def lookups(self, request, model_admin):
        com_autonoma = request.GET.get("com_autonoma")
        provincias = Provincia.objects.exclude(isla__isnull=True)
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
