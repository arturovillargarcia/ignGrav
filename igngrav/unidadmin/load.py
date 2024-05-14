from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Pais, ComAutonoma, Provincia, Isla, Municipio

# # subida de paises
# pais_mapping = {
#     'nombre': 'NAME_ENGL',
#     'geom': 'MULTIPOLYGON',
# }

# pais_shp = Path(__file__).resolve().parent / 'shapefiles' / 'paises' / 'CNTR_RG_01M_2020_4326.shp'

# def pais_run(verbose=True):
#     lm = LayerMapping(Pais, pais_shp, pais_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de comunidades wgs84
# comautonoma_wgs84_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# comautonoma_wgs84_shp = Path(__file__).resolve().parent / 'shapefiles' / 'comunidades' / 'recintos_autonomicas_inspire_canarias_wgs84.shp'

# def comautonoma_wgs84_run(verbose=True):
#     lm = LayerMapping(ComAutonoma, comautonoma_wgs84_shp, comautonoma_wgs84_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de comunidades etrs89
# comautonoma_etrs89_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# comautonoma_etrs89_shp = Path(__file__).resolve().parent / 'shapefiles' / 'comunidades' / 'recintos_autonomicas_inspire_peninbal_etrs89.shp'

# def comautonoma_etrs89_run(verbose=True):
#     lm = LayerMapping(ComAutonoma, comautonoma_etrs89_shp, comautonoma_etrs89_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de provincias wgs84
# provincia_wgs84_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# provincia_wgs84_shp = Path(__file__).resolve().parent / 'shapefiles' / 'provincias' / 'recintos_provinciales_inspire_canarias_wgs84.shp'

# def provincia_wgs84_run(verbose=True):
#     lm = LayerMapping(Provincia, provincia_wgs84_shp, provincia_wgs84_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de provincias etrs89
# provincia_etrs89_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# provincia_etrs89_shp = Path(__file__).resolve().parent / 'shapefiles' / 'provincias' / 'recintos_provinciales_inspire_peninbal_etrs89.shp'

# def provincia_etrs89_run(verbose=True):
#     lm = LayerMapping(Provincia, provincia_etrs89_shp, provincia_etrs89_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de islas wgs84
# isla_wgs84_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# isla_wgs84_shp = Path(__file__).resolve().parent / 'shapefiles' / 'islas' / 'recintos_islas_canarias_wgs84.shp'

# def isla_wgs84_run(verbose=True):
#     lm = LayerMapping(Isla, isla_wgs84_shp, isla_wgs84_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de islas etrs89
# isla_etrs89_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# isla_etrs89_shp = Path(__file__).resolve().parent / 'shapefiles' / 'islas' / 'recintos_islas_baleares_etrs89.shp'

# def isla_etrs89_run(verbose=True):
#     lm = LayerMapping(Isla, isla_etrs89_shp, isla_etrs89_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de municipios wgs84
# municipio_wgs84_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# municipio_wgs84_shp = Path(__file__).resolve().parent / 'shapefiles' / 'municipios' / 'recintos_municipales_inspire_canarias_wgs84.shp'

# def municipio_wgs84_run(verbose=True):
#     lm = LayerMapping(Municipio, municipio_wgs84_shp, municipio_wgs84_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de municipios etrs89
# municipio_etrs89_mapping = {
#     'nombre': 'NAMEUNIT',
#     'geom': 'MULTIPOLYGON',
# }

# municipio_etrs89_shp = Path(__file__).resolve().parent / 'shapefiles' / 'municipios' / 'recintos_municipales_inspire_peninbal_etrs89.shp'

# def municipio_etrs89_run(verbose=True):
#     lm = LayerMapping(Municipio, municipio_etrs89_shp, municipio_etrs89_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)