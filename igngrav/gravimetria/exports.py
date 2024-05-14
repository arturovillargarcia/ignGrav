import csv
import io
import xlsxwriter
from django.contrib.gis import admin
from django.http import HttpResponse
from gravimetria.models import Estacion, PuntoObs, Observacion


@admin.action(description="Exportar elementos seleccionados en formato csv")
def exportar_csv(modeladmin, request, queryset):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="Observaciones.csv"'},
    )

    writer = csv.writer(response)

    writer.writerow([
        "ID estación", "Nombre de la estación", "Punto de observación", "Nombre del punto",
        "Red primaria", "Redes secundarias", "Tipo de observación", "Fecha de observación", 
        "Fecha de procesado", "Gravímetro", "Gravedad observada [μGal]", "Altura de observación [cm]", 
        "Altura de montaje [cm]", "Gravedad a 0 cm [μGal]", "Gravedad procesada [μGal]",
        "Altura de procesado [cm]", "Dispersión entre sets [μGal]", "Incertidumbre de la observación [μGal]", 
        "Incertidumbre sistemática [μGal]", "Incertidumbre total [μGal]", "Número de sets observados", 
        "Número de sets procesados", "Número de caídas por set", "Tipo de gradiente",   
        "Gradiente [μGal]", "Incertidumbre del gradiente [μGal]", "Gravímetro del gradiente", 
        "Comunidad autónoma", "Provincia", "Isla", "Municipio", "Tipo de señalización", 
        "Estado de la señal", "Fecha de revisión", "Tipo de acceso", "Latitud [º]", "Longitud [º]", 
        "Altitud ortométrica [m]", "UTM X [m]", "UTM Y [m]", "Zona UTM", "Frecuencia del reloj [Hz]", 
        "λ azul [nm]", "λ rojo [nm]", "λ pico D [nm]", "λ pico E [nm]",
        "λ pico F [nm]", "λ pico G [nm]", "λ pico H [nm]", "λ pico I [nm]", "λ pico J [nm]",
        "Voltaje pico D [V]", "Voltaje pico E [V]", "Voltaje pico F [V]", "Voltaje pico G [V]",
        "Voltaje pico H [V]", "Voltaje pico I [V]", "Voltaje pico J [V]"
    ])

    if queryset.model is Estacion:
        observaciones = [observacion for estacion in queryset for observacion in estacion.observacion_set.all()]
    elif queryset.model is PuntoObs:
        observaciones = [observacion for punto_obs in queryset for observacion in punto_obs.observacion_set.all()]
    elif queryset.model is Observacion:
        observaciones = queryset
    else:
        return None
    
    for observacion in observaciones:
        redes_secundarias = '_'.join(red.nombre for red in observacion.estacion.red_secundaria.all())
        if observacion.gravimetro_observacion.tipo_gravimetro == 1:
            tipo_observacion = "Absoluta"
        else:
            tipo_observacion = "Relativa"
        writer.writerow([
            observacion.estacion, observacion.estacion.nombre, observacion.punto_obs,
            observacion.punto_obs.nombre, observacion.estacion.red_primaria, redes_secundarias, 
            tipo_observacion, observacion.fecha_observacion, observacion.fecha_procesado,
            observacion.gravimetro_observacion, observacion.gravedad_observada, observacion.altura_de_observacion,
            observacion.altura_de_montaje, observacion.gravedad_cero, observacion.gravedad_procesada,
            observacion.altura_de_procesado, observacion.dispersion, observacion.incertidumbre_medida,
            observacion.incertidumbre_sistematica, observacion.incertidumbre_total, observacion.sets_observados,
            observacion.sets_procesados, observacion.drops_por_set, observacion.get_tipo_gradiente_display(),
            observacion.gradiente_vertical, observacion.incertidumbre_gradiente, observacion.gravimetro_gradiente,
            observacion.estacion.com_autonoma, observacion.estacion.provincia, observacion.estacion.isla,
            observacion.estacion.municipio, observacion.punto_obs.get_tipo_senal_display(),
            observacion.punto_obs.get_estado_senal_display(), observacion.punto_obs.fecha_revision,
            observacion.punto_obs.get_tipo_acceso_display(), observacion.punto_obs.latitud, observacion.punto_obs.longitud,
            observacion.punto_obs.altitud, observacion.punto_obs.utm_x, observacion.punto_obs.utm_y,
            observacion.punto_obs.utm_zona, observacion.frecuencia_reloj, observacion.laser_blue_wlength,
            observacion.laser_red_wlength, observacion.laser_dpeak_wlength, observacion.laser_epeak_wlength,
            observacion.laser_fpeak_wlength, observacion.laser_gpeak_wlength, observacion.laser_hpeak_wlength,
            observacion.laser_ipeak_wlength, observacion.laser_jpeak_wlength, observacion.laser_dpeak_volt,
            observacion.laser_epeak_volt, observacion.laser_fpeak_volt, observacion.laser_gpeak_volt,
            observacion.laser_hpeak_volt, observacion.laser_ipeak_volt, observacion.laser_jpeak_volt      
        ])

    return response


