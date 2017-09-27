#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath

#-------------------------------------------------------------------------------
#Coeficientes de Ajuste para valores del MoCap
## RArm
mx_RArm = -0.4
bx_RArm = 0.0
my_RArm = -1.5
by_RArm = -0.4
mz_RArm = 0.5
bz_RArm = -0.2
## RLeg
mx_RLeg = -0.4
bx_RLeg = 0.0
my_RLeg = -1.5
by_RLeg = -0.4
mz_RLeg = 0.5
bz_RLeg = -0.2
## LLeg
mx_LLeg = -0.4
bx_LLeg = 0.0
my_LLeg = -1.5
by_LLeg = -0.4
mz_LLeg = 0.5
bz_LLeg = -0.2
## LArm
mx_LArm = -0.5
bx_LArm = 0.05
my_LArm = 0.5
by_LArm = -0.05
mz_LArm = 0.4
bz_LArm = -0.1
## Torso
mx_Torso = -0.1
bx_Torso = 0.03
my_Torso = -0.1
by_Torso = -0.012
mz_Torso = 0.4
bz_Torso = -0.12
## Head
mx_Head = -0.4
bx_Head = 0.0
my_Head = -1.5
by_Head = -0.4
mz_Head = 0.5
bz_Head = -0.2
#-------------------------------------------------------------------------------
#Obtencion de directorio base
rootDir = dirname(dirname(abspath(__file__)))
#Declarando directorio para abrir archivo CSV
#archivo = os.path.join(rootDir, "Posiciones_Para_Datos/ROBOT_2/DATA/")
archivo = os.path.join(rootDir, "Posiciones_Para_Datos/PERSONA_ROBOT/DATA/")
archivo = os.path.join(archivo, "PruebaA_2.csv")

#Creando objeto con contenido del archivo CSV
##Abriendo archivo
f = open(archivo, 'rt')
##Obteniendo datos completos
reader = csv.reader(f)
filasIniciales = [r for r in reader]
f.close()

#-------------------------------------------------------------------------------
#Extrayendo informacion importante del archivo
##Obtencion del orden de aparicion de los marcadores(actuadores)
filasActuadores = filasIniciales[3]
###Remueve primeros dos espacios siempre en blanco
filasActuadores.remove('')
filasActuadores.remove('')
j = 0
listaActuadores = [None]*6
for i, item in enumerate(filasActuadores) :
    if i==0 or i==3 or i==6 or i==9 or i==12 or i==15:
        listaActuadores[j] = str(item)
        j+=1

ordenActuadores = [None]*6
for i,item in enumerate(listaActuadores):
    if item == "RArm":
        ordenActuadores[i] = 1
    elif item == "RLeg":
        ordenActuadores[i] = 2
    elif item == "LLeg":
        ordenActuadores[i] = 3
    elif item == "LArm":
        ordenActuadores[i] = 4
    elif item == "Torso":
        ordenActuadores[i] = 5
    elif item == "Head":
        ordenActuadores[i] = 6

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
            if listaActuadores[contActuador] == "RArm":
                actuador[contActuador].append([round(trioXYZ[0]*mx_RArm + bx_RArm, 2), round(trioXYZ[2]*my_RArm + by_RArm, 2), round(trioXYZ[1]*mz_RArm + bz_RArm, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "RLeg":
                actuador[contActuador].append([round(trioXYZ[0]*mx_RLeg + bx_RLeg, 2), round(trioXYZ[2]*my_RLeg + by_RLeg, 2), round(trioXYZ[1]*mz_RLeg + bz_RLeg, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "LLeg":
                actuador[contActuador].append([round(trioXYZ[0]*mx_LLeg + bx_LLeg, 2), round(trioXYZ[2]*my_LLeg + by_LLeg, 2), round(trioXYZ[1]*mz_LLeg + bz_LLeg, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "LArm":
                actuador[contActuador].append([round(trioXYZ[0]*mx_LArm + bx_LArm, 2), round(trioXYZ[2]*my_LArm + by_LArm, 2), round(trioXYZ[1]*mz_LArm + bz_LArm, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "Torso":
                actuador[contActuador].append([round(trioXYZ[0]*mx_Torso + bx_Torso, 2), round(trioXYZ[2]*my_Torso + by_Torso, 2), round(trioXYZ[1]*mz_Torso + bz_Torso, 2), 0.0, 0.0, 0.0])
            elif listaActuadores[contActuador] == "Head":
                actuador[contActuador].append([round(trioXYZ[0]*mx_Head + bx_Head, 2), round(trioXYZ[2]*my_Head + by_Head, 2), round(trioXYZ[1]*mz_Head + bz_Head, 2), 0.0, 0.0, 0.0])
            contActuador+=1
            if contActuador == 6:
                contActuador = 0

#En este punto ya se tienen los vectores de posiciones XYZ+rotacion para cada
#actuador independiente, en el orden segun el archivo CSV
##Generando Vector completo como lista de vectores para cada actuador
coordenadasCompletas = [actuador[2], actuador[3], actuador[4]]

#-------------------------------------------------------------------------------
#Interfaz de extraccion de datos
##Devuelve lista de actuadores en el CSV, con orden a usar
def getActuadores() :
    return listaActuadores

##Devuelve posiciones X,Y,Z en orden correspondiente a los actuadores obtenidos
def getCoordenadas():
    #return coordenadasFinales
    return coordenadasCompletas

##Devuelve lista de Tiempos del movimiento
def getTiempos():
    #Base de tiempo para cada vector de la animacion
    #Debe ser mayor a 20 ms (tiempo que dura en resolver el balance de cuerpo completo)
    #y dar al menos 30 ms entre cambios
    #coef depende de los cuadros por segundo de la animacion en Motive
    coef = 0.05
    listaTiempos = [None]*len(coordenadasCompletas)
    for i in range(len(coordenadasCompletas)):
        listaTiempos[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasCompletas[i]))]

    return listaTiempos
