# -*- coding: utf-8 -*-
"""

Guillermo Martínez
Proyecto Fortalecimiento Acueductos Rurales

Objetivo:
    Procesar informacion numberos prediales para análisis
Requiere:
    Archivos shape con número predial de 30 dígitos
    Ver  Documento IGAC I51500-06/17.V1
"""

import geopandas as gpd
import numpy as np

# Lista shapefiles
shps = [r'../GIS/shp/ACC/25245_Terreno.shp',r'../GIS/shp/ACC/25878_Terreno.shp']

# Columna con codigo catastral de 30 digitos (SNC)
codigo = 'codigo' 

columns=['DEPTO', 'MPIO', 'ZONA', 'SECTOR', 'COMUNA', 'BARRIO', 'MANZVER', 'TERRENO', 'CONDCN', 'EDIFCIO', 'PISO', 'UNIDAD']
lencol=np.array([2,	3,	2,	2,	2,	2,	4,	4,	1,	2,	2,	4])


for shp in shps:
    print(shp)    
    gdf = gpd.read_file(shp)
    startc = 0
    for icol, col in enumerate(columns):        
        gdf[col]=gdf[codigo].str[startc:startc+lencol[icol]]
        startc=startc+lencol[icol]
    gdf.to_file(shp.replace('.shp', '_SNC.shp'))


