#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Se supone que el archivo con los offsets se encuentra en el mismo directorio
#que este script

#Creando objeto con contenido del archivo

##Abriendo archivo
archivo = "offsets.txt"
f = open(archivo, 'rt')
##Obteniendo datos completos y cerrando archivo
reader = csv.reader(f)
filas = [r for r in reader]
print filas[0][0]
f.close()
