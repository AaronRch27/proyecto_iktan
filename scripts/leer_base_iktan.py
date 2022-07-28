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

#comienzo del tratamiento a los datos del df
valores = [f'Aclaración de información (Revisión ROCE) ({x})' for x in range(1,10)]
ndf = df[df.Estatus.isin(valores)] #nuevo frame filtrado con la variable de interes Estatus
ndf['num_rev'] = ndf.apply(lambda fila: fila.Estatus[-2],axis=1)
ndf['contador'] = [1 for i in range(ndf.shape[0])]    
mas_solicitudes = ndf.groupby(by=['Folio']).sum()
filtro = mas_solicitudes['contador'] > 3
ms = mas_solicitudes[filtro]
indexms = list(ms.index)
ncon = list(ms['contador'])
respuesta = {'Folio':indexms,
             'Entidad':[],
             'Usuario':[],
             'Perfil':[],
             'Numero_consultas':ncon}
#llenar dataframe de respuesta
for folio in indexms:
    #iterr en fils de dataframe
    c = 0
    for fila in df['Folio']:
        if fila == folio:
            respuesta['Entidad'].append(df['Entidad'][c])
            respuesta['Usuario'].append(df['Usuario'][c])
            respuesta['Perfil'].append(df['Perfil'][c])
            break
        c += 1

#generar archivo de respuesta con quienes han hecho más solucitudes(arriba de 3)
rt = pd.DataFrame(respuesta)
rt.to_csv('Mas_revisiones.csv',index=False,encoding='latin1')