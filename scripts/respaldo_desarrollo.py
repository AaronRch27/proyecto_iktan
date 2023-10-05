# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 13:29:07 2022

@author: AARON.RAMIREZ
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from gen_graf import generar_imagenes
from mensajes import mensajes


hoy =  datetime.now()

#leer archivo descargado de iktan

documento = pd.read_excel('xIktan_20231003030410237_reporteSegumiento.xlsx')

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
      # 'VERONICA ITZEL JIMENEZ GONZALEZ',#no estan en base de datos
      'MARIANA RIOS MARTINEZ',
      'VICTOR AYAX QUINTERO ORTEGA'],#solo Mariana y Víctor revisan en equipo de Lili
      # 'DANIEL LOPEZ SANCHEZ'],#no estan en base de datos
    'Integración de Información': ['NALLELY BECERRIL DAVILA',
      'ROGELIO ROSALES MORALES',
      'JOSE MANUEL OCOMATL OLAYA',
      'HUGO GONZALEZ VALDEZ',
      'RUBI SAMANTHA MEDRANO MARTINEZ',
      'JOSE ANTONIO CHAVEZ CASTILLO',
      'VICTOR RAMIRO ESPINA CASAS',
      'ANA AGLAE FLORES AGUILAR'],
    'Control y Logística': ['ALEXEI PRADEL HERNANDEZ',
      # 'MA. GUADALUPE ADAME SALGADO',
      'KARLA FABIOLA ACEVEDO BERNARDINO',
      # 'ANTONIO ROMERO LEYVA',
      'YOLISMA IVETTE LOPEZ CERON',
      'URIEL EDUARDO CAMPUZANO HERNANDEZ',
      # 'DIANA LETICIA ALCALA GONZALEZ',
      'EDWIN HECTOR PINEDA LOPEZ']
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
    'CNPLE': 'Operación Estratégica',
    'CNTAIPPDPE': 'Operación Estratégica',
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
    'CNSIPEE':['17/04/2023 00:00:00','30/06/2023 00:00:00'],
    'CNGE': ['24/04/2023 00:00:00','21/07/2023 00:00:00'],
    'CNSPE':['12/06/2023 00:00:00','31/08/2023 00:00:00'],
    'CNPJE':['26/06/2023 00:00:00','08/09/2023 00:00:00'],
    'CNIJE':['10/07/2023 00:00:00','15/09/2023 00:00:00'],
    'CNDHE':['21/08/2023 00:00:00','03/11/2023 00:00:00'],
    'vacio':['01/01/2023 00:00:00','01/01/2023 00:00:00']
    }
feriados = ['2023-02-06', '2023-03-20','2023-04-06','2023-04-07',
            '2023-05-01', '2023-05-05', '2023-07-08', '2023-09-16',
            '2023-11-02', '2023-11-20', '2023-12-25']
d_OC = []
d_firma = []
c = 0
for registro in df['Registro']:
    try:#porque por alguna razón hay fechas que no lee bien
        f_est = pd.to_datetime(registro,format="%d/%m/%Y %H:%M:%S")
        proy = df['Proyecto'][c]
        f_OC = pd.to_datetime(f_corte[proy][0],format="%d/%m/%Y %H:%M:%S")
        f_Fir = pd.to_datetime(f_corte[proy][1],format="%d/%m/%Y %H:%M:%S")
        # d_OC.append(f_OC - f_est)
        d_OC.append(round(np.busday_count(hoy.date(),
                               f_OC.date(),
                               holidays=feriados)))
        #d_firma.append(f_Fir - f_est)
        d_firma.append(round(np.busday_count(hoy.date(),
                               f_Fir.date(),
                               holidays=feriados)))
        
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
#se comenta aclaracipon de informacion oc porque este estatus no sirve para los turnos 
v1c = [f'Aclaración de información OC ({x})' for x in range(1,10)]
# valores1 += v1c
test['cont'] = [i for i in range(df.shape[0])]
testix = test.groupby(['Folio'])['cont'].transform(max) == test['cont']
ntest = test[testix]

ntest = ntest[ntest.Estatus.isin(valores1)] #aquí ya está el dataframe con los que tienen estatus de OC y no otro nuevo
#ya solo resta ordenarlo por fechas de llegada para su revision
ntest['Fecha'] =  pd.to_datetime(ntest['Registro'],format="%d/%m/%Y %H:%M:%S")
ntest = ntest.sort_values(by=['Fecha'])
#borrar columnas
# del ntest['Observación']
del ntest['Contador de días']
del ntest['cont']

del ntest['Dias_inicio_RevOC'] #porque si ya llegó aquí, no tiene caso mostrarlo
#ahora filtrar por miembros del equipo
fila = 0
# borrar = []
excluir = ['LILIANA AVILA LOPEZ','NALLELY BECERRIL DAVILA',
           'ALEXEI PRADEL HERNANDEZ'] #jefes de equipo que designan
nndiasOC = [] #conteo de días que tiene un cuestionario desde su llegada a oficinas centrales para asignacion y revision
nndiasrevOC = []#conteo de dias que tiene un cuestionario luego de ser asignado por jefe de equipo
ntest = ntest.reset_index(drop=True)
dlaborales = [] #este solo es para prueb, no tiene otra utilidad
#crear variable con dias no laborales de inegi año,mes,dia