@admin.action(description="Exportar elementos seleccionados en formato xlsx")
def exportar_xlsx(modeladmin, request, queryset):
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0
    cabecera = (
    "ID estación", "Nombre de la estación", "Punto de observación", "Nombre del punto",
    "Red primaria", "Redes secundarias", "Tipo de observación", "Fecha de observación", 
    "Fecha de procesado", "Gravímetro", "Gravedad observada [μGal]", "Altura de observación [cm]", 
    "Altura de montaje [cm]", "Gravedad a 0 cm [μGal]", "Gravedad procesada [μGal]",
    "Altura de procesado [cm]", "Dispersión entre sets [μGal]", "Incertidumbre de la observación [μGal]", 
    "Incertidumbre sistemática [μGal]", "Incertidumbre total [μGal]", "Número de sets observados", 
    "Número de sets procesados", "Número de caídas por set", "Tipo de gradiente",   
    "Gradiente [μGal]", "Incertidumbre del gradiente [μGal]", "Gravímetro del gradiente", 
    "Comunidad autónoma", "Provincia", "Isla", "Municipio", "Tipo de señalización", 
    "Estado de la señal", "Fecha de revisión", "Tipo de acceso", "Latitud [º]", "Longitud [º]", 
    "Altitud ortométrica [m]", "UTM X [m]", "UTM Y [m]", "Zona UTM", "Frecuencia del reloj [Hz]", 
    "λ azul [nm]", "λ rojo [nm]", "λ pico D [nm]", "λ pico E [nm]",
    "λ pico F [nm]", "λ pico G [nm]", "λ pico H [nm]", "λ pico I [nm]", "λ pico J [nm]",
    "Voltaje pico D [V]", "Voltaje pico E [V]", "Voltaje pico F [V]", "Voltaje pico G [V]",
    "Voltaje pico H [V]", "Voltaje pico I [V]", "Voltaje pico J [V]"
    )
    scale_factor = 1.4
    widths = {}
    for campo in cabecera:
        cell_format = workbook.add_format({"bold": True, "align": "center", "font_name": "Arial"})
        cell_format.set_border(1)
        widths[col] = len(str(campo))
        worksheet.set_column(col, col, widths[col] * scale_factor)
        worksheet.write_string(row, col, campo, cell_format)
        col += 1

    if queryset.model is Estacion:
        observaciones = [observacion for estacion in queryset for observacion in estacion.observacion_set.all()]
    elif queryset.model is PuntoObs:
        observaciones = [observacion for punto_obs in queryset for observacion in punto_obs.observacion_set.all()]
    elif queryset.model is Observacion:
        observaciones = queryset
    else:
        return None

    row = 1
    col = 0
    estacion = ""
    punto_obs = observaciones[0].punto_obs
    counter = 0
    for observacion in observaciones:
        counter += 1
        if str(observacion.estacion) == estacion and counter != len(observaciones):       
            if str(observacion.punto_obs) != str(punto_obs):              
                cell_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "font_name": "Arial", "align": "center"}
                )
                date_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "font_name": "Arial", "align": "center", "num_format": "dd/mm/yyyy"}
                )
                floating_point_0dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "font_name": "Arial", "align": "center", "num_format": "0"}
                )
                floating_point_2dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "font_name": "Arial", "align": "center", "num_format": "0.00"}
                )
                floating_point_3dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "font_name": "Arial", "align": "center", "num_format": "0.000"}
                )
                floating_point_5dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "font_name": "Arial", "align": "center", "num_format": "0.00000"}
                )
                floating_point_8dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "font_name": "Arial", "align": "center", "num_format": "0.00000000"}
                )                
                punto_obs = observacion.punto_obs
            else:
                cell_format = workbook.add_format(
                    {"left": 1, "right": 1, "font_name": "Arial", "align": "center"}
                )
                date_format = workbook.add_format(
                    {"left": 1, "right": 1, "font_name": "Arial", "align": "center", "num_format": "dd/mm/yyyy"}
                )
                floating_point_0dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "font_name": "Arial", "align": "center", "num_format": "0"}
                )
                floating_point_2dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "font_name": "Arial", "align": "center", "num_format": "0.00"}
                )
                floating_point_3dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "font_name": "Arial", "align": "center", "num_format": "0.000"}
                )
                floating_point_5dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000"}
                )
                floating_point_8dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000000"}
                )
        elif str(observacion.estacion) != estacion and counter != len(observaciones):                   
            cell_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "font_name": "Arial", "align": "center"}
            )
            date_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "font_name": "Arial", "align": "center", "num_format": "dd/mm/yyyy"}
            )
            floating_point_0dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "font_name": "Arial", "align": "center", "num_format": "0"}
            )
            floating_point_2dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "font_name": "Arial", "align": "center", "num_format": "0.00"}
            )
            floating_point_3dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "font_name": "Arial", "align": "center", "num_format": "0.000"}
            )
            floating_point_5dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000"}
            )
            floating_point_8dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000000"}
            )
            estacion = str(observacion.estacion)
            punto_obs = observacion.punto_obs
        elif str(observacion.estacion) != estacion and counter == len(observaciones):
            cell_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "bottom": 1, "font_name": "Arial", "align": "center"}
            )
            date_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "dd/mm/yyyy"}
            )
            floating_point_0dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0"}
            )
            floating_point_2dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00"}
            )
            floating_point_3dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.000"}
            )
            floating_point_5dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000"}
            )
            floating_point_8dec_format = workbook.add_format(
                {"left": 1, "right": 1, "top": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000000"}
            )
        elif str(observacion.estacion) == estacion and counter == len(observaciones):
            if str(observacion.punto_obs) != str(punto_obs):              
                cell_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "bottom": 1, "font_name": "Arial", "align": "center"}
                )
                date_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "dd/mm/yyyy"}
                )
                floating_point_0dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0"}
                )
                floating_point_2dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00"}
                )
                floating_point_3dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.000"}
                )
                floating_point_5dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000"}
                )
                floating_point_8dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "top": 3, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000000"}
                )
                punto_obs = observacion.punto_obs
            else:
                cell_format = workbook.add_format(
                    {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center"}
                )
                date_format = workbook.add_format(
                    {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "dd/mm/yyyy"}
                )
                floating_point_0dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0"}
                )
                floating_point_2dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00"}
                )
                floating_point_3dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.000"}
                )       
                floating_point_5dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000"}
                )
                floating_point_8dec_format = workbook.add_format(
                    {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000000"}
                )       
        else:
            cell_format = workbook.add_format(
                {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center"}
            )
            date_format = workbook.add_format(
                {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "dd/mm/yyyy"}
            )
            floating_point_0dec_format = workbook.add_format(
                {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0"}
            )
            floating_point_2dec_format = workbook.add_format(
                {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00"}
            )
            floating_point_3dec_format = workbook.add_format(
                {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.000"}
            )
            floating_point_5dec_format = workbook.add_format(
                {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000"}
            )
            floating_point_8dec_format = workbook.add_format(
                {"left": 1, "right": 1, "bottom": 1, "font_name": "Arial", "align": "center", "num_format": "0.00000000"}
            )
        if observacion.estacion:
            if len(str(observacion.estacion)) > widths[col]:
                widths[col] = len(str(observacion.estacion))
            worksheet.set_column(col, col, widths[col] * scale_factor)
            worksheet.write_string(row, col, str(observacion.estacion), cell_format)
        else:
            worksheet.write_blank(row, col, None, cell_format)

        if observacion.estacion.nombre:
            if len(str(observacion.estacion.nombre)) > widths[col + 1]:
                widths[col + 1] = len(str(observacion.estacion.nombre))
            worksheet.set_column(col + 1, col + 1, widths[col + 1] * scale_factor)            
            worksheet.write_string(row, col + 1, str(observacion.estacion.nombre), cell_format)
        else:
            worksheet.write_blank(row, col + 1, None, cell_format)

        if observacion.punto_obs:
            if len(str(observacion.punto_obs)) > widths[col + 2]:
                widths[col + 2] = len(str(observacion.punto_obs))
            worksheet.set_column(col + 2, col + 2, widths[col + 2] * scale_factor)                
            worksheet.write_string(row, col + 2, str(observacion.punto_obs), cell_format)
        else:
            worksheet.write_blank(row, col + 2, None, cell_format)

        if observacion.punto_obs.nombre:
            if len(str(observacion.punto_obs.nombre)) > widths[col + 3]:
                widths[col + 3] = len(str(observacion.punto_obs.nombre))
            worksheet.set_column(col + 3, col + 3, widths[col + 3] * scale_factor)
            worksheet.write_string(row, col + 3, str(observacion.punto_obs.nombre), cell_format)
        else:
            worksheet.write_blank(row, col + 3, None, cell_format)

        if observacion.estacion.red_primaria:
            if len(str(observacion.estacion.red_primaria)) > widths[col + 4]:
                widths[col + 4] = len(str(observacion.estacion.red_primaria))
            worksheet.set_column(col + 4, col + 4, widths[col + 4] * scale_factor)
            worksheet.write_string(row, col + 4, str(observacion.estacion.red_primaria), cell_format)
        else:
            worksheet.write_blank(row, col + 4, None, cell_format)

        if observacion.estacion.red_secundaria:
            redes_secundarias = ', '.join(red.nombre for red in observacion.estacion.red_secundaria.all())
            if len(str(redes_secundarias)) > widths[col + 5]:
                widths[col + 5] = len(str(redes_secundarias))
            worksheet.set_column(col + 5, col + 5, widths[col + 5] * scale_factor)
            worksheet.write_string(row, col + 5, str(redes_secundarias), cell_format)
        else:
            worksheet.write_blank(row, col + 5, None, cell_format)

        if observacion.gravimetro_observacion.tipo_gravimetro:
            if len(str(observacion.gravimetro_observacion.tipo_gravimetro)) > widths[col + 6]:
                widths[col + 6] = len(str(observacion.gravimetro_observacion.tipo_gravimetro))
            worksheet.set_column(col + 6, col + 6, widths[col + 6] * scale_factor)
            if observacion.gravimetro_observacion.tipo_gravimetro == 1:
                worksheet.write_string(row, col + 6, "Absoluta", cell_format)
            else:
                worksheet.write_string(row, col + 6, "Relativa", cell_format)
        else:
            worksheet.write_blank(row, col + 6, None, cell_format)

        if observacion.fecha_observacion:
            if len(str(observacion.fecha_observacion)) > widths[col + 7]:
                widths[col + 7] = len(str(observacion.fecha_observacion))
            worksheet.set_column(col + 7, col + 7, widths[col + 7] * scale_factor)            
            worksheet.write_datetime(row, col + 7, observacion.fecha_observacion, date_format)
        else:
            worksheet.write_blank(row, col + 7, None, cell_format)

        if observacion.fecha_procesado:
            if len(str(observacion.fecha_procesado)) > widths[col + 8]:
                widths[col + 8] = len(str(observacion.fecha_procesado))
            worksheet.set_column(col + 8, col + 8, widths[col + 8] * scale_factor)            
            worksheet.write_datetime(row, col + 8, observacion.fecha_procesado, date_format)
        else:
            worksheet.write_blank(row, col + 8, None, cell_format)

        if observacion.gravimetro_observacion:
            if len(str(observacion.gravimetro_observacion)) > widths[col + 9]:
                widths[col + 9] = len(str(observacion.gravimetro_observacion))
            worksheet.set_column(col + 9, col + 9, widths[col + 9] * scale_factor)
            worksheet.write_string(row, col + 9, str(observacion.gravimetro_observacion), cell_format)
        else:
            worksheet.write_blank(row, col + 9, None, cell_format)

        if observacion.gravedad_observada:
            if len(str(observacion.gravedad_observada)) > widths[col + 10]:
                widths[col + 10] = len(str(observacion.gravedad_observada))
            worksheet.set_column(col + 10, col + 10, widths[col + 10] * scale_factor)            
            worksheet.write_number(row, col + 10, float(observacion.gravedad_observada), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 10, None, cell_format)

        if observacion.altura_de_observacion:
            worksheet.write_number(row, col + 11, float(observacion.altura_de_observacion), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 11, None, cell_format)

        if observacion.altura_de_montaje:
            worksheet.write_number(row, col + 12, float(observacion.altura_de_montaje), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 12, None, cell_format)

        if observacion.gravedad_cero:
            if len(str(observacion.gravedad_cero)) > widths[col + 13]:
                widths[col + 13] = len(str(observacion.gravedad_cero))
            worksheet.set_column(col + 13, col + 13, widths[col + 13] * scale_factor)            
            worksheet.write_number(row, col + 13, float(observacion.gravedad_cero), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 13, None, cell_format)

        if observacion.gravedad_procesada:
            if len(str(observacion.gravedad_procesada)) > widths[col + 14]:
                widths[col + 14] = len(str(observacion.gravedad_procesada))
            worksheet.set_column(col + 14, col + 14, widths[col + 14] * scale_factor)            
            worksheet.write_number(row, col + 14, float(observacion.gravedad_procesada), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 14, None, cell_format)

        if observacion.altura_de_procesado:
            worksheet.write_number(row, col + 15, float(observacion.altura_de_procesado), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 15, None, cell_format)

        if observacion.dispersion:
            worksheet.write_number(row, col + 16, float(observacion.dispersion), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 16, None, cell_format)

        if observacion.incertidumbre_medida:
            worksheet.write_number(row, col + 17, float(observacion.incertidumbre_medida), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 17, None, cell_format)

        if observacion.incertidumbre_sistematica:
            worksheet.write_number(row, col + 18, float(observacion.incertidumbre_sistematica), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 18, None, cell_format)

        if observacion.incertidumbre_total:
            worksheet.write_number(row, col + 19, float(observacion.incertidumbre_total), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 19, None, cell_format)

        if observacion.sets_observados:
            worksheet.write_number(row, col + 20, int(observacion.sets_observados), cell_format)
        else:
            worksheet.write_blank(row, col + 20, None, cell_format)

        if observacion.sets_procesados:
            worksheet.write_number(row, col + 21, int(observacion.sets_procesados), cell_format)
        else:
            worksheet.write_blank(row, col + 21, None, cell_format)

        if observacion.drops_por_set:
            worksheet.write_number(row, col + 22, int(observacion.drops_por_set), cell_format)
        else:
            worksheet.write_blank(row, col + 22, None, cell_format)

        if observacion.tipo_gradiente:
            if len(str(observacion.get_tipo_gradiente_display())) > widths[col + 23]:
                widths[col + 23] = len(str(observacion.get_tipo_gradiente_display()))
            worksheet.set_column(col + 23, col + 23, widths[col + 23] * scale_factor)
            worksheet.write_string(row, col + 23, str(observacion.get_tipo_gradiente_display()), cell_format)
        else:
            worksheet.write_blank(row, col + 23, None, cell_format)

        if observacion.gradiente_vertical:
            worksheet.write_number(row, col + 24, float(observacion.gradiente_vertical), floating_point_3dec_format)
        else:
            worksheet.write_blank(row, col + 24, None, cell_format)

        if observacion.incertidumbre_gradiente:
            worksheet.write_number(row, col + 25, float(observacion.incertidumbre_gradiente), floating_point_3dec_format)
        else:
            worksheet.write_blank(row, col + 25, None, cell_format)

        if observacion.gravimetro_gradiente:
            worksheet.write_string(row, col + 26, str(observacion.gravimetro_gradiente), cell_format)
        else:
            worksheet.write_blank(row, col + 26, None, cell_format)

        if observacion.estacion.com_autonoma:
            if len(str(observacion.estacion.com_autonoma)) > widths[col + 27]:
                widths[col + 27] = len(str(observacion.estacion.com_autonoma))
            worksheet.set_column(col + 27, col + 27, widths[col + 27] * scale_factor)  
            worksheet.write_string(row, col + 27, str(observacion.estacion.com_autonoma), cell_format)
        else:
            worksheet.write_blank(row, col + 27, None, cell_format)

        if observacion.estacion.provincia:
            if len(str(observacion.estacion.provincia)) > widths[col + 28]:
                widths[col + 28] = len(str(observacion.estacion.provincia))
            worksheet.set_column(col + 28, col + 28, widths[col + 28] * scale_factor)              
            worksheet.write_string(row, col + 28, str(observacion.estacion.provincia), cell_format)
        else:
            worksheet.write_blank(row, col + 28, None, cell_format)

        if observacion.estacion.isla:
            if len(str(observacion.estacion.isla)) > widths[col + 29]:
                widths[col + 29] = len(str(observacion.estacion.isla))
            worksheet.set_column(col + 29, col + 29, widths[col + 29] * scale_factor) 
            worksheet.write_string(row, col + 29, str(observacion.estacion.isla), cell_format)
        else:
            worksheet.write_blank(row, col + 29, None, cell_format)

        if observacion.estacion.municipio:
            if len(str(observacion.estacion.municipio)) > widths[col + 30]:
                widths[col + 30] = len(str(observacion.estacion.municipio))
            worksheet.set_column(col + 30, col + 30, widths[col + 30] * scale_factor) 
            worksheet.write_string(row, col + 30, str(observacion.estacion.municipio), cell_format)
        else:
            worksheet.write_blank(row, col + 30, None, cell_format)

        if observacion.punto_obs.tipo_senal:
            if len(str(observacion.punto_obs.get_tipo_senal_display())) > widths[col + 31]:
                widths[col + 31] = len(str(observacion.punto_obs.get_tipo_senal_display()))
            worksheet.set_column(col + 31, col + 31, widths[col + 31] * scale_factor) 
            worksheet.write_string(row, col + 31, str(observacion.punto_obs.get_tipo_senal_display()), cell_format)
        else:
            worksheet.write_blank(row, col + 31, None, cell_format)

        if observacion.punto_obs.estado_senal:
            if len(str(observacion.punto_obs.get_estado_senal_display())) > widths[col + 32]:
                widths[col + 32] = len(str(observacion.punto_obs.get_estado_senal_display()))
            worksheet.set_column(col + 32, col + 32, widths[col + 32] * scale_factor) 
            worksheet.write_string(row, col + 32, str(observacion.punto_obs.get_estado_senal_display()), cell_format)
        else:
            worksheet.write_blank(row, col + 32, None, cell_format)

        if observacion.punto_obs.fecha_revision:
            if len(str(observacion.punto_obs.fecha_revision)) > widths[col + 33]:
                widths[col + 33] = len(str(observacion.punto_obs.fecha_revision))
            worksheet.set_column(col + 33, col + 33, widths[col + 33] * scale_factor)            
            worksheet.write_datetime(row, col + 33, observacion.punto_obs.fecha_revision, date_format)
        else:
            worksheet.write_blank(row, col + 33, None, cell_format)

        if observacion.punto_obs.tipo_acceso:
            if len(str(observacion.punto_obs.get_tipo_acceso_display())) > widths[col + 34]:
                widths[col + 34] = len(str(observacion.punto_obs.get_tipo_acceso_display()))
            worksheet.set_column(col + 34, col + 34, widths[col + 34] * scale_factor) 
            worksheet.write_string(row, col + 34, str(observacion.punto_obs.get_tipo_acceso_display()), cell_format)
        else:
            worksheet.write_blank(row, col + 34, None, cell_format)

        if observacion.punto_obs.latitud:
            if len(str(observacion.punto_obs.latitud)) > widths[col + 35]:
                widths[col + 35] = len(str(observacion.punto_obs.latitud))
            worksheet.set_column(col + 35, col + 35, widths[col + 35] * scale_factor) 
            worksheet.write_number(row, col + 35, float(observacion.punto_obs.latitud), cell_format)
        else:
            worksheet.write_blank(row, col + 35, None, cell_format)

        if observacion.punto_obs.longitud:
            if len(str(observacion.punto_obs.longitud)) > widths[col + 36]:
                widths[col + 36] = len(str(observacion.punto_obs.longitud))
            worksheet.set_column(col + 36, col + 36, widths[col + 36] * scale_factor) 
            worksheet.write_number(row, col + 36, float(observacion.punto_obs.longitud), cell_format)
        else:
            worksheet.write_blank(row, col + 36, None, cell_format)

        if observacion.punto_obs.altitud:
            worksheet.write_number(row, col + 37, float(observacion.punto_obs.altitud), floating_point_3dec_format)
        else:
            worksheet.write_blank(row, col + 37, None, cell_format)

        if observacion.punto_obs.utm_x:
            if len(str(observacion.punto_obs.utm_x)) > widths[col + 38]:
                widths[col + 38] = len(str(observacion.punto_obs.utm_x))
            worksheet.set_column(col + 38, col + 38, widths[col + 38] * scale_factor) 
            worksheet.write_number(row, col + 38, float(observacion.punto_obs.utm_x), floating_point_3dec_format)
        else:
            worksheet.write_blank(row, col + 38, None, cell_format)

        if observacion.punto_obs.utm_y:
            if len(str(observacion.punto_obs.utm_y)) > widths[col + 39]:
                widths[col + 39] = len(str(observacion.punto_obs.utm_y))
            worksheet.set_column(col + 39, col + 39, widths[col + 39] * scale_factor) 
            worksheet.write_number(row, col + 39, float(observacion.punto_obs.utm_y), floating_point_3dec_format)
        else:
            worksheet.write_blank(row, col + 39, None, cell_format)

        if observacion.punto_obs.utm_zona:
            if len(str(observacion.punto_obs.utm_zona)) > widths[col + 40]:
                widths[col + 40] = len(str(observacion.punto_obs.utm_zona))
            worksheet.set_column(col + 40, col + 40, widths[col + 40] * scale_factor) 
            worksheet.write_string(row, col + 40, str(observacion.punto_obs.utm_zona), cell_format)
        else:
            worksheet.write_blank(row, col + 40, None, cell_format)

        if observacion.frecuencia_reloj:
            if len(str(observacion.frecuencia_reloj)) > widths[col + 41]:
                widths[col + 41] = len(str(observacion.frecuencia_reloj))
            worksheet.set_column(col + 41, col + 41, widths[col + 41] * scale_factor) 
            worksheet.write_number(row, col + 41, float(observacion.frecuencia_reloj), floating_point_5dec_format)
        else:
            worksheet.write_blank(row, col + 41, None, cell_format)

        if observacion.laser_blue_wlength:
            if len(str(observacion.laser_blue_wlength)) > widths[col + 42]:
                widths[col + 42] = len(str(observacion.laser_blue_wlength))
            worksheet.set_column(col + 42, col + 42, widths[col + 42] * scale_factor) 
            worksheet.write_number(row, col + 42, float(observacion.laser_blue_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 42, None, cell_format)

        if observacion.laser_red_wlength:
            if len(str(observacion.laser_red_wlength)) > widths[col + 43]:
                widths[col + 43] = len(str(observacion.laser_red_wlength))
            worksheet.set_column(col + 43, col + 43, widths[col + 43] * scale_factor) 
            worksheet.write_number(row, col + 43, float(observacion.laser_red_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 43, None, cell_format)

        if observacion.laser_dpeak_wlength:
            if len(str(observacion.laser_dpeak_wlength)) > widths[col + 44]:
                widths[col + 44] = len(str(observacion.laser_dpeak_wlength))
            worksheet.set_column(col + 44, col + 44, widths[col + 44] * scale_factor) 
            worksheet.write_number(row, col + 44, float(observacion.laser_dpeak_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 44, None, cell_format)

        if observacion.laser_epeak_wlength:
            if len(str(observacion.laser_epeak_wlength)) > widths[col + 45]:
                widths[col + 45] = len(str(observacion.laser_epeak_wlength))
            worksheet.set_column(col + 45, col + 45, widths[col + 45] * scale_factor) 
            worksheet.write_number(row, col + 45, float(observacion.laser_epeak_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 45, None, cell_format)

        if observacion.laser_fpeak_wlength:
            if len(str(observacion.laser_fpeak_wlength)) > widths[col + 46]:
                widths[col + 46] = len(str(observacion.laser_fpeak_wlength))
            worksheet.set_column(col + 46, col + 46, widths[col + 46] * scale_factor) 
            worksheet.write_number(row, col + 46, float(observacion.laser_fpeak_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 46, None, cell_format)

        if observacion.laser_gpeak_wlength:
            if len(str(observacion.laser_gpeak_wlength)) > widths[col + 47]:
                widths[col + 47] = len(str(observacion.laser_gpeak_wlength))
            worksheet.set_column(col + 47, col + 47, widths[col + 47] * scale_factor) 
            worksheet.write_number(row, col + 47, float(observacion.laser_gpeak_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 47, None, cell_format)

        if observacion.laser_hpeak_wlength:
            if len(str(observacion.laser_hpeak_wlength)) > widths[col + 48]:
                widths[col + 48] = len(str(observacion.laser_hpeak_wlength))
            worksheet.set_column(col + 48, col + 48, widths[col + 48] * scale_factor) 
            worksheet.write_number(row, col + 48, float(observacion.laser_hpeak_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 48, None, cell_format)

        if observacion.laser_ipeak_wlength:
            if len(str(observacion.laser_ipeak_wlength)) > widths[col + 49]:
                widths[col + 49] = len(str(observacion.laser_ipeak_wlength))
            worksheet.set_column(col + 49, col + 49, widths[col + 49] * scale_factor) 
            worksheet.write_number(row, col + 49, float(observacion.laser_ipeak_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 49, None, cell_format)

        if observacion.laser_jpeak_wlength:
            if len(str(observacion.laser_jpeak_wlength)) > widths[col + 50]:
                widths[col + 50] = len(str(observacion.laser_jpeak_wlength))
            worksheet.set_column(col + 50, col + 50, widths[col + 50] * scale_factor) 
            worksheet.write_number(row, col + 50, float(observacion.laser_jpeak_wlength), floating_point_8dec_format)
        else:
            worksheet.write_blank(row, col + 50, None, cell_format)

        if observacion.laser_dpeak_volt:
            if len(str(observacion.laser_dpeak_volt)) > widths[col + 51]:
                widths[col + 51] = len(str(observacion.laser_dpeak_volt))
            worksheet.set_column(col + 51, col + 51, widths[col + 51] * scale_factor) 
            worksheet.write_number(row, col + 51, float(observacion.laser_dpeak_volt), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 51, None, cell_format)

        if observacion.laser_epeak_volt:
            if len(str(observacion.laser_epeak_volt)) > widths[col + 52]:
                widths[col + 52] = len(str(observacion.laser_epeak_volt))
            worksheet.set_column(col + 52, col + 52, widths[col + 52] * scale_factor) 
            worksheet.write_number(row, col + 52, float(observacion.laser_epeak_volt), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 52, None, cell_format)

        if observacion.laser_fpeak_volt:
            if len(str(observacion.laser_fpeak_volt)) > widths[col + 53]:
                widths[col + 53] = len(str(observacion.laser_fpeak_volt))
            worksheet.set_column(col + 53, col + 53, widths[col + 53] * scale_factor) 
            worksheet.write_number(row, col + 53, float(observacion.laser_fpeak_volt), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 53, None, cell_format)

        if observacion.laser_gpeak_volt:
            if len(str(observacion.laser_gpeak_volt)) > widths[col + 54]:
                widths[col + 54] = len(str(observacion.laser_gpeak_volt))
            worksheet.set_column(col + 54, col + 54, widths[col + 54] * scale_factor) 
            worksheet.write_number(row, col + 54, float(observacion.laser_gpeak_volt), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 54, None, cell_format)

        if observacion.laser_hpeak_volt:
            if len(str(observacion.laser_hpeak_volt)) > widths[col + 55]:
                widths[col + 55] = len(str(observacion.laser_hpeak_volt))
            worksheet.set_column(col + 55, col + 55, widths[col + 55] * scale_factor) 
            worksheet.write_number(row, col + 55, float(observacion.laser_hpeak_volt), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 55, None, cell_format)

        if observacion.laser_ipeak_volt:
            if len(str(observacion.laser_ipeak_volt)) > widths[col + 56]:
                widths[col + 56] = len(str(observacion.laser_ipeak_volt))
            worksheet.set_column(col + 56, col + 56, widths[col + 56] * scale_factor) 
            worksheet.write_number(row, col + 56, float(observacion.laser_ipeak_volt), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 56, None, cell_format)

        if observacion.laser_jpeak_volt:
            if len(str(observacion.laser_jpeak_volt)) > widths[col + 57]:
                widths[col + 57] = len(str(observacion.laser_jpeak_volt))
            worksheet.set_column(col + 57, col + 57, widths[col + 57] * scale_factor) 
            worksheet.write_number(row, col + 57, float(observacion.laser_jpeak_volt), floating_point_2dec_format)
        else:
            worksheet.write_blank(row, col + 57, None, cell_format)
        
        row += 1

    workbook.close()

    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="Observaciones.xlsx"'},
    )

    return response
