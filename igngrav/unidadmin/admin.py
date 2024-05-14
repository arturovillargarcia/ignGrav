from django.contrib.gis import admin
from unidadmin.filters import ProvinciaListFilter, ComAutonomaListFilter, \
    IslaListFilter, ComAutonomaListFilterForIsla, ProvinciaListFilterForIsla
from leaflet.admin import LeafletGeoAdmin
from unidadmin.models import Pais, ComAutonoma, Provincia, Municipio, Isla


class PaisAdmin(LeafletGeoAdmin):
    fields = ("nombre", "geom")
    readonly_fields = ("nombre",)
    search_fields = ("nombre",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False        
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)


class ComAutonomaAdmin(LeafletGeoAdmin):
    fields = ("nombre", "geom")
    # list_display = ("nombre", "estaciones_link", "cobertura_estaciones")
    list_display = ("nombre", "estaciones_link")
    readonly_fields = ("nombre",)
    search_fields = ("nombre",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False        
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)


class ProvinciaAdmin(LeafletGeoAdmin):
    fields = ("nombre", "com_autonoma", "geom")
    # list_display = ("nombre", "estaciones_link", "cobertura_estaciones")
    list_display = ("nombre", "estaciones_link")
    list_filter = (ComAutonomaListFilter,)
    readonly_fields = ("nombre", "com_autonoma")
    search_fields = ("nombre",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False        
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)


class IslaAdmin(LeafletGeoAdmin):
    fields = ("nombre", "provincia", "com_autonoma", "geom")
    list_display = ("nombre", "estaciones_link")
    list_filter = (ComAutonomaListFilterForIsla, ProvinciaListFilterForIsla)
    readonly_fields = ("nombre", "provincia", "com_autonoma")
    search_fields = ("nombre",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False        
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)


class MunicipioAdmin(LeafletGeoAdmin):
    fields = ("nombre", "isla", "provincia", "com_autonoma", "geom")
    list_display = ("nombre", "estaciones_link")
    list_filter = (ComAutonomaListFilter, ProvinciaListFilter, IslaListFilter)
    readonly_fields = ("nombre", "isla", "provincia", "com_autonoma")
    search_fields = ("nombre",)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False        
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)


# Register your models here.
admin.site.register(Pais, PaisAdmin)
admin.site.register(ComAutonoma, ComAutonomaAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Isla, IslaAdmin)
admin.site.register(Municipio, MunicipioAdmin)