for val in list(ntest['Usuario']):
    if val not in plantilla:
        var_alfa = 0
        if 'Revisión OC' in ntest.loc[fila,'Estatus']: 
            if ntest.loc[fila,'Estatus']== 'Revisión OC (1)':#acotarlo a la revision 1 porque ahí todavía no es asignado
                ntest.loc[fila,'Estatus'] = 'Pendiente' 
                ntest.loc[fila,'Usuario'] = 'Por asignar'
                var_alfa = 1
            else: #son revisiones oc más de 1
                #buscar la observacion para obtener al ultimo responsable designado
                responsbale_revisor = 'No asignado' #previamente asignado, por fdefecto es no asignado pero cambiará
                historial_folio=df[df['Folio']==ntest.loc[fila,'Folio']]
                historial_folio = historial_folio.reset_index(drop=True)
                #iterar para encontrar el estatus de asignación
                for i in list(historial_folio['Observación']):
                    if 'Folio asignado a usuario para su revisón a:' in i:
                        div_ob = i.split(':')
                        responsbale_revisor = div_ob[-1]
                        # ntest.loc[fila,'Estatus'] = 'En revisión' 
                        ntest.loc[fila,'Usuario'] = responsbale_revisor
                        
        #como no es usuario de los revisores ni jefes de equipo, se interpreta que su cuestionario no ha sido asignado para revision
        tam = historial_folio.shape
        ultimo_stat = historial_folio.loc[tam[0]-1,'Registro']#no es penultimo sino ultimo
        ultimo_stat = pd.to_datetime(ultimo_stat,format="%d/%m/%Y %H:%M:%S")
        # dife = hoy - penultimo_stat
        h_dif = hoy.hour - ultimo_stat.hour
        if h_dif < 0:
            n_hoy = hoy - pd.tseries.offsets.BusinessDay(1)
            horasdia = 1 - (((h_dif*-1) * 10 / 24) * 0.1)
            dife = np.busday_count(ultimo_stat.date(),
                                   n_hoy.date(),
                                   holidays=feriados)
        if h_dif >= 0:
            dife = np.busday_count(ultimo_stat.date(),
                               hoy.date(),
                               holidays=feriados)
            horasdia = (h_dif * 10 / 24) * 0.1
                   
        #verificar si es día no laboral el ultimo estatus
        
        dia_descanso = np.is_busday([ultimo_stat.date()],holidays=feriados).tolist()
        if not dia_descanso[0]:
            nndiasOC.append(round(dife + horasdia,1)+1)#Se suma uno para ajutsar porque lo enviaron en día no laboral y para que no sea mayor que la asignación de revisión OC
        if dia_descanso[0]:
            nndiasOC.append(round(dife + horasdia,1)) #por menos uno para pasarlo a positivo
        # dife = np.busday_count(ntest.loc[fila,'Fecha'].date(),
        #                        hoy.date(),
        #                        holidays=feriados)
        #aquí se agrega directamente lo mismo porque como el útlimo estatus es de otra persona fuera de OC pues eso
        # nndiasrevOC.append(round(dife + horasdia,1))
        #Hacer distinción en el cálculo si es primera revisión y no está asignado, o si ya es segunda revisión y hay un repsonsable revisor asignado
        if var_alfa:
            nndiasrevOC.append('NA')
        if not var_alfa:
            nndiasrevOC.append(round(dife + horasdia,1))
        # docc = hoy - ntest.loc[fila,'Fecha'] 
        # nndiasOC.append(docc.days)
        # nndiasrevOC.append('En revision')
    if val in plantilla:
        ntest.loc[fila,'Estatus'] = 'En revisión'  #dado que el equipo lo tiene debe cambiar este estatus a revision
        #de llegar aquí quiere decir que ya ha sido asignado el cuestionario y habría que revisar la observacion pra ver quien lo tiene a revision
        if val in excluir:
            observacion = ntest.loc[fila,'Observación']
            div_ob = observacion.split(':')
            revisor = div_ob[-1]
            # ntest.loc[fila,'Estatus'] = 'En revisión' 
            ntest.loc[fila,'Usuario'] = revisor
        historial_folio=df[df['Folio']==ntest.loc[fila,'Folio']]
        historial_folio = historial_folio.reset_index(drop=True)
        tam = historial_folio.shape
        penultimo_stat = historial_folio.loc[tam[0]-2,'Registro']
        penultimo_stat = pd.to_datetime(penultimo_stat,format="%d/%m/%Y %H:%M:%S")
        
        h_dif = hoy.hour - penultimo_stat.hour
        if h_dif < 0:
            n_hoy = hoy - pd.tseries.offsets.BusinessDay(1)
            horasdia = 1 - (((h_dif*-1) * 10 / 24) * 0.1)
            dife = np.busday_count(penultimo_stat.date(),
                                   n_hoy.date(),
                                   holidays=feriados)
        if h_dif >= 0:
            dife = np.busday_count(penultimo_stat.date(),
                               hoy.date(),
                               holidays=feriados)
            horasdia = (h_dif * 10 / 24) * 0.1
                   
        #verificar si es día de descanso el último estatus
        
        dia_descanso = np.is_busday([penultimo_stat.date()],holidays=feriados).tolist()
        if not dia_descanso[0]:
            nndiasOC.append(round(dife + horasdia,1)+1)#Se suma uno para ajutsar porque lo enviaron en día no laboral y para que no sea mayor que la asignación de revisión OC           
        if dia_descanso[0]:
            nndiasOC.append(round(dife + horasdia,1))
        
        ultimo_stat = historial_folio.loc[tam[0]-1,'Registro']
        ultimo_stat = pd.to_datetime(ultimo_stat,format="%d/%m/%Y %H:%M:%S")
        
        h_dif = hoy.hour - ultimo_stat.hour
        # print(ultimo_stat,hoy, h_dif)
        if h_dif < 0:
            n_hoy = hoy - pd.tseries.offsets.BusinessDay(1)
            horasdia = 1 - (((h_dif*-1) * 10 / 24) * 0.1)
            dife = np.busday_count(ultimo_stat.date(),
                                   n_hoy.date(),
                                   holidays=feriados)
        if h_dif >= 0:
            dife = np.busday_count(ultimo_stat.date(),
                               hoy.date(),
                               holidays=feriados)
            horasdia = (h_dif * 10 / 24) * 0.1
        # dife = np.busday_count(ultimo_stat.date(),
        #                        hoy.date(),
        #                        holidays=feriados)
        nndiasrevOC.append(round(dife + horasdia,1))
    # retraso = hoy - ntest.loc[fila,'Fecha'] 
    retraso = np.busday_count(ultimo_stat.date(), 
                              hoy.date(),
                              holidays=feriados)
    if retraso > 5:
        #si hay retraso no se cambia al usuario
        # ntest.loc[fila,'Usuario'] = 'Retraso en aisgnación'
        ntest.loc[fila,'Estatus'] = 'FueraT'
        # borrar.append(fila)
    fila += 1
