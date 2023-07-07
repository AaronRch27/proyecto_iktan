# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 16:31:01 2022

@author: AARON.RAMIREZ
"""

import tkinter as tk
from leer_base_iktan import procesar, save
from datetime import datetime
from tkinter import filedialog, ttk, messagebox, StringVar
from hacer_presentacion import gen_presentacion,borrar_imagenes

class aplicacion(tk.Frame):
    
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Asistente de Control y Rendimiento Operativo')
        #self.master.geometry('900x200')
        self.logo = tk.PhotoImage(file="Utilidades_app/acro_log.png")
        self.master.iconphoto('wm',self.logo)
        self.master.configure(bg='#def3f6')
        self.pack()
        
        self.texto_in = 'Para fines internos exclusivamente (personal operativo)'
        self.hoy = datetime.now()
        self.A = []#variables control
        self.estado = StringVar()
        self.contras = StringVar()
        self.user = StringVar()
        self.persona = StringVar()
        self.censo = StringVar()
        self.utilidades()
        
    def utilidades(self):
        br = self.pack_slaves()#limpiar interfaz
        for val in br:
            val.destroy()
        #crear el marco---propósitos estéticos
        self.frame1 = tk.Frame(self,height=250, width=400, bg='#def3f6')
        self.frame1.pack()
        lab = tk.Label(self.frame1,
                       text=self.texto_in,
                       font=('Helvetica 8'),
                       bg='#def3f6',
                       fg='red')
        lab.pack(side=tk.BOTTOM,anchor="w")
        l2 =tk.Label(self.frame1, 
                     text='Iniciar consulta',
                     fg='white',
                     justify=tk.LEFT)
        l2.pack(fill='x',anchor='w')
        l2.config(bg='#0099cc')
        l3 = tk.Label(self.frame1,
                      text='BIENVENIDO',
                      fg='#0099cc',
                      bg='#def3f6',
                      font=15)
        l3.pack(ipady=15,fill='x', expand=False)
        texto_a = """¡Hola! 
                    Recuerde, para poder iniciar con el proceso de consulta previamente deberá obtener el archivo en formato .xlsx (excel) correspondiente al seguimiento tal como se descarga de la plataforma IKTAN.
                    """
        l1 = tk.Label(self.frame1, text=texto_a,wraplength=900,font=16,bg='white')
        l1.pack(pady=30,padx=20)
        boton1 = tk.Button(self.frame1, text ="Iniciar", command = self.ruta)
        boton1.pack()
        tk.Label(self.frame1, text='Para iniciar presione el botón',
                 bg='#def3f6',
                 font=('Arial',7)).pack(fill='x')
        
    def ruta(self):
        try:
            archivo = filedialog.askopenfile(mode='r')
            self.ROCE,self.OA,self.historial,self.fecha_d,self.avance,self.desemp,self.jefes,self.MC,self.MDF,self.frame_rev = procesar(archivo.name)
            ##aqui pantalla de usuarios, el save se hará solo si es OC
            # save(self.ROCE,self.OA,self.historial,self.avance)
            if type(self.ROCE) != list:
                self.perfil_operativo_fun()
                
        except Exception as e:
            tk.Label(self.frame1, text="Error en la lectura, selecciona otro archivo ").pack()
            tk.Label(self.frame1, text=e).pack()
    
    def perfil_operativo_fun(self):
        # imagen= tk.PhotoImage(file='usuario.png')
        br = self.pack_slaves()#limpiar interfaz
        for val in br:
            val.destroy()
        self.frame1 = tk.Frame(self,height=250, width=400, bg='#def3f6')
        self.frame1.pack()
        l1 = tk.Label(self.frame1, text="Perfil operativo ",
                      fg='white',
                      bg='#0099cc')
        l1.pack(fill='x',ipadx=150)
        tk.Label(self.frame1,
                 # image=imagen,
                 text='USUARIO',
                 # compound=tk.LEFT,
                 fg='#0099cc',
                 bg='#def3f6'
                 ).pack()
        users = ttk.Combobox(self.frame1,
            state='readonly',
            textvariable=self.user,
            values=['Regional','OC']
            )
        users.pack()
        tk.Label(self.frame1,text='',bg='#def3f6').pack(pady=65)#este es solo para darle altura a la ventana 
        
        #definir funcion para crear desplegables a partir de la elección del usuario en su tipo de usuario
        def eleccion(evento):
            t_usuario = evento.widget.get()
            self.el_usuario = evento.widget.get() #variable para identificar la información a desplegar más adelante en las tablas de turnos y desempeño
            if t_usuario == 'Regional':
                br = self.frame1.pack_slaves()#limpiar interfaz
                if len(br)>2:
                    for val in br[3:]:
                        val.destroy()
                l2 = tk.Label(self.frame1, text="Selecciona tu región ",bg='#def3f6')
                l2.pack(fill='x')
                edos = ttk.Combobox(self.frame1,
                    state='readonly',
                    textvariable=self.estado,
                    values=list(self.OA['Región'].unique())
                    )
                edos.pack()                    
                b2=tk.Button(self.frame1,
                          text ="Seleccionar",
                          command = self.retrasos)
                b2.pack(pady=20)
                tk.Label(self.frame1,
                         text=self.texto_in,
                         bg='#def3f6',
                         fg='red').pack()
            
            if t_usuario == 'OC':
                br = self.frame1.pack_slaves()#limpiar interfaz
                if len(br)>2:
                    for val in br[3:]:
                        val.destroy()
                l2 = tk.Label(self.frame1, text="Introduce la contraseña ",bg='#def3f6')
                l2.pack(fill='x')
                contra = tk.Entry(self.frame1,
                                  textvariable=self.contras,
                                  show="*"
                                  )
                contra.pack()
                b2=tk.Button(self.frame1,
                          text ="Continuar",
                          command = self.val_con)
                b2.pack(pady=20)
                tk.Label(self.frame1,
                         text=self.texto_in,
                         bg='#def3f6',
                         fg='red').pack()
            
        users.bind("<<ComboboxSelected>>", eleccion)
    
    def val_con(self):
        contra = self.contras.get()
        if contra == 'contraseñaOC':
            self.edd = 'Todos'
            save(self.ROCE,self.OA,self.historial,self.avance,self.desemp,self.jefes,self.MC,self.MDF,self.frame_rev,self.fecha_d)
            br = self.pack_slaves()#limpiar interfaz
            for val in br:
                val.destroy()
            rev = list(self.OA['Estatus'])
            #hacer presentación
            try:
                gen_presentacion()
            except:
                messagebox.showinfo(
                    message = 'Debido a que primero inició sesión como usuario regional, se han borrado las imagenes generadas para construir la presentación de desempeño. Si desea obtenerla, es necesario volver a cargar un cuestionario para su lectura y a continuación, ingresar con usuario OC',
                    title = '¡problema con presentación de desempeño!'
                    )
            #crear el marco---propósitos estéticos
            self.frame1 = tk.Frame(self,height=250, width=400, bg='#def3f6')
            self.frame1.pack()
            if 'FueraT' in rev:
                # texto = self.retrasoOC(self.OA)
                texto = 'Con base a los términos establecidos en el cronograma general de actividades del programa censal, solicitamos de su apoyo para dar continuidad con la dinámica establecida en plan integral de seguimiento.'
                messagebox.showinfo(
                    message = texto,
                    title = '¡Alerta de desfase en la planeación!'
                    )
            l1 = tk.Label(self.frame1, text="Carga de trabajo ",
                          fg='white',
                          bg='#0099cc')
            l1.pack(fill='x',anchor='w')
            tk.Label(self.frame1, 
                     text="Selecciona el proyecto a consultar ",
                     bg='#def3f6'
                     ).pack()
            

            self.despl = ttk.Combobox(self.frame1,
                state='readonly',
                values=list(self.OA['Proyecto'].unique())
                )
            self.despl.pack()
            b2=tk.Button(self.frame1, text ="Consultar", command = self.consul)
            b2.pack(pady=10)
            
            tk.Label(self.frame1, 
                     text="""NOTA.
                     Si en el catálogo no se enlista el programa a consultar, es porque aún no se ha asignado cuestionario al equipo revisor o tiene un estatus diferente al destinado para ser carga de trabajo en OC. """,
                     font=('Times 10'),
                     wraplength=600,
                     bg='white'
                     ).pack(pady=15,padx=20)
            #agregar boton de regreso
            btr = tk.Button(self.frame1, text ="Regresar", command = self.perfil_operativo_fun)
            btr.pack(anchor='w') 
            tk.Label(self.frame1,
                     text=self.texto_in,
                     bg='#def3f6',
                     fg='red').pack()
        else:
            texto = 'Contraseña incorrecta'
            messagebox.showinfo(
                message = texto,
                title = 'Error'
                )
            return
            
    def retrasos(self):
        edo = self.estado.get()
        self.edd = edo
        # br = self.pack_slaves()#limpiar interfaz
        # for val in br:
        #     val.destroy()
        if edo == '' or edo== 'vacio':
            texto = 'Debes seleccionar algún estado'
            messagebox.showinfo(
                message = texto,
                title = 'Error de selección'
                )
            return
        if edo != 'Todos':
            borrar_imagenes()
            br = self.pack_slaves()#limpiar interfaz
            for val in br:
                val.destroy()
            filtro = self.historial.loc[self.historial['Región']==edo]
            texto1 = self.obtener_retraso(filtro)
            #se genera un nuevo texto para requerimentos de Alexei en mensaje de error
            texto = 'Con base a los términos establecidos en el cronograma general de actividades del programa censal, solicitamos de su apoyo para dar continuidad con la dinámica establecida en plan integral de seguimiento.' 
            if texto1:
                messagebox.showinfo(
                    message = texto,
                    title = '¡Alerta de desfase en la planeación!'
                    )
        if edo =='Todos':
            br = self.pack_slaves()#limpiar interfaz
            for val in br:
                val.destroy()
            rev = list(self.OA['Estatus'])
            if 'FueraT' in rev:
                # texto = self.retrasoOC(self.OA)
                texto = 'Con base a los términos establecidos en el cronograma general de actividades del programa censal, solicitamos de su apoyo para dar continuidad con la dinámica establecida en plan integral de seguimiento.'
                messagebox.showinfo(
                    message = texto,
                    title = '¡Alerta de desfase en la planeación!'
                    )
        
        #crear el marco---propósitos estéticos
        self.frame1 = tk.Frame(self,height=250, width=400, bg='#def3f6')
        self.frame1.pack()
        l1 = tk.Label(self.frame1, text="Carga de trabajo ",
                      fg='white',
                      bg='#0099cc')
        l1.pack(fill='x')
        tk.Label(self.frame1, 
                 text="Ahora selecciona el proyecto que quieres consultar ",
                 bg='#def3f6'
                 ).pack()
        
        if edo != 'Todos':
            OA1 = self.OA.loc[self.OA['Región']==edo]
            self.despl = ttk.Combobox(self.frame1,
                state='readonly',
                values=list(OA1['Proyecto'].unique())
                )
        if edo == 'Todos':
            self.despl = ttk.Combobox(self.frame1,
                state='readonly',
                values=list(self.OA['Proyecto'].unique())
                )
        self.despl.pack(pady=10)
        b2=tk.Button(self.frame1, text ="Consultar", command = self.consul)
        b2.pack(pady=10)
        tk.Label(self.frame1, 
                 text="""NOTA.
                 Si en el catálogo no se enlista el programa a consultar, es porque aún no se ha asignado cuestionario al equipo revisor o tiene un estatus diferente al destinado para ser carga de trabajo en OC. """,
                 font=('Times 10'),
                 wraplength=600,
                 bg='white'
                 ).pack(pady=15,padx=20)
        #agregar boton de regreso
        btr = tk.Button(self.frame1, text ="Regresar", command = self.perfil_operativo_fun)
        btr.pack(anchor='w') 
        tk.Label(self.frame1,
                 text=self.texto_in,
                 bg='#def3f6',
                 fg='red').pack()
        
    def consul(self):
        self.NV = tk.Toplevel(self,bg='#def3f6')
        self.NV.title(self.texto_in)
        #crear el marco---propósitos estéticos
        self.frame1 = tk.Frame(self.NV, bg='#def3f6')
        self.frame1.pack()
        l1 = tk.Label(self.frame1, text="Distribución de carga de trabajo ",
                      fg='white',
                      bg='#0099cc')
        l1.pack(fill='x')
        # self.NV.geometry('900x700')
        tk.Label(self.frame1,text='Fecha de corte: '+self.fecha_d,
                 bg='#def3f6').pack(anchor='w')#self.fecha_d[:11]
        
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
        # filtro = filtro.set_index('Turno')
        filtro = filtro.loc[filtro['Región'] == self.edd] if self.edd!='Todos' else filtro
        self.filtro = filtro.loc[:,['Turno','Proyecto',
                               'Módulo','Entidad',
                               'Registro','Estatus',
                               'Usuario','dias_en_OC',
                               'dias_en_rev_OC']]
        # tk.Label(self.frame1, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ",
        #          bg='#def3f6').pack(pady=20,padx=15)
        # tab = tk.Text(self.frame1,width=100)
        # tab.insert(tk.INSERT, self.filtro.to_string())
        # tab.pack(pady=10)
        medidas = {'Turno':45,'Proyecto':60,
                   'Módulo':60,'Entidad':105,
                   'Registro':80,'Estatus':100,
                   'Usuario':125,'dias_en_OC':65,
                   'dias_en_rev_OC':95}
        arbol = ttk.Treeview(self.frame1)
        arbol['columns'] = list(self.filtro.columns)
        arbol.column('#0', width=0, stretch=tk.NO)#borrar primera columna porque sale vacia      
        for x in list(self.filtro.columns):
            arbol.column(x, width=medidas[x], anchor='center' )
            arbol.heading(x, text=x)
        for imm in range(len(self.filtro)):
            arbol.insert('', tk.END, values=(list(self.filtro.iloc[imm,:])))
        arbol.pack()
        #boton de generar excel con los datos
        boton_g = tk.Button(self.frame1,
                            text='Generar excel con estos datos',
                            command=self.gen_excel)
        boton_g.pack()
        
        self.A.append(1)
        tk.Label(self.frame1, 
                 text='Filtros de consulta',
                 bg='grey'
                 ).pack(fill='x',pady=5,ipady=5)
        li_des = tk.ttk.Combobox(self.frame1,
            state='readonly',
            textvariable=self.persona,
            values=list(self.filtro['Usuario'].unique())
            )
        li_des.pack()
        tk.Label(self.frame1, 
                 text='Selecciona a la persona resonsable revisor(a)',
                 bg='#def3f6').pack()
        b3 = tk.Button(self.frame1, text ="Consultar", command = self.f_per)
        b3.pack(pady=5)  
        
        #sino es OC el usuario no tiene caso mostrar esto
        if self.el_usuario == 'OC':
            filtro2 = self.avance.loc[self.avance['Equipo']==equipos[pro]]
            filtro2 = filtro2.loc[:,['Programa','Porcentaje_de_conclusion']]
            tk.Label(self.frame1, 
                     text='Avance de revisión del equipo: ',
                     bg='#def3f6').pack()
            AV = tk.Label(self.frame1, text=filtro2.to_string(),
                          bg='#def3f6')
            AV.config(font=("Courier", 10))
            AV.pack()
        tk.Label(self.frame1,text='Fecha de consulta:'+ self.hoy.strftime("%d/%m/%Y"),
                 bg='#def3f6').pack()
    
    def gen_excel(self):
        #guardar frame
        fecha = self.fecha_d
        fecha = fecha.replace('/','-')
        fecha = fecha.replace(' ','-')
        fecha = fecha.replace(':','-')
        nombre = f'Turnos_{fecha}.csv'
        self.filtro.to_csv(nombre,index=False,encoding='latin1')
        messagebox.showinfo(
            message =f'Archivo guardado en carpeta donde está este ejecutable con el nombre {nombre}',
            title = 'Estado del archivo'
            )
    
    def consul1(self):
        br = self.NV.pack_slaves()
        for sl in br:
            sl.destroy()
        #crear el marco---propósitos estéticos
        self.frame1 = tk.Frame(self.NV, bg='#def3f6')
        self.frame1.pack()
        l1 = tk.Label(self.frame1, text="Distribución de carga de trabajo ",
                      fg='white',
                      bg='#0099cc')
        l1.pack(fill='x')
        tk.Label(self.frame1,text='Fecha de corte: '+self.fecha_d,bg='#def3f6').pack()
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
        # filtro = filtro.set_index('Turno')
        filtro = filtro.loc[filtro['Región'] == self.edd] if self.edd!='Todos' else filtro
        self.filtro = filtro.loc[:,['Turno','Proyecto',
                               'Módulo','Entidad',
                               'Registro','Estatus',
                               'Usuario','dias_en_OC',
                               'dias_en_rev_OC']]
        tk.Label(self.frame1, text="Los módulos que tiene pendientes el equipo que revisa tu proyecto son los siguientes: ",
                 bg='#def3f6').pack()
        # tab = tk.Text(self.frame1,width=100)
        # tab.insert(tk.INSERT, self.filtro.to_string())
        # tab.pack(pady=10)
        medidas = {'Turno':45,'Proyecto':60,
                   'Módulo':60,'Entidad':105,
                   'Registro':80,'Estatus':100,
                   'Usuario':125,'dias_en_OC':65,
                   'dias_en_rev_OC':95}
        arbol = ttk.Treeview(self.frame1)
        arbol['columns'] = list(self.filtro.columns)
        arbol.column('#0', width=0, stretch=tk.NO)
        for x in list(self.filtro.columns):
            arbol.column(x, width=medidas[x], anchor='center' )
            arbol.heading(x, text=x)
        for imm in range(len(self.filtro)):
            arbol.insert('', tk.END, values=(list(self.filtro.iloc[imm,:])))
        arbol.pack()
        boton_g = tk.Button(self.frame1,
                            text='Generar excel con estos datos',
                            command=self.gen_excel)
        boton_g.pack()
        self.A.append(1)
        li_des = tk.ttk.Combobox(self.frame1,
            state='readonly',
            textvariable=self.persona,
            values=list(self.filtro['Usuario'].unique())
            )
        li_des.pack()
        b3 = tk.Button(self.frame1, text ="Filtrar", command = self.f_per)
        b3.pack(pady=10) 
        tk.Label(self.frame1,text='Fecha de consulta:'+ self.hoy.strftime("%d/%m/%Y"),
                 bg='#def3f6').pack()
    
    def f_per(self):
        perso = self.persona.get()
        br = self.frame1.pack_slaves()
        for sl in br[2:]:
            sl.destroy()
        filtro1 = self.filtro.loc[self.filtro['Usuario']==perso]
        turnos = [i for i in range(1,len(list(filtro1['Usuario']))+1)]
        # filtro1['Turno'] = turnos
        filtro1.pop('Turno')
        filtro1.insert(loc=0,column='Turno',value=turnos)
        # filtro1 = filtro1.set_index('Turno')
        tk.Label(self.frame1, text="Los módulos que revisa la persona seleccionada son los siguientes: ",
                 bg='#def3f6').pack()
        # tab = tk.Text(self.frame1,width=100)
        # tab.insert(tk.INSERT, filtro1.to_string())
        # tab.pack()
        medidas = {'Turno':45,'Proyecto':60,
                   'Módulo':60,'Entidad':105,
                   'Registro':80,'Estatus':100,
                   'Usuario':125,'dias_en_OC':65,
                   'dias_en_rev_OC':95}
        arbol = ttk.Treeview(self.frame1)
        arbol['columns'] = list(filtro1.columns)
        arbol.column('#0', width=0, stretch=tk.NO)
        for x in list(filtro1.columns):
            arbol.column(x, width=medidas[x], anchor='center' )
            arbol.heading(x, text=x)
        for imm in range(len(filtro1)):
            arbol.insert('', tk.END, values=(list(filtro1.iloc[imm,:])))
        arbol.pack()
        #aquí condicional par que sino son de OC no se despliegue la informacion de desempeño
        if self.el_usuario == 'OC':
            excluir = ['LILIANA AVILA LOPEZ','NALLELY BECERRIL DAVILA',
                       'ALEXEI PRADEL HERNANDEZ']
            #comienza filtro para desplegar desempeño de responsable revisor o jefe
            if perso not in excluir:
                filtro2 = self.desemp[self.desemp['usuario']==perso].squeeze()
                # filtro2 = self.desemp.loc[self.desemp['usuario']==perso]
                tk.Label(self.frame1, text='Desempeño en revisiones',
                         bg='#def3f6').pack()
            if perso in excluir:
                filtro2 = self.jefes[self.jefes['usuario']==perso].squeeze()
                # filtro2 = self.jefes.loc[self.jefes['usuario']==perso]
                tk.Label(self.frame1, text='Desempeño en designaciones',
                         bg='#def3f6').pack()
            tk.Label(self.frame1, text=filtro2.to_string(),
                     bg='#def3f6').pack()
        #boton para regresar
        brt1 = tk.Button(self.frame1, text ="Regresar", command = self.consul1)
        brt1.pack()
        tk.Label(self.frame1,text='Fecha de consulta:'+ self.hoy.strftime("%d/%m/%Y"),
                 bg='#def3f6').pack()
        return
    
    @staticmethod
    def mod_text(texto):
        "funcion para modificartexto de estatus y reducirlo"

        if 'Revisión OC (1)' in texto or 'Pendiente' in texto: #se hace especificacion de revisión 1 porque es cuando por primera vez se manda a OC y no tiene a nadie asignado por su revisión, las demás revisiones en teoría ya tendrán a alguien asignado para esa labor
            res = 'Pendiente'
        elif 'FueraT' in texto:
            res = 'Retraso'
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
                    if df['Dias_inicio_RevOC'][c] < 0:
                        retrasos.append(df['Proyecto'][c])
            if df['Recuperado_firma_y_sello?'][c] == 'No':
                if type(df['Dias_fin_Recfirma'][c]) != str:
                    if df['Dias_fin_Recfirma'][c] < 0:
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