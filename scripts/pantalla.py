# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:55:58 2022

@author: AARON.RAMIREZ
"""

import tkinter as tk
from tkinter import filedialog, ttk
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

def consul(des,OA):
    pro = des.get() #esta se usa con la variable equipos
    filtro = OA.loc[OA['Proyecto']==pro]
    filtro = filtro.loc[:,['Proyecto','Módulo','Entidad','Registro']]
    tk.Label(ventana, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ").pack()
    tab = tk.Text(ventana)
    tab.insert(tk.INSERT, filtro.to_string())
    tab.pack()
    return 
A = []

def ruta():
    archivo = filedialog.askopenfile(mode='r')
    ROCE,OA,historial = procesar(archivo.name)
    if type(ROCE) != list:
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
            print(equipos[pro])
            filtro = OA.loc[OA['Equipo']==equipos[pro]]
            filtro = filtro.loc[:,['Proyecto','Módulo','Entidad','Registro']]
            tk.Label(ventana, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ").pack()
            tab = tk.Text(ventana)
            tab.insert(tk.INSERT, filtro.to_string())
            tab.pack()
            A.append(1)
            return 
        tk.Button(ventana, text ="Consultar", command = consul).pack()
        


# def labs():
#     return tk.Label(ventana, text="¡Hola Mundo!").pack() 

# boton = tk.Button(ventana, text ="Hello", command = labs)
# boton.pack()

boton1 = tk.Button(ventana, text ="Iniciar", command = ruta)
boton1.pack()


ventana.mainloop()