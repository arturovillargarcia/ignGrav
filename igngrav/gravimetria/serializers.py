from django.contrib.gis import admin
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from gravimetria.models import Estacion, PuntoObs, Observacion
from pathlib import Path
import json
from djgeojson.serializers import Serializer as GeoJSONSerializer
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class EstacionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Estacion
        geo_field = "geom"
        fields = ["nombre"]

# serializer = EstacionSerializer(Estacion.objects.all(), many=True)


# class ObservacionSerializer(serializers.Serializer):



@admin.action(description="Exportar elementos seleccionados en formato geojson")
def exportar_geojson(modeladmin, request, queryset):
    serializer = EstacionSerializer(queryset, many=True)

    # response = JsonResponse(serializer.data, safe=True).content

    response = HttpResponse(
        serializer,
        content_type='application/json',
        headers={'Content-Disposition': 'attachment; filename="Observaciones.geojson"'},
    )

    # response = HttpResponse(
    #     # serialize(
    #     #     format="geojson", queryset=queryset,
    #     #     # fields=("id_estacion", "id_punto_obs")
    #     # ),
    #     GeoJSONSerializer().serialize(Observacion.objects.all()),
    #     content_type='application/json',
    #     headers={'Content-Disposition': 'attachment; filename="Observaciones.geojson"'},
    # )
    print(serializer)
    return response