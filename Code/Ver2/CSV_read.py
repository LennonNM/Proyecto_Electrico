#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath

#-------------------------------------------------------------------------------
#Obtencion de directorio base
rootDir = dirname(dirname(abspath(__file__)))
#Declarando directorio para abrir archivo CSV
archivo = os.path.join(rootDir, "Posiciones_Para_Datos/Frame_Robot/")
archivo = os.path.join(archivo, "pruebaA.csv")

#Creando objeto con contenido del archivo CSV
##Abriendo archivo
f = open(archivo, 'rt')
##Obteniendo datos completos
reader = csv.reader(f)
filasIniciales = [r for r in reader]
f.close()

#-------------------------------------------------------------------------------
#Extrayendo informacion importante
##Obtencion del orden de aparicion de los marcadores(actuadores)
filasActuadores = filasIniciales[3]
###Remueve primeros dos espacios siempre en blanco
filasActuadores.remove('')
filasActuadores.remove('')
j = 0
actuadores = [None]*6
for i, item in enumerate(filasActuadores) :
    if i==0 or i==3 or i==6 or i==9 or i==12 or i==15:
        marcador = str(item)
        actuadores[j] = marcador[10::]
        j+=1

##Obtencion datos de posiciones, estas se muestran hasta la fila 7 (iniciando cuenta en 0)
##incluyen numero de cuadro, tiempo en segundos y coordenadas XYZ en orden segun los
##actuadores obtenidos
filasCoordenadas = filasIniciales[7::]

###Eliminado del elemento numero de cuadro
for i,item in enumerate(filasCoordenadas) :
    del filasCoordenadas[i][0]

###Generando lista de tiempos
tiempos = [None]*len(filasCoordenadas)
for i,item in enumerate(filasCoordenadas) :
    tiempos[i] = float(filasCoordenadas[i].pop(0))

###Ordenando coordenadas para generar lista de posiciones XYZ segun el orden de los actuadores
contXYZ = 0
contActuador = 1
trioXYZ = [None]*3 #XYZ+rotacion
trioXYZ.extend([0.0,0.0,0.0])
trioTemp = trioXYZ #Temporal por si se pierde la informacion del marcador
####Manejando cada actuador con su propia lista de posiciones
actuador1 = list()
actuador2 = list()
actuador3 = list()
actuador4 = list()
actuador5 = list()
actuador6 = list()
for i, item in enumerate(filasCoordenadas) :
    contActuador = 1 #Reinicia contador de actuador cada vez que carga fila nueva
    for contTrio in range(0,18) : #3 ejes * 6 actuadores
        if contXYZ < 2 :
            if filasCoordenadas[i][0] == '' : #Revisa si se perdio el marcador
                #En caso de posicion faltante se pasa el valor obtenidos
                #del cuadro anterior con posicion valida
                trioXYZ[contXYZ] = trioTemp[contXYZ]
            else :
                trioXYZ[contXYZ] = float(filasCoordenadas[i].pop(0))
                trioTemp[contXYZ] = trioXYZ[contXYZ]
                contXYZ+=1
        elif contXYZ == 2 :
            if filasCoordenadas[i][0] == '' :
                trioXYZ[contXYZ] = trioTemp[contXYZ]
            else :
                trioXYZ[contXYZ] = float(filasCoordenadas[i].pop(0))
                contXYZ=0
                trioTemp[contXYZ] = trioXYZ[contXYZ]
            #Se tienen XYZ+rot para un actuador en un cuadro especifico
            if contActuador == 1 :
                actuador1.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                contActuador+=1
            elif contActuador == 2 :
                actuador2.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                contActuador+=1
            elif contActuador == 3 :
                actuador3.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                contActuador+=1
            elif contActuador == 4 :
                actuador4.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                contActuador+=1
            elif contActuador == 5 :
                actuador5.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                contActuador+=1
            elif contActuador == 6 :
                actuador6.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                contActuador=1

print actuador6

#print len(coordenadas[0])

#-------------------------------------------------------------------------------
#Interfaz de extraccion de datos
##Devuelve lista de actuadores en el CSV, con orden a usar
def getActuadores() :
    return actuadores

##Devuelve posiciones X,Y,Z en orden correspondiente a los actuadores obtenidos
def getCoordenadas():
    return filasCoordenadas

##Devuelve lista de Tiempos del movimiento
def getCoordenadas():
    return tiempos
