import csv
import os
from itertools import islice
from os.path import dirname, abspath

#Obtencion de directorio base
rootDir = dirname(dirname(abspath(__file__)))

#Declarando directorio para abrir archivo CSV
archivo = os.path.join(rootDir, "Posiciones_Para_Datos/Frame_Robot/")
archivo = os.path.join(archivo, "pruebaA.csv")

#Creando objeto con contenido del archivo CSV
    #Abriendo archivo
f = open(archivo, 'rt')
    #Obteniendo datos completos
reader = csv.reader(f)
filasIniciales = [r for r in reader]
    #Filtrando coordenadas, estas se muestran hasta la fila 7
filasImportantes = islice(filasIniciales,7, None)
f.close()

def getColumna():
    return filasImportantes