del ntest['Fecha']
del ntest['Observación']
ntest['dias_en_OC'] = nndiasOC
ntest['dias_en_rev_OC'] = nndiasrevOC
ntest = pd.DataFrame(ntest)
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
             'el_cuestionario_aplica?': [],
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
    aplica = 'Sí'
    c = 0
    for val in trabajar['Estatus']:
        if val in uctu:
            ultimo = pd.to_datetime(list(trabajar['Registro'])[c],format="%d/%m/%Y %H:%M:%S")
            uctu[val] = ultimo
        if 'Recuperado con firma y sello' in val:
            fys = 'Sí'
        if 'Revisión OC' in val:
            OC = 'Sí'
        if 'No aplica (1)' in val:
            aplica = 'No'
        
        c += 1
    estructura['Recuperado_firma_y_sello?'].append(fys)
    estructura['Rev_OC?'].append(OC)
    estructura['el_cuestionario_aplica?'].append(aplica)
    #calcular los días desde primera revision OC hasta su último estatus de revision
    if OC == 'Sí':
        # inicio = estructura['Revisión OC (1)'][c1]
        inicio = uctu['Revisión OC (1)']
        #dias = (ultimo-inicio).days
        dias = round(np.busday_count(inicio.date(),
                               ultimo.date(),
                               holidays=feriados),1)
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
fecha = list(df['Folio'])[-2] #fecha de descarga de la base
# historial.to_csv('Historial_de_revision_OC.csv',index=False,encoding='utf-8-sig')
# with pd.ExcelWriter('analisis_seguimiento.xlsx') as writer:  
#     rt.to_excel(writer, sheet_name='Revision_ROCE',index=False)
#     ntest.to_excel(writer, sheet_name='Orden_atencion',index=False)
#     historial.to_excel(writer, sheet_name='historial',index=False) 



#### avance de revision de censos por equipo

censos = list(df['Proyecto'].unique())
if 'vacio' in censos:
    censos.remove('vacio')
cen_can = {} #cantidad de cuestionarios
avan = []
revi = []
liber = []
NoAp = []

for censo in censos:
    bb = df.loc[df['Proyecto']==censo]
    cantidad = len(list(bb['Folio'].unique()))
    cen_can[censo] = cantidad
    #otro proceso dentro de esta iteracion
    # bb = df.loc[df['Proyecto']==censo]
    filtros = list(bb['Folio'].unique())
    r = 0 #suma de recuperados con firma y sello--concluidos
    OCCC = 0 #suma de revisiones
    lib = 0 #suma de cuestionarios revisados
    nop = 0 #no aplica
    if censo == 'CNGE':
        revisiss={'Entidad':[],'Modulo':[],'folio':[]}
    for filtro in filtros:
        bb1 = bb.loc[bb['Folio']==filtro]
        sta = list(bb1['Estatus'])
        suma = False
        suma1 = False
        suma2 = False
        suma3 = False
        for es in sta:
            if 'No aplica' in es:
                suma3 = True
            if 'Revisión OC' in es:
                suma1 = True
            if 'En proceso de firma y sello (1)' in es:
                suma2 = True
            if 'Recuperado con firma y sello (1)' in es:
                suma = True
                
        if suma and not suma3:
            r += 1
        if suma1:
            OCCC += 1
        if suma2:
            lib += 1
        if suma3:
            if censo=='CNGE':
                revisiss['Entidad'].append(list(bb1['Entidad'])[0])
                revisiss['Modulo'].append(list(bb1['Módulo'])[0])
                revisiss['folio'].append(filtro)
            nop += 1
    avan.append(r)
    revi.append(OCCC)
    liber.append(lib)
    NoAp.append(nop)
avance = {'Equipo':[equipos[x] for x in list(cen_can.keys())],
       'Programa':list(cen_can.keys()),
       'Cuestionarios':list(cen_can.values()),
       'revisiones':revi,
       'cuestionarios_liberados':liber,
       'Avance_recuperados_conFyS':avan,
       'Cuestionarios_NoAplica': NoAp,
       'Porcentaje_de_conclusion(recup_firmaysello_y_NoAplica)':[]
       }
c = 0
for val in list(cen_can.values()):
    avance['Porcentaje_de_conclusion(recup_firmaysello_y_NoAplica)'].append(f'{round((avan[c]+NoAp[c])*100/val)}%')
    c += 1
avance = pd.DataFrame(avance)

