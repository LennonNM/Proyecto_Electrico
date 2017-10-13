#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath

import Offset_read #Lectura parametros de ajuste
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Coeficientes de Ajuste para valores del MoCap, considerando relacion lineal
#entre datos del MoCap y datos del Nao
##Lectura del archivo con los parametros
listaOffsets = Offset_read.getLineal()
## RArm
mx_RArm = float(listaOffsets[0][0])
bx_RArm = float(listaOffsets[0][1])
my_RArm = float(listaOffsets[1][0])
by_RArm = float(listaOffsets[1][1])
mz_RArm = float(listaOffsets[2][0])
bz_RArm = float(listaOffsets[2][1])
## RLeg
mx_RLeg = float(listaOffsets[3][0])
bx_RLeg = float(listaOffsets[3][1])
my_RLeg = float(listaOffsets[4][0])
by_RLeg = float(listaOffsets[4][1])
mz_RLeg = float(listaOffsets[5][0])
bz_RLeg = float(listaOffsets[5][1])
## LLeg
mx_LLeg = float(listaOffsets[6][0])
bx_LLeg = float(listaOffsets[6][1])
my_LLeg = float(listaOffsets[7][0])
by_LLeg = float(listaOffsets[7][1])
mz_LLeg = float(listaOffsets[8][0])
bz_LLeg = float(listaOffsets[8][1])
## LArm
mx_LArm = float(listaOffsets[9][0])
bx_LArm = float(listaOffsets[9][1])
my_LArm = float(listaOffsets[10][0])
by_LArm = float(listaOffsets[10][1])
mz_LArm = float(listaOffsets[11][0])
bz_LArm = float(listaOffsets[11][1])
## Torso
mx_Torso = float(listaOffsets[12][0])
bx_Torso = float(listaOffsets[12][1])
my_Torso = float(listaOffsets[13][0])
by_Torso = float(listaOffsets[13][1])
mz_Torso = float(listaOffsets[14][0])
bz_Torso = float(listaOffsets[14][1])
## Head
mx_Head = float(listaOffsets[15][0])
bx_Head = float(listaOffsets[15][1])
my_Head = float(listaOffsets[16][0])
by_Head = float(listaOffsets[16][1])
mz_Head = float(listaOffsets[17][0])
bz_Head = float(listaOffsets[17][1])
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Obtencion de directorio base
rootDir = dirname(dirname(abspath(__file__)))
#Declarando directorio para abrir archivo CSV
#archivo = os.path.join(rootDir, "Posiciones_Para_Datos/ROBOT_2/DATA/")
archivo = os.path.join(rootDir, "Posiciones_Para_Datos/PERSONA_ROBOT/DATA/")
#Nombre del archivo CSV a leer
archivo = os.path.join(archivo, "PruebaA.csv")

#Creando objeto con contenido del archivo CSV
##Abriendo archivo
f = open(archivo, 'rt')
##Obteniendo datos completos y cerrando archivo
reader = csv.reader(f)
filasIniciales = [r for r in reader]
f.close()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Extrayendo informacion importante del archivo

##Obtencion del orden de aparicion de los marcadores(actuadores)
filasActuadores = filasIniciales[3]
###Remueve primeros dos espacios siempre en blanco
filasActuadores.remove('')
filasActuadores.remove('')
j = 0
listaActuadores = [None]*6 #Se trabaja con 6 marcadores
for i, item in enumerate(filasActuadores) :
    #Se repite el nombre del marcador 3 veces(XYZ)
    if i==0 or i==3 or i==6 or i==9 or i==12 or i==15:
        listaActuadores[j] = str(item)
        j+=1
#print listaActuadores

#-------------------------------------------------------------------------------
##Obtencion datos de posiciones, estas se muestran hasta la fila 7 (iniciando cuenta en 0)
##incluyen numero de cuadro, tiempo en segundos y coordenadas XYZ en orden segun los
##actuadores obtenidos
filasCoordenadas = filasIniciales[7::]

