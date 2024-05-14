from django.contrib.gis import admin
from hojasmtn.models import HojaMtn25, HojaMtn50
from leaflet.admin import LeafletGeoAdmin


class HojaMtn25Admin(LeafletGeoAdmin):
    fields = ("nombre", "hoja", "geom")
    list_display = ("hoja", "nombre")
    readonly_fields = ("nombre", "hoja")
    search_fields = ("nombre", "hoja")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False        
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)


class HojaMtn50Admin(LeafletGeoAdmin):
    fields = ("nombre", "hoja", "geom")
    list_display = ("hoja", "nombre")
    readonly_fields = ("nombre", "hoja")
    search_fields = ("nombre", "hoja")

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
admin.site.register(HojaMtn25, HojaMtn25Admin)
admin.site.register(HojaMtn50, HojaMtn50Admin)