# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 11:59:55 2023

@author: AARON.RAMIREZ
"""

import matplotlib.pyplot as plt


def generar_imagenes(fechas,usuario,carga_dia,rev_dia,r5,r7):
    fig, ax = plt.subplots()
    ax.bar(fechas,carga_dia,label=u"Carga por día")
    ax.stem(fechas,rev_dia,label=u"Revisiones por día",linefmt="aqua")
    ax.bar(fechas,r5,label=u"Retraso +5 por día",color="orange")
    ax.bar(fechas,r7,label=u"Retraso +7 por día",color='red')
    ax.set_title(usuario)
    ax.legend()
    ax.grid()
    if len(carga_dia)>25:
        fig.set_size_inches(12, 8)
    plt.xticks(rotation = 60)
    plt.xlabel('Fecha')
    plt.ylabel(u'Número de Revisiones')
    plt.savefig(f'Utilidades_app\{usuario}.png',dpi=100,bbox_inches="tight")
    plt.show()