###Eliminado numero de cuadro
for i,item in enumerate(filasCoordenadas) :
    del filasCoordenadas[i][0]

###Elimina columna de tiempos
tiempos = [None]*len(filasCoordenadas)
for i,item in enumerate(filasCoordenadas) :
    tiempos[i] = round(float(filasCoordenadas[i].pop(0)), 2)

###Ordenando coordenadas para generar lista de posiciones XYZ segun el orden de los actuadores
contXYZ = 0
contActuador = 0
basura = 0
trioXYZ = [0.0,0.0,0.0,0.0,0.0,0.0] #XYZ+rotacion
#trioXYZ.extend([0.0,0.0,0.0])
trioTemp = trioXYZ #Temporal por si se pierde la informacion del marcador
####Manejando cada actuador con su propia lista de posiciones
actuador = [None]*6
for i in range(len(listaActuadores)):
    actuador[i] = list()

for i, item in enumerate(filasCoordenadas) :
    #contActuador = 1 #Reinicia contador de actuador cada vez que carga fila nueva
    for contTrio in range(0,18) : #3 ejes * 6 actuadores
        if contXYZ < 2 :
            if filasCoordenadas[i][0] == '' : #Revisa si se perdio el marcador
                #En caso de posicion faltante se pasa el valor obtenidos
                #del cuadro anterior con posicion valida
                basura = filasCoordenadas.pop(0) #Saca valor vacio de la lista
                trioXYZ[contXYZ] = trioTemp[contXYZ]
            else :
                trioXYZ[contXYZ] = float(filasCoordenadas[i].pop(0))
                #trioTemp[contXYZ] = trioXYZ[contXYZ]
            contXYZ+=1
        elif contXYZ == 2 :
            if filasCoordenadas[i][0] == '' :
                trioXYZ[contXYZ] = trioTemp[contXYZ]
                filasCoordenadas.pop(0)
            else :
                trioXYZ[contXYZ] = float(filasCoordenadas[i].pop(0))
            contXYZ=0
                #trioTemp[contXYZ] = trioXYZ[contXYZ]
            #Se tienen XYZ+rot para un actuador en un cuadro especifico
            ### Z e Y estan invertidos en el marco de referencia del MoCap
            ### rotaciones en 0.0
            ####Sin importar el orden de los actuadores aqui se acomodan en el
            ####orden preferente
            if listaActuadores[contActuador] == "RArm":
                actuador[0].append([round(trioXYZ[0]*mx_RArm + bx_RArm, 2), round(trioXYZ[2]*my_RArm + by_RArm, 2), round(trioXYZ[1]*mz_RArm + bz_RArm, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "RLeg":
                actuador[1].append([round(trioXYZ[0]*mx_RLeg + bx_RLeg, 2), round(trioXYZ[2]*my_RLeg + by_RLeg, 2), round(trioXYZ[1]*mz_RLeg + bz_RLeg, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "LLeg":
                actuador[2].append([round(trioXYZ[0]*mx_LLeg + bx_LLeg, 2), round(trioXYZ[2]*my_LLeg + by_LLeg, 2), round(trioXYZ[1]*mz_LLeg + bz_LLeg, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "LArm":
                actuador[3].append([round(trioXYZ[0]*mx_LArm + bx_LArm, 2), round(trioXYZ[2]*my_LArm + by_LArm, 2), round(trioXYZ[1]*mz_LArm + bz_LArm, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "Torso":
                actuador[4].append([round(trioXYZ[0]*mx_Torso + bx_Torso, 2), round(trioXYZ[2]*my_Torso + by_Torso, 2), round(trioXYZ[1]*mz_Torso + bz_Torso, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "Head":
                actuador[5].append([round(trioXYZ[0]*mx_Head + bx_Head, 2), round(trioXYZ[2]*my_Head + by_Head, 2), round(trioXYZ[1]*mz_Head + bz_Head, 2), 0.0, 0.0, 0.0])
            contActuador+=1
            if contActuador == 6:
                contActuador = 0

#En este punto ya se tienen los vectores de posiciones XYZ+rotacion para cada
#actuador independiente, en el orden segun el archivo CSV
##Generando Vector completo como lista de vectores para cada actuador
coordenadasCompletasROBOT = [actuador[0], actuador[3], actuador[4]]

##Si los datos obtenidos vienen con referencia al TORSO no es necesario este
##proceso
listaDeActuadores = coordenadasCompletasROBOT
## RArm
for i, item in enumerate(listaDeActuadores[0]):
    for j, item2 in enumerate(listaDeActuadores[0][j]):
        listaDeActuadores[0][i][j] = round((listaDeActuadores[0][i][j] - listaDeActuadores[4][i][j]), 2)
## RLeg
for i, item in enumerate(listaDeActuadores[1]):
    for j, item2 in enumerate(listaDeActuadores[1][j]):
        listaDeActuadores[1][i][j] = round((listaDeActuadores[1][i][j] - listaDeActuadores[4][i][j]), 2)
## LLeg
for i, item in enumerate(listaDeActuadores[2]):
    for j, item2 in enumerate(listaDeActuadores[2][j]):
        listaDeActuadores[2][i][j] = round((listaDeActuadores[2][i][j] - listaDeActuadores[4][i][j]), 2)
## LArm
for i, item in enumerate(listaDeActuadores[3]):
    for j, item2 in enumerate(listaDeActuadores[3][j]):
        listaDeActuadores[3][i][j] = round((listaDeActuadores[3][i][j] - listaDeActuadores[4][i][j]), 2)
## TORSO
for i, item in enumerate(listaDeActuadores[4]):
    for j, item2 in enumerate(listaDeActuadores[4][j]):
        listaDeActuadores[4][i][j] = round((listaDeActuadores[4][i][j] - listaDeActuadores[4][i][j]), 2)
## Head
for i, item in enumerate(listaDeActuadores[5]):
    for j, item2 in enumerate(listaDeActuadores[5][j]):
        listaDeActuadores[5][i][j] = round((listaDeActuadores[5][i][j] - listaDeActuadores[5][i][j]), 2)
#Recibe datos respecto al TORSO
coordenadasCompletasTORSO = listaDeActuadores
print actuador[0][1]
print coordenadasCompletasTORSO[0][1]

#-------------------------------------------------------------------------------
#Base de tiempo para cada vector de la animacion
##Debe ser mayor a 20 ms (tiempo que dura en resolver el balance de cuerpo completo)
##y dar al menos 30 ms entre cambios
##coef depende de los cuadros por segundo de la animacion en Motive en el momento
##de exportar los datos
coef = 0.05
listaTiempos = [None]*len(coordenadasCompletasROBOT)
for i in range(len(coordenadasCompletasROBOT)):
    listaTiempos[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasCompletasROBOT[i]))]
    #Se maneja un vector de tiempos independiente para cada actuador, con longitud
    #correspondiente a la lista con coordenadas respectivo al actuador

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Interfaz de extraccion de datos
##Devuelve lista de actuadores en el CSV, con orden a usar, si no se quiere el
##orden preferente
def getActuadores() :
    return listaActuadores

##Devuelve posiciones X,Y,Z+rot en orden correspondiente a los actuadores obtenidos
##segun el marco ROBOT
def getCoordenadasROBOT():
    return coordenadasCompletasROBOT

##Devuelve posiciones X,Y,Z+rot en orden correspondiente a los actuadores obtenidos
##segun el marco ROBOT
def getCoordenadasTORSO():
    return coordenadasCompletasTORSO

##Devuelve lista de Tiempos del movimiento
def getTiempos():
    return listaTiempos
