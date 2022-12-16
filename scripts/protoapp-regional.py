# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 16:31:01 2022

@author: AARON.RAMIREZ
"""

import tkinter as tk
from leer_base_iktan import procesar, save
from datetime import datetime
from tkinter import filedialog, ttk, messagebox, StringVar


class aplicacion(tk.Frame):
    
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.title('ACIRO')
        self.master.geometry('900x200')
        self.pack()
        self.texto_in = 'Para fines internos exclusivamente (personal operativo)'
        self.hoy = datetime.now()
        self.A = []#variables control
        self.estado = StringVar()
        self.persona = StringVar()
        self.censo = StringVar()
        self.utilidades()
        
    def utilidades(self):
        br = self.pack_slaves()#limpiar interfaz
        for val in br:
            val.destroy()
        l1 = tk.Label(self, text="Hola, para iniciar presiona el botón y selecciona un archivo en formato .xlsx (excel) con el reporte de seguimiento tal como se descarga de la plataforma IKTAN")
        l1.pack()
        boton1 = tk.Button(self, text ="Iniciar", command = self.ruta)
        boton1.pack()
        tk.Label(self, text=self.texto_in).pack()
        
    def ruta(self):
        try:
            archivo = filedialog.askopenfile(mode='r')
            self.ROCE,self.OA,self.historial,self.fecha_d,self.avance,self.desemp = procesar(archivo.name)
            save(self.ROCE,self.OA,self.historial,self.avance)
            if type(self.ROCE) != list:
                
                br = self.pack_slaves()#limpiar interfaz
                for val in br:
                    val.destroy()
                l2 = tk.Label(self, text="Selecciona tu región ")
                l2.pack()
                edos = ttk.Combobox(self,
                    state='readonly',
                    textvariable=self.estado,
                    values=list(self.historial['Región'].unique())+['Todos']
                    )
                edos.pack()                    
                b2=tk.Button(self,
                          text ="Seleccionar",
                          command = self.retrasos)
                b2.pack()
                tk.Label(self, text=self.texto_in).pack()
        except Exception as e:
            tk.Label(self, text="Error en la lectura, selecciona otro archivo ").pack()
            tk.Label(self, text=e).pack()
            
    def retrasos(self):
        edo = self.estado.get()
        self.edd = edo
        br = self.pack_slaves()#limpiar interfaz
        for val in br:
            val.destroy()
        if edo == '' or edo== 'vacio':
            texto = 'Debes seleccionar algún estado'
            messagebox.showinfo(
                message = texto,
                title = 'Error de selección'
                )
            return
        if edo != 'Todos':
            filtro = self.historial.loc[self.historial['Región']==edo]
            texto = self.obtener_retraso(filtro)
            if texto:
                messagebox.showinfo(
                    message = texto,
                    title = '¡Alerta de retraso!'
                    )
        if edo =='Todos':
            rev = list(self.OA['Estatus'])
            if 'FueraT' in rev:
                texto = self.retrasoOC(self.OA)
                messagebox.showinfo(
                    message = texto,
                    title = '¡Alerta de retraso!'
                    )
        

        tk.Label(self, 
                 text="Ahora selecciona el proyecto que quieres consultar "
                 ).pack()
        tk.Label(self, 
                 text="Si el proyecto que buscas no está en lista, o directamente no hay lista, es porque aún no ha sido asignado para revisión o tiene un estatus diferente a los registrados para revisión en Oficinas Centrales",
                 font=('Times 10'),
                 wraplength=650
                 ).pack()
        if edo != 'Todos':
            OA1 = self.OA.loc[self.OA['Región']==edo]
            self.despl = ttk.Combobox(self,
                state='readonly',
                values=list(OA1['Proyecto'].unique())
                )
        if edo == 'Todos':
            self.despl = ttk.Combobox(self,
                state='readonly',
                values=list(self.OA['Proyecto'].unique())
                )
        self.despl.pack()
        b2=tk.Button(self, text ="Consultar", command = self.consul)
        b2.pack()
        #agregar boton de regreso
        btr = tk.Button(self, text ="Regresar", command = self.utilidades)
        btr.pack() 
        tk.Label(self, text=self.texto_in).pack()
        
    def consul(self):
        self.NV = tk.Toplevel(self)
        self.NV.title('Tabla de turnos')
        self.NV.geometry('900x700')
        tk.Label(self.NV,text='Fecha de descarga de base: '+self.fecha_d[:11]).pack()
        tk.Label(self.NV,text='Fecha de esta consulta:'+ self.hoy.strftime("%d/%m/%Y")).pack()
        pro = self.despl.get() #esta se usa con la variable equipos
        equipos = {
            'CNSIPEE':'Integración de Información',
            'CNGE': 'Integración de Información',
            'CNSPE':'Integración de Información',
            'CNPJE':'Integración de Información',
            'CNIJE':'Control y Logística',
            'CNDHE':'Operación Estratégica',
            'vacio':'Sin equipo asignado'
            }
        filtro = self.OA.loc[self.OA['Equipo']==equipos[pro]]
        turnos = [i for i in range(1,len(list(filtro['Usuario']))+1)]
        filtro['Turno'] = turnos
        #sobrescribir estatus para ahorrar espacio
        filtro['Estatus'] = [self.mod_text(i) for i in list(filtro['Estatus'])] 
        filtro['Registro'] = [i[:11] for i in list(filtro['Registro'])]
        filtro = filtro.set_index('Turno')
        filtro = filtro.loc[filtro['Región'] == self.edd] if self.edd!='Todos' else filtro
        self.filtro = filtro.loc[:,['Proyecto',
                               'Módulo','Entidad',
                               'Registro','Estatus',
                               'Usuario']]
        tk.Label(self.NV, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ").pack()
        tab = tk.Text(self.NV,width=100)
        tab.insert(tk.INSERT, self.filtro.to_string())
        tab.pack()
        self.A.append(1)
        li_des = tk.ttk.Combobox(self.NV,
            state='readonly',
            textvariable=self.persona,
            values=list(self.filtro['Usuario'].unique())
            )
        li_des.pack()
        b3 = tk.Button(self.NV, text ="Filtrar", command = self.f_per)
        b3.pack()  
        
        filtro2 = self.avance.loc[self.avance['Equipo']==equipos[pro]]
        filtro2 = filtro2.loc[:,['Programa','Porcentaje']]
        tk.Label(self.NV, text='Avance de revisión del equipo: ').pack()
        AV = tk.Label(self.NV, text=filtro2.to_string())
        AV.config(font=("Courier", 10))
        AV.pack()
        tk.Label(self.NV, text=self.texto_in).pack()
    
    def consul1(self):
        br = self.NV.pack_slaves()
        for sl in br:
            sl.destroy()
        tk.Label(self.NV,text='Fecha de descarga de base: '+self.fecha_d[:11]).pack()
        tk.Label(self.NV,text='Fecha de esta consulta:'+ self.hoy.strftime("%d/%m/%Y")).pack()
        pro = self.despl.get() #esta se usa con la variable equipos
        equipos = {
            'CNSIPEE':'Integración de Información',
            'CNGE': 'Integración de Información',
            'CNSPE':'Integración de Información',
            'CNPJE':'Integración de Información',
            'CNIJE':'Control y Logística',
            'CNDHE':'Operación Estratégica',
            'vacio':'Sin equipo asignado'
            }
        filtro = self.OA.loc[self.OA['Equipo']==equipos[pro]]
        turnos = [i for i in range(1,len(list(filtro['Usuario']))+1)]
        filtro['Turno'] = turnos
        #sobrescribir estatus para ahorrar espacio
        filtro['Estatus'] = [self.mod_text(i) for i in list(filtro['Estatus'])] 
        filtro['Registro'] = [i[:11] for i in list(filtro['Registro'])]
        filtro = filtro.set_index('Turno')
        filtro = filtro.loc[filtro['Región'] == self.edd] if self.edd!='Todos' else filtro
        self.filtro = filtro.loc[:,['Proyecto',
                               'Módulo','Entidad',
                               'Registro','Estatus',
                               'Usuario']]
        tk.Label(self.NV, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ").pack()
        tab = tk.Text(self.NV,width=100)
        tab.insert(tk.INSERT, self.filtro.to_string())
        tab.pack()
        self.A.append(1)
        li_des = tk.ttk.Combobox(self.NV,
            state='readonly',
            textvariable=self.persona,
            values=list(self.filtro['Usuario'].unique())
            )
        li_des.pack()
        b3 = tk.Button(self.NV, text ="Filtrar", command = self.f_per)
        b3.pack() 
        tk.Label(self.NV, text=self.texto_in).pack()
    
    def f_per(self):
        perso = self.persona.get()
        br = self.NV.pack_slaves()
        for sl in br[2:]:
            sl.destroy()
        filtro1 = self.filtro.loc[self.filtro['Usuario']==perso]
        turnos = [i for i in range(1,len(list(filtro1['Usuario']))+1)]
        filtro1['Turno'] = turnos
        filtro1 = filtro1.set_index('Turno')
        tk.Label(self.NV, text="Los módulos que revisa la persona seleccionada son los siguientes: ").pack()
        tab = tk.Text(self.NV,width=100)
        tab.insert(tk.INSERT, filtro1.to_string())
        tab.pack()
        #aquí condicional par que sino son de OC no se despliegue la informacion de desempeño
        #comienza filtro para desplegar desempeño de responsable revisor
        filtro2 = self.desemp.loc[self.desemp['usuario']==perso]
        tk.Label(self.NV, text='Desempeño en revisiones').pack()
        tk.Label(self.NV, text=filtro2.to_string()).pack()
        #boton para regresar
        brt1 = tk.Button(self.NV, text ="Regresar", command = self.consul1)
        brt1.pack()
        tk.Label(self.NV, text=self.texto_in).pack()
        return
    
    @staticmethod
    def mod_text(texto):
        "funcion para modificartexto de estatus y reducirlo"

        if 'Revisión OC' in texto or 'Pendiente' in texto:
            res = 'Pendiente'
        elif 'FueraT' in texto:
            res = 'En revisión'
        else:
            res = 'En revisión'
        return res
    
    @staticmethod    
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
    
    @staticmethod
    def retrasoOC(df):
        fil = df.loc[df['Estatus']=='FueraT']
        equi = list(fil['Equipo'].unique())
        res = {}
        for e in equi:
            f = fil.loc[fil['Equipo']==e]
            res[e] = list(f['Proyecto'].unique())
        salida = 'El o los siguientes equipos tienen un retraso en asignación para revisión de módulos en los siguientes proyectos: '+str(res)
        return salida
    
ventana = tk.Tk()
app = aplicacion(master=ventana)
app.mainloop()