#Desempeño de los revisores
revs = [f'Aclaración de información OC ({x})' for x in range(1,15)]
fff = ['En proceso de firma y sello (1)'] #solo este porque los demas ya corresponden aveces a otro miembro de los revisores, generalmente del equipo de Alexei
nw1 = df[df.Estatus.isin(revs+fff)]
nw2 = df[df.Estatus.isin(revOC)]
gen_jef = nw2.copy()
general_r = nw1.copy()
general = df.copy()
excluir = ['LILIANA AVILA LOPEZ','NALLELY BECERRIL DAVILA',
           'ALEXEI PRADEL HERNANDEZ']
control = {
    'usuario':[],
    'equipo':[],
    'cuestionarios_revisados':[],
    'promedio_dias_revision':[],
    'prom_revisiones_por_cuestionario':[],
    'Max_dias_en_rev':[]
    }
control_jefes = {
    'usuario':[],
    'equipo':[],
    'cuestionarios_asignados':[],
    'dias_prom_asig_cuestionario':[],
    'dias_max_asig_cuestionario':[],
    'dias_max_asig_cuestionario(folio)':[],
    'cuest_asignados_fuerade_horario_lab': [],
    'cuest_asignados_fuerade_horario_lab(folio)':[]
    }
for usuario in plantilla: #itearar por cada usuario en el directorio de OC
    # if usuario not in excluir: #sacar a los jefes   
    folios = general_r.loc[general_r['Usuario']==usuario]#cuestionarios del usuario
    cuestionarios_revisados = list(folios['Folio'].unique())
    #conseguir el equipo del usuario
    for equpo in equipos_nom:
        if usuario in equipos_nom[equpo]:
            control['equipo'].append(equpo)
    # print(usuario,len(cuestionarios_revisados))
    control['usuario'].append(usuario)
    revisados = len(cuestionarios_revisados) if df.isin([f'Folio asignado a usuario para su revisón a: {usuario}']).any().any() else 0
    control['cuestionarios_revisados'].append(revisados)
    n_revisiones = [] #numero de revisiones por cuestionario
    fechas = []#lista con tuplas de fecha inicio revision OC y fecha de siguiente estatus que es cuando terminaron de revisar
    if revisados:  #nuevo filtro e comprobación para calcular datos solo si hizo revisiones--- ver caso de nayeli, no hizo revisiones entonces no tiene sentido calcular 
        for cuestionario in cuestionarios_revisados:
            folio = general.loc[general['Folio']==cuestionario]#solo con los folios de un cuestionario--es base pequeña
            folio = folio.reset_index(drop=True)
            ultimoOC = 0 #conteo de  revisiones
            c = 0
            for proceso in list(folio['Usuario']):
                if usuario == proceso and 'reconsulta' not in list(folio['Estatus'])[c]:
                    f_ini = folio['Registro'][c-1]
                    f_term = folio['Registro'][c]
                    inicio = datetime.strptime(f_ini,"%d/%m/%Y %H:%M:%S")
                    term = datetime.strptime(f_term,"%d/%m/%Y %H:%M:%S")
                    # resta = term-inicio
                    h_dif = term.hour - inicio.hour
                    # resta = np.busday_count(inicio.date(),
                    #                        term.date(),
                    #                        holidays=feriados)
                    if h_dif < 0:
                        n_hoy = term - pd.tseries.offsets.BusinessDay(1)
                        horasdia = 1 - (((h_dif*-1) * 10 / 24) * 0.1)
                        dife = np.busday_count(inicio.date(),
                                               n_hoy.date(),
                                               holidays=feriados)
                    if h_dif >= 0:
                        dife = np.busday_count(inicio.date(),
                                           term.date(),
                                           holidays=feriados)
                        horasdia = (h_dif * 10 / 24) * 0.1
                    fechas.append(round(dife + horasdia,1)) 
                    # fechas.append(resta.days) 
                    # if usuario == 'JOSE ANTONIO CHAVEZ CASTILLO' and resta.days>15: #esto es solo para veririfcar tema de tiempos y encontrar el folio donde fue registrado
                    #     print(cuestionario,'77777777', resta,inicio,term)
                    ultimoOC += 1
                c += 1
                   
            if ultimoOC:
                # num = ''
                # for letra in ultimoOC:
                #     if letra.isdigit():
                #         num += letra
                # revision = int(num) #sacar numero de la string y convertirlo a formato numero
                n_revisiones.append(ultimoOC)
    # print(usuario,len(fechas),fechas,len(n_revisiones),sum(n_revisiones)) #los len no son iguales porque hay más revisiones y el numero de aquí solo representa la cantidad de ellas, mientras que las fechas es una tupla por revision
    control['promedio_dias_revision'].append(sum(fechas) / len(fechas) if len(fechas)>0 else 0)
    control['prom_revisiones_por_cuestionario'].append(sum(n_revisiones) / len(n_revisiones) if len(n_revisiones)>0 else 0)
    control['Max_dias_en_rev'].append(max(fechas) if fechas else 0)
    
            
    #ahora conseguir métricas para los jefes
    if usuario in excluir:
        folios = gen_jef.loc[gen_jef['Usuario']==usuario]#cuestionarios donde participa el jefe
        cuestionarios_asignados = list(folios['Folio'].unique())
        #conseguir el equipo del usuario
        for equpo in equipos_nom:
            if usuario in equipos_nom[equpo]:
                control_jefes['equipo'].append(equpo)
        # print(usuario,len(cuestionarios_revisados))
        control_jefes['usuario'].append(usuario)
        control_jefes['cuestionarios_asignados'].append(len(cuestionarios_asignados))
        fechas = []
        folio_fechas = []
        asig_fuera_lab_fol = []
        for cuestionario in cuestionarios_asignados:
            folio = general.loc[general['Folio']==cuestionario]#solo con los folios de un cuestionario--es base pequeña
            folio = folio.reset_index(drop=True)
            c = 0
            revi = list(folio['Estatus'])
            for proceso in list(folio['Usuario']):
                if usuario == proceso and revi[c] in revOC:#este filtro es para solo seleccionar al usuario cuando hizo un estatus de asignacion revision OC numero que sea
                    f_ini = folio['Registro'][c-1]
                    f_term = folio['Registro'][c]
                    folio1_rev = revi[c-1]
                    folio2_rev = revi[c]
                    if folio1_rev in revOC and folio2_rev in revOC:
                        #esta excepción deriva de una doble asignación de cuestionario. Esto no se debe tomar en cuenta [ver caso de Nayeli con Alexei]
                        if usuario == list(folio['Usuario'])[c-1]:
                            continue
                    inicio = datetime.strptime(f_ini,"%d/%m/%Y %H:%M:%S")
                    term = datetime.strptime(f_term,"%d/%m/%Y %H:%M:%S")
                    h_dif = term.hour - inicio.hour
                    #conseguir numero y folios asignados fuera de horario laboral o de días laborales
                    comprobar = np.is_busday([term.date()],holidays=feriados)
                    comprobar = comprobar.tolist()
                    if term.hour > 17 or not comprobar[0]:
                        asig_fuera_lab_fol.append(cuestionario)
                    
                    # resta = np.busday_count(inicio.date(),
                    #                        term.date(),
                    #                        holidays=feriados)
                    if h_dif < 0:
                        n_hoy = term - pd.tseries.offsets.BusinessDay(1)
                        horasdia = 1 - (((h_dif*-1) * 10 / 24) * 0.1)
                        dife = np.busday_count(inicio.date(),
                                               n_hoy.date(),
                                               holidays=feriados)
                    if h_dif >= 0:
                        dife = np.busday_count(inicio.date(),
                                           term.date(),
                                           holidays=feriados)
                        horasdia = (h_dif * 10 / 24) * 0.1
                    fechas.append(round(dife + horasdia,1)) 
                    folio_fechas.append(cuestionario)
                    #sigueientes dos lineas son para comprobación de retrasos en asignacion para nayeli
                    # if round(dife + horasdia,1) > 6:
                    #     print(cuestionario,usuario,round(dife + horasdia,1))
                c += 1
        # print(usuario,fechas)
        control_jefes['dias_prom_asig_cuestionario'].append(sum(fechas) / len(fechas) if len(fechas)>0 else 0)
        control_jefes['dias_max_asig_cuestionario'].append(max(fechas) if len(fechas)>0 else 0)
        control_jefes['cuest_asignados_fuerade_horario_lab'].append(len(asig_fuera_lab_fol))
        control_jefes['cuest_asignados_fuerade_horario_lab(folio)'].append(asig_fuera_lab_fol)
        folio_fech = ''
        for i,f in enumerate(fechas):
            if f == max(fechas):
                folio_fech = folio_fechas[i]   
                break
        control_jefes['dias_max_asig_cuestionario(folio)'].append(folio_fech)
            
