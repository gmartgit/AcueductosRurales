# -*- coding: utf-8 -*-
"""
Guillermo Martínez
Proyecto Fortalecimiento Acueductos Rurales

Objetivo:
    Extraer Informacion SIASAR en archivos shapefile y csv
Requiere:
    Folder con archivos de excel de SIASAR (http://data.globalsiasar.org/download-excels)
    Archivo shapefile con polígono del area de estudio
"""

import geopandas as gpd
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Localización de archivos
directorio_SIASAR = r'../data/Acueductos/SIASAR'
archivo_shp = r'../GIS/shp/DANE/MGN_MPIO_POLITICO_AOI.shp'

# Riect
dir_resultados = '../Resultados/SIASAR'
if not os.path.exists(dir_resultados):
    os.makedirs(dir_resultados)

# importar archivo shp con area de estudio en un geodataframe
gae = gpd.read_file(archivo_shp)

# reprojetar a WGS84 (EPSG: 4326)
gae = gae.to_crs("EPSG:4326")

print(os.getcwd())
#os.chdir(directorio_SIASAR)
puntos_en_SIASAR = []
nombres_SIASAR = []
for pathfile in glob.glob(os.path.join(directorio_SIASAR,"*.xls")):
    print(pathfile)
    file=os.path.basename(pathfile)
    df = pd.read_excel(pathfile)
    # revisar si el archivo tiene longitud y latitud
    if ('latitud' in df.columns) & ('longitud' in df.columns):
        print(f'Archivo {file} tiene coordenadas')
        df['geometry'] = df.apply(lambda x: Point((float(x.longitud), float(x.latitud))), axis=1)
        puntos_gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:4326')

        puntos_en_ae = gpd.sjoin(puntos_gdf, gae, op='within')

        print(f'{file} contiene {len(puntos_en_ae)}')

        if len(puntos_en_ae) > 0:
            # crear shapefile, cambiar el formato de fecha
            # TODO mejorar forma de truncar columnas dado el limite de shp. salver en gdb o gpkg?
            schema = gpd.io.file.infer_schema(puntos_en_ae)
            lista_datetime = []
            for key in schema['properties'].keys():
                if schema['properties'][key] == 'datetime':
                    lista_datetime.append(key)
            print(lista_datetime)
            for col in lista_datetime:
                puntos_en_ae[col] = puntos_en_ae[col].dt.strftime('%Y-%m-%d')  #
            print('')
            puntos_en_ae.to_file(os.path.join(dir_resultados, f'{file[:-4]}_ae.shp'))
            puntos_en_ae.drop('geometry',axis=1).to_csv(os.path.join(dir_resultados, f'{file[:-4]}_ae.csv'))

            puntos_en_SIASAR.append(puntos_en_ae)
            nombres_SIASAR.append(f'{file[:-4]} [{str(len(puntos_en_ae))}]')

# Cargar informacion seleccionada
fig, ax = plt.subplots(figsize=(15, 15))
gae.plot(ax=ax, label='Area de Estudio',color="white", edgecolor='black')
for gdf, nombre in zip(puntos_en_SIASAR, nombres_SIASAR):
    gdf.plot(ax=ax, label=nombre)

plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.tight_layout()

plt.show()
plt.savefig(os.path.join(dir_resultados,'Puntos_SIASAR_en_AE.png'), bbox_inches='tight')


