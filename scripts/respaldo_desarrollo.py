# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:29:07 2022

@author: AARON.RAMIREZ
"""

import pandas as pd



#leer archivo descargado de iktan

documento = pd.read_excel('xIktan_20220907015014929_reporteSegumiento.xlsx')

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


#crear vairiables de identificación
proyectos = {'1':'CNGE','2':'CNSPE','3':'CNSIPEE',
             '4':'CNPJE','5':'CNIJE',
             '6':'CNPLE','7':'CNDHE',
             '8':'CNTAIPPDPE','a':'vacio',
             '0': 'vacio',
             'vacio': 'vacio'}

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
#variable con los equipos de trabajo para identificar 
#identificacion pr nombres estará descativada ya que con el proyecto se puede dar con el equipo que lo trabaja, sin emabrgo, esta variabl puede ser útil más adelante para identificar cargas de trabajo por persona
equipos_nom = { 
    'Operación Estratégica': ['LILIANA AVILA LOPEZ',
      'VERONICA ITZEL JIMENEZ GONZALEZ',#no estan en base de datos
      'MARIANA RIOS MARTINEZ',
      'DANIEL LOPEZ SANCHEZ'],#no estan en base de datos
    'Integración de Información': ['NALLELY BECERRIL DAVILA',
      'ROGELIO ROSALES MORALES',
      'JOSE MANUEL OCOMATL OLAYA',
      'HUGO GONZALEZ VALDEZ',
      'RUBI SAMANTHA MEDRANO MARTINEZ',
      'JOSE ANTONIO CHAVEZ CASTILLO',
      'VICTOR RAMIRO ESPINA CASAS',
      'ANA AGLAE FLORES AGUILAR'],
    'Control y Logística': ['ALEXEI PRADEL HERNANDEZ',
      'MA. GUADALUPE ADAME SALGADO',
      'KARLA FABIOLA ACEVEDO BERNARDINO',
      'ANTONIO ROMERO LEYVA',
      'YOLISMA IVETTE LOPEZ CERON',
      'DIANA LETICIA ALCALA GONZALEZ']
    }

#lineas para conseguir quienes están en la base y quienes no
plantilla = []
for k in equipos_nom:
    plantilla += equipos_nom[k]
# listasde=list(df['Usuario'])
# for nombre in plantilla:
#     if nombre in listasde:
#         print(nombre)


# equip =[]
# #proceso para asignar equipos a los diferentes folios por estatus de aclaracion de informacion OC
      
# for usuario in df['Usuario']:
#     if usuario in equipos['Operación Estratégica']:
#         equip.append('Operación Estratégica')
#     if usuario in equipos['Integración de Información']:
#         equip.append('Integración de Información')
#     if usuario in equipos['Control y Logística']:
#         equip.append('Control y Logística')
#     if usuario not in equipos['Operación Estratégica'] and usuario not in equipos['Integración de Información'] and usuario not in equipos['Control y Logística']:
#         equip.append('Sin equipo asignado a revisión') 

equipos = {
    'CNSIPEE':'Integración de Información',
    'CNGE': 'Integración de Información',
    'CNSPE':'Integración de Información',
    'CNPJE':'Integración de Información',
    'CNIJE':'Control y Logística',
    'CNDHE':'Operación Estratégica',
    'vacio':'Sin equipo asignado'
    }



df.insert(1,'Proyecto',[proyectos[x[-4]] if len(x)<8 else 'vacio' for x in df['Folio']],allow_duplicates=False)
df.insert(2,'Módulo',[x[-4:] for x in df['Folio']],allow_duplicates=False)
df.insert(3,'Num_Entidad',[x[:-4] for x in df['Folio']],allow_duplicates=False)
df.insert(4,'Equipo',[equipos[x] for x in df['Proyecto']],allow_duplicates=False)
reg = []
for val in df['Num_Entidad']:
    for k in region:
        try:
            if int(val) in region[k]:
                reg.append(k)
                break
        except:
            reg.append('vacio')
            break
df.insert(4,'Región',reg,allow_duplicates=False)

#hacer variables de fechas para revision oc y recuperacion de firmas y sellos
f_corte = {#cada llave tiene una lista con dos valores, el primero es la fecha de inicio a revision oc del cronograma y el segundo es la fecha de conclusion de recuperacion de firma 
    'CNSIPEE':['24/02/2022 00:00:00','10/06/2022 00:00:00'],
    'CNGE': ['09/05/2022 00:00:00','08/07/2022 00:00:00'],
    'CNSPE':['30/05/2022 00:00:00','29/07/2022 00:00:00'],
    'CNPJE':['13/06/2022 00:00:00','12/08/2022 00:00:00'],
    'CNIJE':['27/06/2022 00:00:00','12/08/2022 00:00:00'],
    'CNDHE':['15/08/2022 00:00:00','07/10/2022 00:00:00'],
    'vacio':['01/01/2022 00:00:00','01/01/2022 00:00:00']
    }
d_OC = []
d_firma = []
c = 0
for registro in df['Registro']:
    try:#porque por alguna razón hay fechas que no lee bien
        f_est = pd.to_datetime(registro,format="%d/%m/%Y %H:%M:%S")
        proy = df['Proyecto'][c]
        f_OC = pd.to_datetime(f_corte[proy][0],format="%d/%m/%Y %H:%M:%S")
        f_Fir = pd.to_datetime(f_corte[proy][1],format="%d/%m/%Y %H:%M:%S")
        d_OC.append(f_OC - f_est)
        d_firma.append(f_Fir - f_est)
    except:
        d_OC.append('Error en fechas')
        d_firma.append('Error en fechas')
    c += 1
df.insert(5,'Dias_inicio_RevOC',d_OC,allow_duplicates=False)#tener numero negativo quiere decir que ya se pasó la fecha y son los días de retraso
df.insert(6,'Dias_fin_Recfirma',d_firma,allow_duplicates=False)#tener numero negativo quiere decir que ya se pasó la fecha y son los días de retraso
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
             'Proyecto': [],
             'Módulo': [],
             'Entidad': [],
             'Región': [],
             'Usuario': [],
             'Perfil': [],
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
            respuesta['Módulo'].append(df['Módulo'][c])
            respuesta['Proyecto'].append(df['Proyecto'][c])
            respuesta['Región'].append(df['Región'][c])
            break
        c += 1

#generar archivo de respuesta con quienes han hecho más solucitudes(arriba de 3)
rt = pd.DataFrame(respuesta)
# rt.to_csv('Mas_Aclaracion_de_información_(Revision_ROCE).csv',index=False,encoding='latin1')
# with pd.ExcelWriter('analisis_seguimiento.xlsx',
#                     mode='a') as writer:  
#     rt.to_excel(writer, sheet_name='Revision_ROCE')



#generar orden de atención
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
#borrar columnas
del ntest['Observación']
del ntest['Contador de días']
del ntest['cont']
del ntest['Fecha']
del ntest['Dias_inicio_RevOC'] #porque si ya llegó aquí, no tiene caso mostrarlo
#ahora filtrar por miembros del equipo
fila = 0
borrar = []
ntest = ntest.reset_index(drop=True)
for val in list(ntest['Usuario']):
    if val not in plantilla:
        borrar.append(fila)
    fila += 1
ntest = ntest.drop(borrar,axis=0)
#guardar archivo
# ntest.to_csv('Orden_de_atencion_por_fecha_de_llegada.csv',index=False,encoding='utf-8-sig')
# with pd.ExcelWriter('analisis_seguimiento.xlsx',
#                     mode='a') as writer:  
#     ntest.to_excel(writer, sheet_name='Orden_atencion')



#generar historial de atención
#hacer nombres para nuevas columnas
revOC = [f'Revisión OC ({x})' for x in range(1,10)]
acOC = v1c
acROCEdOC = [f'Aclaración ROCE derivado de OC ({x})' for x in range(1,10)]
rROCEdOC = [f'Revisión ROCE derivado de OC ({x})' for x in range(1,10)]
firma = [f'En proceso de firma y sello ({x})' for x in range(1,10)]
nombres_col = []#aquí los nomnbres de las nuevas columnas para el frame
c = 0
for nombre in revOC:
    to = [nombre,acOC[c],acROCEdOC[c],rROCEdOC[c],firma[c]]
    for v in to:
        nombres_col.append(v)
    c += 1
#variable con estructura para nuevo dataframe
estructura = {'Folio':[],
             'Proyecto': [],
             'Módulo': [],
             'Entidad': [],
             'Región': [],
             'Equipo': [],
             'Rev_OC?': [],
             'Dias_inicio_RevOC': [],
             'Recuperado_firma_y_sello?': [],
             'Dias_fin_Recfirma': [],
             'Días_RevOC-último_estatus': []
             }
#sumarle los nombres de las otras columnas
for val in nombres_col:
    estructura[val] = []

#generar los datos para el frame

folios_unicos = list(df['Folio'].unique())
c1 = 0
for folio in folios_unicos:
    # filtrar frame por cada folio
    trabajar = df.loc[df['Folio']==folio]
    trabajar.reset_index(drop=True)
    for col in trabajar:
        if col in estructura:
            # print(col,trabajar.shape)
            estructura[col].append(list(trabajar[col])[0])
    #nuevo dic para evitar duplicados
    uctu = {}
    for val in nombres_col:
        uctu[val] = 'NA'
    fys = 'No'
    OC = 'No'
    c = 0
    for val in trabajar['Estatus']:
        if val in uctu:
            ultimo = pd.to_datetime(list(trabajar['Registro'])[c],format="%d/%m/%Y %H:%M:%S")
            uctu[val] = ultimo
        if 'Recuperado con firma y sello' in val:
            fys = 'Sí'
        if 'Revisión OC' in val:
            OC = 'Sí'
        
        c += 1
    estructura['Recuperado_firma_y_sello?'].append(fys)
    estructura['Rev_OC?'].append(OC)
    #calcular los días desde primera revision OC hasta su último estatus de revision
    if OC == 'Sí':
        # inicio = estructura['Revisión OC (1)'][c1]
        inicio = uctu['Revisión OC (1)']
        dias = (ultimo-inicio).days
        estructura['Días_RevOC-último_estatus'].append(dias)
    if OC == 'No':
        estructura['Días_RevOC-último_estatus'].append('No aplica')
    #llenar el resto de columnas para la fila que quedaorn en blanco
    # refe = len(estructura['Folio'])
    # for k in estructura:
    #     if len(estructura[k]) < refe:
    #         estructura[k].append('NA')
    for k in uctu:
        estructura[k].append(uctu[k])
            
    c1 += 1
historial = pd.DataFrame(estructura)
# historial.to_csv('Historial_de_revision_OC.csv',index=False,encoding='utf-8-sig')
# with pd.ExcelWriter('analisis_seguimiento.xlsx') as writer:  
#     rt.to_excel(writer, sheet_name='Revision_ROCE',index=False)
#     ntest.to_excel(writer, sheet_name='Orden_atencion',index=False)
#     historial.to_excel(writer, sheet_name='historial',index=False) 