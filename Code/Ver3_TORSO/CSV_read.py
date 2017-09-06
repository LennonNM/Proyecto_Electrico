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
#archivo = os.path.join(archivo, "NaoPruebaA.csv")

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

###Eliminado numero de cuadro
for i,item in enumerate(filasCoordenadas) :
    del filasCoordenadas[i][0]

###Elimina columna de tiempos
tiempos = [None]*len(filasCoordenadas)
for i,item in enumerate(filasCoordenadas) :
    tiempos[i] = round(float(filasCoordenadas[i].pop(0)), 2)

###Ordenando coordenadas para generar lista de posiciones XYZ segun el orden de los actuadores
contXYZ = 0
contActuador = 1
basura = 0
trioXYZ = [0.0,0.0,0.0,0.0,0.0,0.0] #XYZ+rotacion
#trioXYZ.extend([0.0,0.0,0.0])
trioTemp = trioXYZ #Temporal por si se pierde la informacion del marcador
####Manejando cada actuador con su propia lista de posiciones
listaRArm = list()
listaRLeg = list()
listaLLeg = list()
listaLArm = list()
listaTorso = list()
listaHead = list()

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
            ### RArm
            if contActuador == 1 :
                listaRArm.append([(-1)*trioXYZ[0], trioXYZ[2], trioXYZ[1], 0.0, 0.0, 0.0])
                contActuador+=1
            ### RLeg
            elif contActuador == 2 :
                listaRLeg.append([trioXYZ[0], trioXYZ[2], trioXYZ[1], 0.0, 0.0, 0.0])
                contActuador+=1
            ### LLeg
            elif contActuador == 3 :
                listaLLeg.append([trioXYZ[0], trioXYZ[2], trioXYZ[1], 0.0, 0.0, 0.0])
                contActuador+=1
            ### LArm
            elif contActuador == 4 :
                listaLArm.append([trioXYZ[0], trioXYZ[2], trioXYZ[1], 0.0, 0.0, 0.0])
                contActuador+=1
            ### Torso
            elif contActuador == 5 :
                listaTorso.append([trioXYZ[0], trioXYZ[2], trioXYZ[1], 0.0, 0.0, 0.0])
                contActuador+=1
            ### Head
            elif contActuador == 6 :
                listaHead.append([trioXYZ[0], trioXYZ[2], trioXYZ[1], 0.0, 0.0, 0.0])
                contActuador=1

#Ajustando vectores respecto al TORSO
## RArm
for i, item in enumerate(listaRArm):
    for j, item2 in enumerate(listaRArm[j]):
        listaRArm[i][j] = round((listaRArm[i][j] - listaTorso[i][j]), 2)
## RLeg
for i, item in enumerate(listaRLeg):
    for j, item2 in enumerate(listaRLeg[j]):
        listaRLeg[i][j] = round((listaRLeg[i][j] - listaTorso[i][j]), 2)
## LLeg
for i, item in enumerate(listaLLeg):
    for j, item2 in enumerate(listaLLeg[j]):
        listaLLeg[i][j] = round((listaLLeg[i][j] - listaTorso[i][j]), 2)
## LArm
for i, item in enumerate(listaLArm):
    for j, item2 in enumerate(listaLArm[j]):
        listaLArm[i][j] = round((listaLArm[i][j] - listaTorso[i][j]), 2)
## TORSO
for i, item in enumerate(listaTorso):
    for j, item2 in enumerate(listaTorso[j]):
        listaTorso[i][j] = round((listaTorso[i][j] - listaTorso[i][j]), 2)
## Head
for i, item in enumerate(listaHead):
    for j, item2 in enumerate(listaHead[j]):
        listaHead[i][j] = round((listaHead[i][j] - listaTorso[i][j]), 2)

#En este punto ya se tienen los vectores de posiciones XYZ+rotacion para cada
#actuador independiente, en el orden segun el archivo CSV
##Generando Vector completo como lista de vectores para cada actuador
#coordenadasCompletas = [listaRArm, listaRLeg, listaLLeg, listaLArm, listaTorso, listaHead]
#coordenadasCompletas = [listaRArm, listaLArm, listaTorso, listaHead] #Sin piernas para usar FRAME.ROBOT
#coordenadasCompletas = [listaRArm, listaLArm, listaTorso] #Sin piernas ni cabeza
coordenadasCompletas = [listaRArm, listaRLeg, listaLLeg, listaLArm, listaHead] #Todo menos TORSO

#-------------------------------------------------------------------------------
#Interfaz de extraccion de datos
##Devuelve lista de actuadores en el CSV, con orden a usar
def getActuadores() :
    return actuadores

##Devuelve posiciones X,Y,Z en orden correspondiente a los actuadores obtenidos
def getCoordenadas():
    #return coordenadasFinales
    return coordenadasCompletas

##Devuelve lista de Tiempos del movimiento
#def getTiempos():
#    return tiemposFinales
