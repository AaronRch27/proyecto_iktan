# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:35:44 2022

@author: AARON.RAMIREZ
"""

import pandas as pd

#leer archivo descargado de iktan

documento = pd.read_excel('xIktan_20220727034229952_reporteSegumiento.xlsx')

#formar nuevo dataframe
rep = documento.fillna('vacio') #llenar espacios vacios con la palabra 'vacio'

c_nomb = list(rep.iloc[7,:]) #conseguir fila donde están los encabezados de la tabla 
c_nomb = [c for c in c_nomb if c != 'vacio'] #eliminar vacios en fila de encabezados de tabla

#armar columnas de la tabla
frame = {}
lista_col = [2,3,5,6,8,10,12,14] #index de filas obtenidos viendo el excel en donde hay datos
c = 0
for col in lista_col:
    frame[c_nomb[c]] = list(rep.iloc[8:,col])
    c += 1
df = pd.DataFrame(frame)

    
