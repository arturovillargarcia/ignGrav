from datetime import datetime, timedelta


# ruta en la que se almacenan las imágenes para la reseña
def ruta_imagenes(self, filename):
    return f"FOTOS/{self.estacion}/{self.id_punto_obs}/{filename}"

# ruta en la que se almacenan los ficheros g
def ruta_ficheros_g(self, filename):
    return f"FICHEROS/{self.estacion}/{self.punto_obs}/{filename}"

# ruta en la que se almacenan los manuales de los gravímetros
def ruta_manuales(self, filename):
    return f"MANUALES/{self.get_modelo_display()}#{self.numero_serie}/{filename}"

# ruta en la que se almacenan los ficheros de mantenimiento
def ruta_mantenimiento(self, filename):
    return f"MANTENIMIENTO/{self.gravimetro}/{filename}"

# extracción de los datos alojados en el fichero project
def extracción_fichero_project(fichero_project_path):
    if fichero_project_path.name.split(".")[1][:7] == "project":
        indices = [
            2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 4, 4, 3
        ]

        palabras = [
            "Created", "Setup", "Transfer", "Actual", "Gradient", "Type",
            "S/N", "Rubidium", "Gravity", "Set", "Measurement", "Total", 
            "Collected", "Processed", "Drops"
        ]

        atributos = [
            "fecha_procesado", "altura_de_montaje", "altura_de_procesado", 
            "altura_de_observacion", "gradiente_vertical", "modelo",
            "numero_serie", "frecuencia_reloj", "gravedad_procesada", "dispersion", "incertidumbre_medida",
            "incertidumbre_total", "sets_observados", "sets_procesados", "drops_por_set"
        ]

        valores = {}

        fichero = fichero_project_path.open("r")

        mi_iterador = fichero.__iter__()

        linea = ""
        for i in range(len(indices)):
            while not palabras[i] in linea:
                linea = next(mi_iterador)
            valores[atributos[i]] = linea.split()[indices[i]]

        fichero.close()

        fichero = fichero_project_path.open("r")

        if valores["modelo"] == "A10":
            for linea in fichero:
                if "Blue Lock" in linea:
                    valores["laser_blue_wlength"] = linea.split()[2]
                if "Red Lock" in linea:
                    valores["laser_red_wlength"] = linea.split()[2]
        elif valores["modelo"] == "FG5":
            for linea in fichero:
                if "ID:" in linea:
                    valores["laser_dpeak_wlength"] = linea.split()[1]
                    valores["laser_dpeak_volt"] = linea.split()[4]
                if "IE:" in linea:
                    valores["laser_epeak_wlength"] = linea.split()[1]
                    valores["laser_epeak_volt"] = linea.split()[4]
                if "IF:" in linea:
                    valores["laser_fpeak_wlength"] = linea.split()[1]
                    valores["laser_fpeak_volt"] = linea.split()[4]
                if "IG:" in linea:
                    valores["laser_gpeak_wlength"] = linea.split()[1]
                    valores["laser_gpeak_volt"] = linea.split()[4]
                if "IH:" in linea:
                    valores["laser_hpeak_wlength"] = linea.split()[1]
                    valores["laser_hpeak_volt"] = linea.split()[4]
                if "II:" in linea:
                    valores["laser_ipeak_wlength"] = linea.split()[1]
                    valores["laser_ipeak_volt"] = linea.split()[4]
                if "IJ:" in linea:
                    valores["laser_jpeak_wlength"] = linea.split()[1]
                    valores["laser_jpeak_volt"] = linea.split()[4]
        else:
            pass

        fichero.close()

        fichero = fichero_project_path.open("r")

        flag = False

        observaciones_medida = ""

        for linea in fichero:
            if flag == True:
                observaciones_medida += linea
            if "Comments" in linea:
                flag = True

        if len(observaciones_medida) > 0:
            valores["observaciones_medida"] = observaciones_medida
            
        fichero.close()

        return(valores)
    else:
        pass

# extracción de los datos alojados en el fichero project
def extracción_fichero_set(fichero_set_path):
    if fichero_set_path.name.split(".")[1][:7] == "set":
        fichero = fichero_set_path.open("r")

        datos_set = {
            "set": [], "fecha_observacion": [], "gravedad": [], "dispersion": [],
            "marea_terrestre": [], "carga_oceanica": [], "corr_presion": [],
            "mov_polo": [], "temperatura": [], "presion": []
        }

        contador = 0
        for linea in fichero:
            contador += 1
            if contador > 4:                
                anno = int(linea.split()[3])
                doy = int(linea.split()[2])
                hora = int(linea.split()[1].split(":")[0])
                minuto = int(linea.split()[1].split(":")[1])
                segundo = int(linea.split()[1].split(":")[2])
                fecha_observacion = datetime(
                    year=anno, month=1, day=1, hour=hora, minute=minuto, second=segundo
                ) + timedelta(days=doy - 1)
                datos_set["set"].append(int(linea.split()[0]))
                datos_set["fecha_observacion"].append(fecha_observacion)
                datos_set["gravedad"].append(float(linea.split()[4]))
                datos_set["dispersion"].append(float(linea.split()[5]))
                datos_set["marea_terrestre"].append(float(linea.split()[8]))
                datos_set["carga_oceanica"].append(float(linea.split()[9]))
                datos_set["corr_presion"].append(float(linea.split()[10]))
                datos_set["mov_polo"].append(float(linea.split()[11]))
                datos_set["temperatura"].append(float(linea.split()[17]))
                datos_set["presion"].append(float(linea.split()[18]))
            else:
                pass

        fichero.close()

        return datos_set


# extracción de la fecha de observación desde el fichero drop
def extraccion_fecha_observacion(fichero_drop_path):
    if fichero_drop_path.name.split(".")[1][:7] == "drop":
        fichero = fichero_drop_path.open("r")
        
        for linea in fichero:
            if linea.split()[1] == "1":
                doy = int(linea.split()[3])
                anno = int(linea.split()[4])
                fecha_observacion = datetime(year=anno, month=1, day=1) + timedelta(days=doy - 1)
                return fecha_observacion
    else:
        pass

# extracción de datos de varias observaciones
def extraccion_datos_observaciones(observaciones):
    datos_observaciones = {
        "fecha_observacion": [], "gravedad_procesada": [], "gravedad_cero": [],
        "dispersion": [], "incertidumbre_medida": [], "incertidumbre_sistematica": [],
        "incertidumbre_total": [], "altura_de_observacion": [], "publicable": []
    }
    for observacion in observaciones:
        datos_observaciones["fecha_observacion"].append(observacion.fecha_observacion)
        datos_observaciones["gravedad_procesada"].append(observacion.gravedad_procesada)
        datos_observaciones["gravedad_cero"].append(observacion.gravedad_cero)
        datos_observaciones["dispersion"].append(observacion.dispersion)
        datos_observaciones["incertidumbre_medida"].append(observacion.incertidumbre_medida)
        datos_observaciones["incertidumbre_sistematica"].append(observacion.incertidumbre_sistematica)
        datos_observaciones["incertidumbre_total"].append(observacion.incertidumbre_total)
        datos_observaciones["altura_de_observacion"].append(observacion.altura_de_observacion)
        datos_observaciones["publicable"].append(observacion.publicable)

    # print(datos_observaciones)
    return datos_observaciones
