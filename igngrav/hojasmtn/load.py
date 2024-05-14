from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import HojaMtn25, HojaMtn50


# # subida de hojas mtn25
# hojamtn25_mapping = {
#     'hoja': 'MTN25_CLAS',
#     'nombre': 'NOMBRE_25',
#     'geom': 'MULTIPOLYGON',
# }

# hojamtn25_shp = Path(__file__).resolve().parent / 'shapefiles' / 'mtn25' / 'MTN25_ETRS89_Peninsula_Baleares_Canarias.shp'

# def hojamtn25_run(verbose=True):
#     lm = LayerMapping(HojaMtn25, hojamtn25_shp, hojamtn25_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)

# # subida de hojas mtn50
# hojamtn50_mapping = {
#     'hoja': 'MTN50_CLAS',
#     'nombre': 'NOMBRE_50',
#     'geom': 'MULTIPOLYGON',
# }

# hojamtn50_shp = Path(__file__).resolve().parent / 'shapefiles' / 'mtn50' / 'MTN50_ETRS89_Peninsula_Baleares_Canarias.shp'

# def hojamtn50_run(verbose=True):
#     lm = LayerMapping(HojaMtn50, hojamtn50_shp, hojamtn50_mapping, transform=True)
#     lm.save(step=10, strict=True, verbose=verbose)
