#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Se supone que el archivo con los offsets se encuentra en el mismo directorio
#que este script
##El formato del CSV a leer con los offsets es el siguiente:
## ----------------------------
## Axis,          M,       B
## Eje_Joint,  Valor_M, Valor_B
## ----------------------------
##Con cuantas filas se requiera segun actuadores y grados de libertad involucrados
##M y B son los parametros de la relacion lineal encontrada F = Eje*M + B

#Creando objeto con contenido del archivo

##Abriendo archivo
archivo = "offsets.csv"
f = open(archivo, 'rt')
##Obteniendo datos completos y cerrando archivo
reader = csv.reader(f)
filas = [r for r in reader]
f.close()

##Borrando indicadores y dejando solo datos
del filas[0]
for i,item in enumerate(filas):
    del filas[i][0]

#-------------------------------------------------------------------------------
#Interface

def getLineal():
    return filas    