desempe = pd.DataFrame(control)
desem_jefes = pd.DataFrame(control_jefes)


#Apartado para generar un reporte de carga de trabajo a los responsables revisores, por día laboral
#Primer paso es generar una matriz donde los indices sean los dias laborales, y las columnas los nombres de los responsbales revisores
matriz_carga = {'dia_laboral':[]}
matriz_folios_carga = {'dia_laboral':[]}
#agregar responsables revisores
for user in control['usuario']:
    matriz_carga[user] = []
    matriz_folios_carga[user] = []
#agregar días indice pero desde abril, ya que enero a marzo no hay revision en oc
filas_fecha = pd.date_range(start=pd.to_datetime('01/04/2023 00:00:00',format="%d/%m/%Y %H:%M:%S"),
                            end=pd.to_datetime(fecha,format="%d/%m/%Y %H:%M:%S")#termina en la fecha de corte de la base de datos (dia que se descargó)
                            )
#corroborar que sean días laborales en inegi
for date in list(filas_fecha):
    comprobar = np.is_busday([date.date()],holidays=feriados)
    comprobar = comprobar.tolist()
    if comprobar[0]:
        matriz_carga['dia_laboral'].append(date.date())
        matriz_folios_carga['dia_laboral'].append(date.date())

#llenar con ceros
for key in matriz_carga:
    if key != "dia_laboral":
        matriz_carga[key] = [0 for i in matriz_carga['dia_laboral']]
        matriz_folios_carga[key] = [[] for i in matriz_carga['dia_laboral']] # esta no se vair a dataframe todavía
