from django.http import HttpResponse
from django.template import loader
from gravimetria.models import Estacion, Observacion, Gravimetro, PuntoObs
from django.shortcuts import render
from django.core import serializers
from django.conf import settings
import json
import ast
import csv
import os

def visualizador(request):
  template = loader.get_template('index.html')
  
  data = serializers.serialize('json', Estacion.objects.all())
  obs = serializers.serialize('json', Observacion.objects.all(),
  fields=(
    "estacion", "punto_obs", "publicable", "resenable", "fichero_project", 
    "fichero_set", "fichero_drop", "fecha_observacion", "fecha_procesado", 
    "operador_observacion", "operador_procesado", "tipo_gradiente",
    "gravimetro_observacion", "gravimetro_gradiente", "gradiente_vertical",
    "incertidumbre_gradiente", "gravedad_procesada", "gravedad_observada",
    "gravedad_cero", "dispersion", "incertidumbre_medida", 
    "incertidumbre_sistematica", "incertidumbre_total", "sets_observados",
    "sets_procesados", "drops_por_set", "altura_de_montaje", "altura_de_observacion",
    "altura_de_procesado",    
    )   
  )

  gravimetros = serializers.serialize('json', Gravimetro.objects.all())

  ptosObs = serializers.serialize('json', PuntoObs.objects.all())


  ptosObs2 = ptosObs.replace('"geom":', '"geometry": {"type": ').replace('"SRID=4326;POINT (', '"Point", "coordinates": [').replace(')"', ']}'). replace(")", "]").replace("(", "[").replace("5 ", '5, ').replace("1 ", '1, ').replace("0 ", '0, ').replace("2 ", '2, ').replace("3 ", '3, ').replace("4 ", '4, ').replace("7 ", '7, ').replace("6 ", '6, ').replace("7 ", '7, ').replace("8 ", '8, ').replace("9 ", '9, ').replace("fields", "properties")

  data = data.replace('"geom":', '"geometry": {"type": ').replace('"SRID=4326;MULTIPOINT ((', '"MultiPoint", "coordinates": [[').replace('))"', ']]}'). replace(")", "]").replace("(", "[").replace("5 ", '5, ').replace("1 ", '1, ').replace("0 ", '0, ').replace("2 ", '2, ').replace("3 ", '3, ').replace("4 ", '4, ').replace("7 ", '7, ').replace("6 ", '6, ').replace("7 ", '7, ').replace("8 ", '8, ').replace("9 ", '9, ').replace("fields", "properties")

  data = { "estaciones": data, "observaciones": obs, "gravimetro": gravimetros, "ptos" : ptosObs, "ptos2": ptosObs2}
  
  return render(request, 'index.html',  data)

def info(request):
  template = loader.get_template('info.html')
  obs = serializers.serialize('json', Observacion.objects.all())
  # parse x:
  ficheros_sets = []
  y = json.loads(obs)
  # print(y[0])
  for x in y:
    if x["fields"]["fichero_set"] not in ficheros_sets:
      ficheros_sets.append(x["fields"]["fichero_set"])
  
  sets = []
  
  for li in ficheros_sets:
    set_data = {
      "file": li,
      "datos": []
    }
    
    path = "C:\\ignGrav\\igngrav\\media\\"
    
    path_complete = path + li.replace("/", "\\")
    # print(path_complete)
    datos = []
    if ".txt" in path_complete:
      archivo = open(path_complete)
      lineas = archivo.readlines()
      for linea in lineas:
        # print(len(linea.split()))
        if len(linea.split()) > 4:
          if 'Set' not in linea.split(): 
            num_sets = linea.split()[1].split(':')
            num_set = "{}".format(linea.split()[0])
            date = "{}:{}".format(num_sets[0], num_sets[1])
            num_gravedad = float(linea.split()[4])
            num_incertidumbre = float(linea.split()[5]) + float(linea.split()[7]) + float(linea.split()[6])
            num_temperatura = float(linea.split()[17])
            num_presion = float(linea.split()[18])
            num_marea = float(linea.split()[8])
            num_carga = float(linea.split()[9])


            collection = {
              "sets": num_set,
              "gravedad": num_gravedad,
              "gravedad_tool": num_gravedad,
              "incertidumbre": num_incertidumbre,
              "temperatura" : num_temperatura,
              "presion":  num_presion,
              "mareaT": num_marea,
              "cargaO": num_carga,
            }
            set_data["datos"].append(collection)
      
      sets.append(set_data) 
      archivo.close()
  
  # print(sets) 

  data = {"fichero_sets": sets}
  return render(request, 'info.html',  data)
