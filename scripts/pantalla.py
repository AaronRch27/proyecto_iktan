# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:55:58 2022

@author: AARON.RAMIREZ
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, StringVar
from leer_base_iktan import procesar, save


ventana = tk.Tk()
ventana.title('Prueba')
tk.Label(ventana, text="Hola, para iniciar presiona el botón y selecciona un archivo en formato .xlsx (excel) con el reporte de seguimiento tal como se descarga de la plataforma IKTAN").pack() 

equipos = {
    'CNSIPEE':'Integración de Información',
    'CNGE': 'Integración de Información',
    'CNSPE':'Integración de Información',
    'CNPJE':'Integración de Información',
    'CNIJE':'Control y Logística',
    'CNDHE':'Operación Estratégica',
    'vacio':'Sin equipo asignado'
    }


A = []
estado = StringVar()
censo = StringVar()

def obtener_retraso(df):
    df = df.reset_index(drop=True)
    retrasos = []#retrasos en revision de OC
    r2 = []#retrasos en tener firma y sellos
    c = 0
    for val in df['Rev_OC?']:
        if val == 'No':
            if type(df['Dias_inicio_RevOC'][c]) != str:
                if df['Dias_inicio_RevOC'][c].days < 0:
                    retrasos.append(df['Proyecto'][c])
        if df['Recuperado_firma_y_sello?'][c] == 'No':
            print(df['Dias_fin_Recfirma'][c])
            if type(df['Dias_fin_Recfirma'][c]) != str:
                if df['Dias_fin_Recfirma'][c].days < 0:
                    r2.append(df['Proyecto'][c])
        c += 1
    res = ''
    if retrasos:
        retrasos = list(set(retrasos))
        retrasos = ' '.join(retrasos)
        res += f'El o los censos siguientes tienen un retraso para su inicio de revisión en oficinas centrales: {retrasos} \n'
    if r2:
        r2 = list(set(r2))
        r2 = ' '.join(r2)
        res += f'El o los censos siguientes tienen un retraso para ser recuperados con firma y sello: {r2}'
    return res

def ruta():
    archivo = filedialog.askopenfile(mode='r')
    ROCE,OA,historial = procesar(archivo.name)
    save(ROCE,OA,historial)
    if type(ROCE) != list:
        tk.Label(ventana, text="Selecciona tu entidad ").pack()
        edos = ttk.Combobox(
            state='readonly',
            textvariable=estado,
            values=list(historial['Entidad'].unique())
            )
        edos.pack()
        def retrasos():
            edo = estado.get()
            filtro = historial.loc[historial['Entidad']==edo]
            texto = obtener_retraso(filtro)
            if texto:
                messagebox.showinfo(
                    message = texto,
                    title = '¡Alerta de retraso!'
                    )
            # br = ventana.pack_slaves()#limpiar interfaz
            # for val in br:
            #     val.destroy()
            
        tk.Button(ventana,
                  text ="Seleccionar",
                  command = retrasos).pack()
        tk.Label(ventana, text="Ahora selecciona el proyecto que quieres consultar ").pack()
        despl = ttk.Combobox(
            state='readonly',
            values=list(OA['Proyecto'].unique())
            )
        despl.pack()
        
        
        def consul():
            if A:
                br = ventana.pack_slaves()
                br[-1].destroy()
                br[-2].destroy()#para quitar tabla y mensaje
            pro = despl.get() #esta se usa con la variable equipos
            filtro = OA.loc[OA['Equipo']==equipos[pro]]
            filtro = filtro.loc[:,['Proyecto','Módulo','Entidad','Registro']]
            tk.Label(ventana, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ").pack()
            tab = tk.Text(ventana)
            tab.insert(tk.INSERT, filtro.to_string())
            tab.pack()
            A.append(1)
            return 
        tk.Button(ventana, text ="Consultar", command = consul).pack()
        


boton1 = tk.Button(ventana, text ="Iniciar", command = ruta)
boton1.pack()


ventana.mainloop()