MC = pd.DataFrame(matriz_carga,index=matriz_carga['dia_laboral'])
MDF = pd.DataFrame(matriz_folios_carga,index=matriz_folios_carga['dia_laboral'])
#inicio de conteo de cuestionarios por día
#filtrar base por folios unicos
trabajo_dias = df.copy()#copiado del frame original de iktan
trabajo_dias.drop([df.shape[0]-1,df.shape[0]-2],axis=0,inplace=True)
folios_unicos = list(trabajo_dias['Folio'].unique())
for folio in folios_unicos:
    frame = trabajo_dias.loc[trabajo_dias['Folio']==folio]
    frame = frame.reset_index(drop=True)
    #identificar al responsable revisor del folio
    responsbale_revisor = False
    for i in list(frame['Observación']):
        if 'Folio asignado a usuario para su revisón a:' in i:
            div_ob = i.split(':')
            responsbale_revisor = div_ob[-1]
    if not responsbale_revisor:
        #de no existir se pasa al siguiente folio
        continue
    # if responsbale_revisor==' RUBI SAMANTHA MEDRANO MARTINEZ':
    #     print(folio)
    fila = 0
    for estatus in list(frame['Estatus']):
        if 'Revisión OC' in estatus:
            num_rev  = estatus[-3:]
            # print(estatus,frame.loc[fila,'Usuario'])
            if '(1)' in estatus and frame.loc[fila,'Usuario'] in excluir:
                fecha_inicial_rev = pd.to_datetime(frame.loc[fila,'Registro'].split(' ')[0],format="%d/%m/%Y")
            if '(1)' not in estatus:
                fecha_inicial_rev = pd.to_datetime(frame.loc[fila,'Registro'].split(' ')[0],format="%d/%m/%Y")
            if '(1)' in estatus and frame.loc[fila,'Usuario'] not in excluir:
                fila += 1
                continue
            try:#porque quizá el indcie excede el len del frame y podría ser error.
                fecha_fin_rev = pd.to_datetime(frame.loc[fila+1,'Registro'].split(' ')[0],format="%d/%m/%Y")
            except:
                tomorrow =  hoy + timedelta(days=1)
                fecha_fin_rev = tomorrow.date()
            #igualar horas de fecha final para no saltar ningun día
            # if folio == '152101':
            #     resta = fecha_inicial_rev-fecha_fin_rev
            #     print(resta)
            lista_dias = list(pd.date_range(start=fecha_inicial_rev,
                                        end=fecha_fin_rev
                                        ))
            # if folio == '152101':
                # print(fecha_inicial_rev,fecha_fin_rev,'estos')
                # print(lista_dias)
            for dia in lista_dias:
                try:
                    MC.loc[dia.date(),responsbale_revisor[1:]] += 1
                    MDF.loc[dia.date(),responsbale_revisor[1:]].append(folio+'-'+num_rev)
                except:
                    
                    pass
                
                
        fila += 1
index_f1 = list(MC['dia_laboral'])
index_f = index_f1[:-1]
del MC['dia_laboral'] #borrar columna de indices para que no se duplique
del MDF['dia_laboral']
#con esto ya se tiene el frame en MC con los cuestionarios que tienen o tenían por día. Sin embargo falta hacer una limpieza de los días donde no tuvieron nada y del último día porque ese no da un buen cálculo.
#iterar por usuario en frame de avance
maximo_carga_por_dia = []
promedio_carga_trabajo = []
n_retrasos_en_rev = []
n_retrasos_7 = []
num_revisados = []
max_rev_al_dia = []
matriz_rev = {}
retr_cuest_asig_fhlab = []
retr_cuest_asig_fhlab_fol = []
total_revisiones = [] #esto solo es para desarrollo. No está contemplado en los indicadores de acro, solo en powerbi
#matriz resumen solo es para el desarrollo!!! power bi
matriz_resumen = {'Fecha':[],
                  'Folio':[],
                  'Censo':[],
                  'Módulo':[],
                  'Región':[],
                  'Entidad':[],
                  'Equipo':[],
                  'Revisor':[],
                  'Días_en_revisión':[],
                  'Retraso+5':[],
                  'Retraso+7':[],
                  'Retraso+5_histórico':[],
                  'Retraso+7_histórico':[]}
#Esta matriz es también solo de entorno de desarrollo y es para generar el modelo de regresion lineal
regresion = {'revisor':[],
             'censo':[],
             'modulo':[],
             'entidad':[],
             # 'promedio_carga_trabajo':[],
             'num_de_revision':[],
             'dias_en_revision':[]
    }
