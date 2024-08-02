# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 11:59:55 2023

@author: AARON.RAMIREZ
"""

import matplotlib.pyplot as plt


def generar_imagenes(fechas,usuario,carga_dia,rev_dia,r5,r7):
    chek = corte(carga_dia)
    if chek:
        fechas = fechas[:-chek]
        carga_dia = carga_dia[:-chek]
        rev_dia = rev_dia[:-chek]
        r5 = r5[:-chek]
        r7 = r7[:-chek]
    fig, ax = plt.subplots()
    ax.bar(fechas,carga_dia,label=u"Carga por día")
    ax.bar(fechas,r5,label=u"Retraso +5 por día",color="orange")
    ax.bar(fechas,r7,label=u"Retraso +7 por día",color='red')
    ax.scatter(fechas,rev_dia,label=u"Revisiones por día",c='aqua')
    ax.set_title(usuario)
    ax.legend()
    ax.grid()
    if len(carga_dia)>25:
        fig.set_size_inches(11, 7)
    plt.xticks(rotation = 60)
    plt.xlabel('Fecha')
    plt.ylabel(u'Número de Revisiones')
    plt.savefig(f'Utilidades_app\{usuario}.png',dpi=100,bbox_inches="tight")
    # plt.show() #no hace falta mostrarlo
    plt.close()
    
def corte(revisar):
    "determinar si debe cortarse la grafica por nulas cargas de trabajo"
    for i,val in enumerate(reversed(revisar)):
        if val != 0:
            return i + 1
    return False