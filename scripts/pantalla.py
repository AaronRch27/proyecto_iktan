# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:55:58 2022

@author: AARON.RAMIREZ
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, StringVar
from leer_base_iktan import procesar, save
from datetime import datetime

hoy =  datetime.now()
ventana = tk.Tk()
ventana.title('Prueba')
ventana.geometry('900x600')
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

A = []#variables control
B = []#variables control
estado = StringVar()
persona = StringVar()
censo = StringVar()

def mod_text(texto):
    "funcion para modificartexto de estatus y reducirlo"
    lista = texto.split()
    resultado = []
    for val in lista[:-1]: #menos 1 es el parentesis con el numero de revision, ese no es necesrio
        resultado.append(val[:2])
    res = ' '.join(resultado)
    return res

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
    ROCE,OA,historial,fecha_d = procesar(archivo.name)
    save(ROCE,OA,historial)
    if type(ROCE) != list:
        tk.Label(ventana, text="Selecciona tu entidad ").pack()
        edos = ttk.Combobox(
            state='readonly',
            textvariable=estado,
            values=list(historial['Entidad'].unique())+['Todos']
            )
        edos.pack()
        def retrasos():
            edo = estado.get()
            if edo != 'Todos':
                filtro = historial.loc[historial['Entidad']==edo]
                texto = obtener_retraso(filtro)
                if texto:
                    messagebox.showinfo(
                        message = texto,
                        title = '¡Alerta de retraso!'
                        )
            B.append(1) #variable control para desplegar nuevo boton
            br = ventana.pack_slaves()#limpiar interfaz
            for val in br[:5]:
                val.destroy()
            if B:
                tk.Label(ventana, 
                         text="Ahora selecciona el proyecto que quieres consultar "
                         ).pack()
                tk.Label(ventana, 
                         text="Si el proyecto que buscas no está en lista, o directamente no hay lista, es porque aún no ha sido asignado para revisión o tiene un estatus diferente a los registrados para revisión en Oficinas Centrales",
                         font=('Times 10'),
                         wraplength=650
                         ).pack()
                if edo != 'Todos':
                    OA1 = OA.loc[OA['Entidad']==edo]
                    despl = ttk.Combobox(
                        state='readonly',
                        values=list(OA1['Proyecto'].unique())
                        )
                if edo == 'Todos':
                    despl = ttk.Combobox(
                        state='readonly',
                        values=list(OA['Proyecto'].unique())
                        )
                despl.pack()
                
                
                def consul():
                    
                    if A:
                        br = ventana.pack_slaves()
                        if len(br)==8:
                            for sl in br[-4:]:
                                sl.destroy()
                        if len(br)==10:
                            for sl in br[-6:]:
                                sl.destroy()
                        # br[-1].destroy()
                        # br[-2].destroy()#para quitar tabla y mensaje
                    tk.Label(ventana,text='Fecha de descarga de base: '+fecha_d[:11]).pack()
                    tk.Label(ventana,text='Fecha de esta consulta:'+ hoy.strftime("%d/%m/%Y")).pack()
                    pro = despl.get() #esta se usa con la variable equipos
                    filtro = OA.loc[OA['Equipo']==equipos[pro]]
                    turnos = [i for i in range(1,len(list(filtro['Usuario']))+1)]
                    filtro['Turno'] = turnos
                    #sobrescribir estatus para ahorrar espacio
                    filtro['Estatus'] = [mod_text(i) for i in list(filtro['Estatus'])] 
                    filtro['Registro'] = [i[:11] for i in list(filtro['Registro'])]
                    filtro = filtro.set_index('Turno')
                    filtro = filtro.loc[:,['Proyecto',
                                           'Módulo','Entidad',
                                           'Registro','Estatus',
                                           'Usuario']]
                    tk.Label(ventana, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ").pack()
                    tab = tk.Text(ventana,width=100)
                    tab.insert(tk.INSERT, filtro.to_string())
                    tab.pack()
                    A.append(1)
                    li_des = ttk.Combobox(
                        state='readonly',
                        textvariable=persona,
                        values=list(filtro['Usuario'].unique())
                        ).pack()
                    
                    def f_per():
                        perso = persona.get()
                        br = ventana.pack_slaves()
                        for sl in br[-4:]:
                            sl.destroy()
                        filtro1 = filtro.loc[filtro['Usuario']==perso]
                        turnos = [i for i in range(1,len(list(filtro1['Usuario']))+1)]
                        filtro1['Turno'] = turnos
                        filtro1 = filtro1.set_index('Turno')
                        tk.Label(ventana, text="Los módulos que revisa la persona seleccionada son los siguientes: ").pack()
                        tab = tk.Text(ventana,width=100)
                        tab.insert(tk.INSERT, filtro1.to_string())
                        tab.pack()
                        return
                    
                    tk.Button(ventana, text ="Filtrar", command = f_per).pack()    
                    return 
                tk.Button(ventana, text ="Consultar", command = consul).pack()
                
        tk.Button(ventana,
                  text ="Seleccionar",
                  command = retrasos).pack()

boton1 = tk.Button(ventana, text ="Iniciar", command = ruta)
boton1.pack()


ventana.mainloop()