foly_retr = {}
for usuario in desempe['usuario']:
    valores = list(MC[usuario])
    if sum(valores) == 0:
        #anteriormente se asignaba un NA a los valores sin registro, pero por comodidad en la presentacion de datos para tablero power bi se cambió a ceros. Esto solo ocurre en apartado para desarrollo, porque en acro sigue estando igual, con los NA
        maximo_carga_por_dia.append(0)
        promedio_carga_trabajo.append(0)
        n_retrasos_en_rev.append(0)
        n_retrasos_7.append(0)
        num_revisados.append(0)
        max_rev_al_dia.append(0)
        retr_cuest_asig_fhlab.append(0)
        retr_cuest_asig_fhlab_fol.append(0)
        total_revisiones.append(0)
    else:
        f1 = desempe.loc[desempe['usuario']==usuario]
        equipo_revisor = list(f1['equipo']) 
        inicio_rev = 0
        for valor in valores:
            if valor != 0:#detectar el primer cero para sacar su indice y trabajar sobre ese
                break
            inicio_rev += 1
        efectivos = valores[inicio_rev:]#menos uno porque no interesa el dato final ya que ese no es preciso por ser fecha de corte de la descarga de la base de datos
        maximo_carga_por_dia.append(max(efectivos))
        promedio_carga_trabajo.append(sum(efectivos)/len(efectivos))
        #conteo de cuestionarios con retraso
        folio_r = list(MDF[usuario])
        folio_efectivo = folio_r[inicio_rev:]
        fol_tot = {}
        num_revi = [0]
        max_rev_al = 0
        atraso = 0
        fol_asig_hlab = []
        #apartado para contar numero de revisiones hechas en el día
        lcinco = []
        lsiete1 = [] 
        for n, lista in enumerate(folio_efectivo):
            cinco = 0
            siete1 = 0 
            if n > 0:
                rev = 0
                #iterar folios de dia anterior
                for fol in folio_efectivo[n-1]:
                    if fol not in lista:
                        rev +=1
                num_revi.append(rev)
                max_rev_al = max([max_rev_al,rev])
            #contar el numero de veces quue aparece el folio en los días de revision
            for fol in lista:
                inf_folio = df.loc[df['Folio']==fol[:-4]]
                inf_folio = inf_folio.reset_index(drop=True)
                matriz_resumen['Censo'].append(list(inf_folio['Proyecto'])[0])
                matriz_resumen['Módulo'].append(list(inf_folio['Módulo'])[0])
                matriz_resumen['Región'].append(list(inf_folio['Región'])[0])
                matriz_resumen['Entidad'].append(list(inf_folio['Entidad'])[0])
                matriz_resumen['Fecha'].append(index_f1[inicio_rev:][n])
                matriz_resumen['Folio'].append(fol)
                matriz_resumen['Equipo'].append(equipo_revisor[0])
                matriz_resumen['Revisor'].append(usuario)
                
                regresion['revisor'].append(usuario)
                regresion['censo'].append(inf_folio['Proyecto'][0])
                regresion['modulo'].append(inf_folio['Módulo'][0])
                regresion['entidad'].append(inf_folio['Entidad'][0])
                regresion['num_de_revision'].append(int(fol[-2:-1]))
                
                if fol not in fol_tot:
                    fol_tot[fol] = 1
                else:
                    fol_tot[fol] += 1
                    
                regresion['dias_en_revision'].append(fol_tot[fol])
                #conteo de folio con retraso 5 y 7
                five = 0
                seven = 0
                if fol_tot[fol] > 5:
                    cinco += 1
                    five = 1
                    #revisar folios asignados fuera de horario laboral con retraso en revisiones mayores a 5 días
                    if fol.endswith('(1)'):#solo para la revision 1 se hará este analaisis ya que es donde se justifica el retraso en asignaciones fuera de la jornada laboral
                        asignaciones_jefe = desem_jefes.loc[desem_jefes['equipo']==equipo_revisor[0]]
                        asignaciones_jefe = list(asignaciones_jefe['cuest_asignados_fuerade_horario_lab(folio)'])[0] 
                        if fol[:-4] in asignaciones_jefe:
                            fol_asig_hlab.append(fol)
                if fol_tot[fol] > 7:
                    seven = 1
                    siete1 += 1
                matriz_resumen['Días_en_revisión'].append(fol_tot[fol])
                matriz_resumen['Retraso+5'].append(1 if fol_tot[fol]==6 else 0)
                matriz_resumen['Retraso+7'].append(1 if fol_tot[fol] == 8 else 0)#es importante dejarlo así con igual a ocho para no contar más elementos con retrasos mas 7, ya que está pensado para usarse en powerbi y eso genera una sobrestimación de casos
                matriz_resumen['Retraso+5_histórico'].append(five)
                matriz_resumen['Retraso+7_histórico'].append(seven)
            lcinco.append(cinco)
            lsiete1.append(siete1)
        fol_asig_hlab = list(set(fol_asig_hlab))
        retr_cuest_asig_fhlab.append(len(fol_asig_hlab)) 
        retr_cuest_asig_fhlab_fol.append(fol_asig_hlab) 
        #generarla imagen por usuario
        num_rev1 = num_revi + [0]
        num_rev1.pop(0)
        generar_imagenes(index_f1[inicio_rev:],
                         usuario,efectivos,
                         num_rev1,lcinco,
                         lsiete1)
        foly_retr[usuario] = fol_tot
        total_revisiones.append(len(fol_tot))
        #apartado para calcular el numero de folios con retrasos 
        cuest_retrasados = [] #lista con los cuestionarios retrasados
        siete = []
        for k in fol_tot:
            if fol_tot[k] > 5:
                cuest_retrasados.append(k)
            if fol_tot[k] > 7:
                siete.append(k)
        n_retrasos_en_rev.append(len(cuest_retrasados))
        n_retrasos_7.append(len(siete))
        num_revisados.append(sum(num_revi)/len(num_revi))
        max_rev_al_dia.append(max_rev_al)
        #rellenar columna con ceros para matriz de interpretacion
        relleno = [0 for i in range(inicio_rev)]
        matriz_rev[usuario] = relleno+num_revi
        matriz_rev[usuario].pop(0)#eliminar primer registro para acomodar todo a las fechas adecuadas en donde se hizo la revision
        # print(usuario,num_revi,len(relleno+num_revi))

desempe['maximo_carga_por_dia'] = maximo_carga_por_dia
desempe['promedio_carga_trabajo_por_dia'] = promedio_carga_trabajo
desempe['revisiones_con_mas_5_dias'] = n_retrasos_en_rev
desempe['revisiones_con_mas_7_dias'] = n_retrasos_7
desempe['promedio_revisiones_al_dia'] = num_revisados
desempe['maximo_revisiones_al_dia'] = max_rev_al_dia
desempe['retrasos_con_asignacion_fuera_hlab'] = retr_cuest_asig_fhlab
desempe['retrasos_con_asignacion_fuera_hlab_fol'] = retr_cuest_asig_fhlab_fol
desempe['Total_revisiones'] = total_revisiones

frame_rev = pd.DataFrame(matriz_rev,index=index_f)

#generar matriz de folios con atraso +5 y +7
mas5 = {}
mas7 = {}
l5 = []
l7 = []
for usuario in foly_retr:
    cinco = []
    siete = []
    for folio in foly_retr[usuario]:
        if foly_retr[usuario][folio] > 5 and foly_retr[usuario][folio] <= 7:
            cinco.append(folio)
        if foly_retr[usuario][folio] > 7:
            siete.append(folio)
    mas5[usuario] = cinco
    mas7[usuario] = siete
    l5.append(len(cinco))
    l7.append(len(siete))

