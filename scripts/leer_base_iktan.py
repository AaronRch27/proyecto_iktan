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
ndf1 = df[df.Estatus.isin(valores)] #nuevo frame filtrado con la variable de interes Estatus
ndf = ndf1.copy()
# ndf['num_rev'] = ndf.apply(lambda fila: fila.Estatus[-2],axis=1)
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
rt.to_csv('Mas_Aclaracion_de_información_(Revision_ROCE).csv',index=False,encoding='latin1')


#crear vairiables de identificación
proyectos = {'1':'CNGE','2':'CNSPE','3':'CNSIPEE',
             '4':'CNPJE','5':'CNIJE',
             '6':'CNPLE','7':'CNDHE',
             '8':'CNTAIPPDPE'}

region = {'centro':[9],
          'centro_norte':[1,11,22,24],
          'centro_sur':[12,15,17],
          'noreste':[5,19,28],
          'noroeste':[2,3,25,26],
          'norte':[8,10,32],
          'occidente':[6,14,16,18],
          'oriente':[13,21,29,30],
          'sur':[7,20,27],
          'sureste':[4,23,31]}
#otro enfoque
test = df.copy()
valores1 = [f'Revisión OC ({x})' for x in range(1,10)]
v1c = [f'Aclaración de información OC ({x})' for x in range(1,10)]
valores1 += v1c
test['cont'] = [i for i in range(df.shape[0])]
testix = test.groupby(['Folio'])['cont'].transform(max) == test['cont']
ntest = test[testix]

ntest = ntest[ntest.Estatus.isin(valores1)] #aquí ya está el dataframe con los que tienen estatus de OC y no otro nuevo
#ya solo resta ordenarlo por fechas de llegada para su revision
ntest['Fecha'] =  pd.to_datetime(ntest['Registro'],format="%d/%m/%Y %H:%M:%S")
ntest = ntest.sort_values(by=['Fecha'])
ntest.insert(0,'Proyecto',[proyectos[x[-4]] for x in ntest['Folio']],allow_duplicates=False)
ntest.insert(1,'Módulo',[x[-4:] for x in ntest['Folio']],allow_duplicates=False)
ntest.insert(2,'Num_Entidad',[x[:-4] for x in ntest['Folio']],allow_duplicates=False)
reg = []
for val in ntest['Num_Entidad']:
    for k in region:
        if int(val) in region[k]:
            reg.append(k)
            break
ntest.insert(3,'Región',reg,allow_duplicates=False)
ntest.to_csv('Orden_de_atencion_por_fecha_de_llegada.csv',index=False,encoding='utf-8-sig')


#generar lista de fechas con pendientes
# valores1 = [f'Revisión OC ({x})' for x in range(1,10)]
# mdf = df[df.Estatus.isin(valores1)]
# # mdf['Registro'] = mdf['Registro'].map({'vacio':'01/01/2022 00:00:00'})
# mdf['Fecha'] = pd.to_datetime(mdf['Registro'],format="%d/%m/%Y %H:%M:%S")
# fe_ord = mdf.sort_values(by=['Fecha'])
# fe_ord['cont'] = [i for i in range(fe_ord.shape[0])]
# foldx = fe_ord.groupby(['Folio'])['cont'].transform(max) == fe_ord['cont']
# folios = fe_ord[foldx] #dataframe con un solo valor de folio, el que tiene la fecha más actual de revision de oc
# folios = folios.reset_index(drop=True)
# folios_in  = list(folios['Folio'])
# #conseguir el mismo dataframe de folios, pero con todos los tipos de estatus para comparar las fechas posteriormente
# #por problema para traducir fechas, se hace el referente con el contador de dias, bajo la lógica de que si ese contador es mayor, es porque ya cambió de estatus
# folios_out = []
# c = 0
# for folio in folios_in:
#     c1 = 0
#     for fol in df['Folio']:
#         if fol == folio:
#             if pd.to_datetime(df['Registro'][c1]) > folios['Fecha'][c]:
#                 folios_out.append(fol)
#                 break
#         c1 += 1
#     c += 1

# #borrar folios que ya tienen otro estatus 
# for folio in folios_out:
#     if folio in folios_in:
#         folios_in.remove(folio)
        
# foliosdf = df[df.Folio.isin(folios_in)]
# foliosdf['fecha'] = pd.to_datetime(foliosdf['Registro'],format="%d/%m/%Y %H:%M:%S")
# foliosdf = foliosdf.sort_values(by=['fecha'])
# #va nuevo filtro a partir de fechas
# foliosdf['cont'] = [i for i in range(foliosdf.shape[0])]
# idx = foliosdf.groupby(['Folio'])['cont'].transform(max) == foliosdf['cont']
# foliosdf = foliosdf[idx]