for usuario in mas5:
    if len(mas5[usuario]) < max(l5):
        ceros_sumar = max(l5) - len(mas5[usuario])
        ss = [0 for i in range(ceros_sumar)]
        mas5[usuario] += ss
    if len(mas7[usuario]) < max(l7):
        ceros_sumar = max(l7) - len(mas7[usuario])
        ss = [0 for i in range(ceros_sumar)]
        mas7[usuario] += ss

#Esto solo irá en el desarrollo, debido a que corresponde al proceso de generar o actualizar el powerbi
MR = pd.DataFrame(matriz_resumen)
MR.to_csv('matriz_resumen.csv',index=False,encoding='latin-1')
with pd.ExcelWriter('matriz_resumen_pow.xlsx') as writer:  
    desempe.to_excel(writer, sheet_name='desempeño',index=False)
    # MC.to_excel(writer, sheet_name='Dias_carga_cuestionarios')
    # MDF.to_excel(writer, sheet_name='Dias_carga_cuestionarios_folio')
    # frame_rev.to_excel(writer, sheet_name='revisiones_por_dia')
    MR.to_excel(writer, sheet_name='matriz_resumen',index=False)
    desem_jefes.to_excel(writer, sheet_name= 'desem_jefes',index=False)
    avance.to_excel(writer, sheet_name='avance',index=False)
    
#crear salida para enviar mensajes
d_salida = {}
for usuario in MDF:
    #conseguir los folios del usuario cargas de trabajo
    historico_folios = list(MDF[usuario])
    #solo seleccionar los folios de día previo de descarga de la base
    interes =  historico_folios[-1]#el útlimo día es es de la fecha de descarga de la base
    d_salida[usuario] = {}
    for folio in interes:
        if folio not in foly_retr[usuario]:#se trata de folios recien asignados
            continue
        # if foly_retr[usuario][folio] == 4:
        #     inf_folio = df.loc[df['Folio']==folio[:-4]]
        #     inf_folio = inf_folio.reset_index(drop=True)
        #     censo = list(inf_folio['Proyecto'])[0]
        #     modulo = list(inf_folio['Módulo'])[0]
        #     entidad = list(inf_folio['Entidad'])[0]
        #     texto = f'{censo} {entidad} {modulo}'
        #     if 4 in d_salida[usuario]:
        #         d_salida[usuario][4].append(texto)
        #     else:
        #         d_salida[usuario][4] = [texto]
        if foly_retr[usuario][folio] == 5:
            inf_folio = df.loc[df['Folio']==folio[:-4]]
            inf_folio = inf_folio.reset_index(drop=True)
            censo = list(inf_folio['Proyecto'])[0]
            modulo = list(inf_folio['Módulo'])[0]
            entidad = list(inf_folio['Entidad'])[0]
            texto = f'{censo} {entidad} {modulo}'
            if 5 in d_salida[usuario]:
                d_salida[usuario][5].append(texto)
            else:
                d_salida[usuario][5] = [texto]
        if foly_retr[usuario][folio] > 5 and foly_retr[usuario][folio] < 8:
            inf_folio = df.loc[df['Folio']==folio[:-4]]
            inf_folio = inf_folio.reset_index(drop=True)
            censo = list(inf_folio['Proyecto'])[0]
            modulo = list(inf_folio['Módulo'])[0]
            entidad = list(inf_folio['Entidad'])[0]
            texto = f'{censo} {entidad} {modulo}'
            if 6 in d_salida[usuario]:
                d_salida[usuario][6].append(texto)
            else:
                d_salida[usuario][6] = [texto]
        if foly_retr[usuario][folio] > 7:
            inf_folio = df.loc[df['Folio']==folio[:-4]]
            inf_folio = inf_folio.reset_index(drop=True)
            censo = list(inf_folio['Proyecto'])[0]
            modulo = list(inf_folio['Módulo'])[0]
            entidad = list(inf_folio['Entidad'])[0]
            texto = f'{censo} {entidad} {modulo}'
            if 7 in d_salida[usuario]:
                d_salida[usuario][7].append(texto)
            else:
                d_salida[usuario][7] = [texto]
                
#va comentada para no enviarlos en automático!
# mensajes(d_salida)
        


#continuar ocn generacion de matriz para regresion lineal

# dregresion = pd.DataFrame(regresion)
# dregresion = dregresion.groupby(['modulo','entidad']).max()
# serie_comp = desempe['promedio_carga_trabajo_por_dia']
# serie_comp = serie_comp.set_axis(desempe['usuario'])
# addd = [serie_comp[user] for user in dregresion['revisor']]
# dregresion['carga_trabajo_promedio'] = addd
# #guardar el frame sin codificar para tomar en cuenta los datos de entrada
# dregresion.to_csv('regresion_ini.csv',encoding='latin1')
# dregresion = pd.DataFrame(dregresion)

# def codificar(df,col,l_var):
#     "transforar el frame con la columna codificada/l_var es letra de variable para identificarla"
#     dimension = len(list(df[col].unique()))
#     equivalencias = {}
#     #generar matrix
#     for i,val in enumerate(df[col].unique()):
#         equivalencias[val] = [0 for n in range(dimension-1)]
#         if i == 0:
#             continue
#         equivalencias[val][i-1] = 1
#     print(equivalencias)
# # import matplotlib.pyplot as plt

# codificar(dregresion,'revisor','x')
# filtro = desempe.loc[desempe['cuestionarios_revisados']>0]
# del filtro['retrasos_con_asignacion_fuera_hlab_fol']
# # filtro = filtro.loc[filtro['equipo']=='Integración de Información']
# filtro = filtro.reset_index(drop=True)

# for var in filtro.iloc[:,3:]:
#     fig, ax = plt.subplots()
#     ax.scatter(filtro['cuestionarios_revisados'],filtro[var])
#     ax.set_title(var)
#     fig.show()
    