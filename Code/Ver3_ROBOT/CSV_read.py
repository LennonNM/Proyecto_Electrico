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
#Extrayendo informacion importante
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
actuador1 = list()
actuador2 = list()
actuador3 = list()
actuador4 = list()
actuador5 = list()
actuador6 = list()

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
                trioXYZ[contXYZ] = round(float(filasCoordenadas[i].pop(0)), 2)
                #trioTemp[contXYZ] = trioXYZ[contXYZ]
            contXYZ+=1
        elif contXYZ == 2 :
            if filasCoordenadas[i][0] == '' :
                trioXYZ[contXYZ] = trioTemp[contXYZ]
                filasCoordenadas.pop(0)
            else :
                trioXYZ[contXYZ] = round(float(filasCoordenadas[i].pop(0)), 2)
            contXYZ=0
                #trioTemp[contXYZ] = trioXYZ[contXYZ]
            #Se tienen XYZ+rot para un actuador en un cuadro especifico
            ### Z e Y estan invertidos en el marco de referencia del MoCap
            ### rotaciones en 0.0
            if contActuador == 1 :
                if listaActuadores[contActuador-1] == "RArm":
                    actuador1.append([trioXYZ[0]*mx_RArm + bx_RArm, trioXYZ[2]*my_RArm + by_RArm, trioXYZ[1]*mz_RArm + bz_RArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "RLeg":
                    actuador1.append([trioXYZ[0]*mx_RLeg + bx_RLeg, trioXYZ[2]*my_RLeg + by_RLeg, trioXYZ[1]*mz_RLeg + bz_RLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LLeg":
                    actuador1.append([trioXYZ[0]*mx_LLeg + bx_LLeg, trioXYZ[2]*my_LLeg + by_LLeg, trioXYZ[1]*mz_LLeg + bz_LLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LArm":
                    actuador1.append([trioXYZ[0]*mx_LArm + bx_LArm, trioXYZ[2]*my_LArm + by_LArm, trioXYZ[1]*mz_LArm + bz_LArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Torso":
                    actuador1.append([trioXYZ[0]*mx_Torso + bx_Torso, trioXYZ[2]*my_Torso + by_Torso, trioXYZ[1]*mz_Torso + bz_Torso, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Head":
                    actuador1.append([trioXYZ[0]*mx_Head + bx_Head, trioXYZ[2]*my_Head + by_Head, trioXYZ[1]*mz_Head + bz_Head, 0.0, 0.0, 0.0])
                contActuador+=1

            elif contActuador == 2 :
                if listaActuadores[contActuador-1] == "RArm":
                    actuador2.append([trioXYZ[0]*mx_RArm + bx_RArm, trioXYZ[2]*my_RArm + by_RArm, trioXYZ[1]*mz_RArm + bz_RArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "RLeg":
                    actuador2.append([trioXYZ[0]*mx_RLeg + bx_RLeg, trioXYZ[2]*my_RLeg + by_RLeg, trioXYZ[1]*mz_RLeg + bz_RLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LLeg":
                    actuador2.append([trioXYZ[0]*mx_LLeg + bx_LLeg, trioXYZ[2]*my_LLeg + by_LLeg, trioXYZ[1]*mz_LLeg + bz_LLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LArm":
                    actuador2.append([trioXYZ[0]*mx_LArm + bx_LArm, trioXYZ[2]*my_LArm + by_LArm, trioXYZ[1]*mz_LArm + bz_LArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Torso":
                    actuador2.append([trioXYZ[0]*mx_Torso + bx_Torso, trioXYZ[2]*my_Torso + by_Torso, trioXYZ[1]*mz_Torso + bz_Torso, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Head":
                    actuador2.append([trioXYZ[0]*mx_Head + bx_Head, trioXYZ[2]*my_Head + by_Head, trioXYZ[1]*mz_Head + bz_Head, 0.0, 0.0, 0.0])
                contActuador+=1

            elif contActuador == 3 :
                if listaActuadores[contActuador-1] == "RArm":
                    actuador3.append([trioXYZ[0]*mx_RArm + bx_RArm, trioXYZ[2]*my_RArm + by_RArm, trioXYZ[1]*mz_RArm + bz_RArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "RLeg":
                    actuador3.append([trioXYZ[0]*mx_RLeg + bx_RLeg, trioXYZ[2]*my_RLeg + by_RLeg, trioXYZ[1]*mz_RLeg + bz_RLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LLeg":
                    actuador3.append([trioXYZ[0]*mx_LLeg + bx_LLeg, trioXYZ[2]*my_LLeg + by_LLeg, trioXYZ[1]*mz_LLeg + bz_LLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LArm":
                    actuador3.append([trioXYZ[0]*mx_LArm + bx_LArm, trioXYZ[2]*my_LArm + by_LArm, trioXYZ[1]*mz_LArm + bz_LArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Torso":
                    actuador3.append([trioXYZ[0]*mx_Torso + bx_Torso, trioXYZ[2]*my_Torso + by_Torso, trioXYZ[1]*mz_Torso + bz_Torso, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Head":
                    actuador3.append([trioXYZ[0]*mx_Head + bx_Head, trioXYZ[2]*my_Head + by_Head, trioXYZ[1]*mz_Head + bz_Head, 0.0, 0.0, 0.0])
                contActuador+=1

            elif contActuador == 4 :
                if listaActuadores[contActuador-1] == "RArm":
                    actuador4.append([trioXYZ[0]*mx_RArm + bx_RArm, trioXYZ[2]*my_RArm + by_RArm, trioXYZ[1]*mz_RArm + bz_RArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "RLeg":
                    actuador4.append([trioXYZ[0]*mx_RLeg + bx_RLeg, trioXYZ[2]*my_RLeg + by_RLeg, trioXYZ[1]*mz_RLeg + bz_RLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LLeg":
                    actuador4.append([trioXYZ[0]*mx_LLeg + bx_LLeg, trioXYZ[2]*my_LLeg + by_LLeg, trioXYZ[1]*mz_LLeg + bz_LLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LArm":
                    actuador4.append([trioXYZ[0]*mx_LArm + bx_LArm, trioXYZ[2]*my_LArm + by_LArm, trioXYZ[1]*mz_LArm + bz_LArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Torso":
                    actuador4.append([trioXYZ[0]*mx_Torso + bx_Torso, trioXYZ[2]*my_Torso + by_Torso, trioXYZ[1]*mz_Torso + bz_Torso, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Head":
                    actuador4.append([trioXYZ[0]*mx_Head + bx_Head, trioXYZ[2]*my_Head + by_Head, trioXYZ[1]*mz_Head + bz_Head, 0.0, 0.0, 0.0])
                contActuador+=1

            elif contActuador == 5 :
                if listaActuadores[contActuador-1] == "RArm":
                    actuador5.append([trioXYZ[0]*mx_RArm + bx_RArm, trioXYZ[2]*my_RArm + by_RArm, trioXYZ[1]*mz_RArm + bz_RArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "RLeg":
                    actuador5.append([trioXYZ[0]*mx_RLeg + bx_RLeg, trioXYZ[2]*my_RLeg + by_RLeg, trioXYZ[1]*mz_RLeg + bz_RLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LLeg":
                    actuador5.append([trioXYZ[0]*mx_LLeg + bx_LLeg, trioXYZ[2]*my_LLeg + by_LLeg, trioXYZ[1]*mz_LLeg + bz_LLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LArm":
                    actuador5.append([trioXYZ[0]*mx_LArm + bx_LArm, trioXYZ[2]*my_LArm + by_LArm, trioXYZ[1]*mz_LArm + bz_LArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Torso":
                    actuador5.append([trioXYZ[0]*mx_Torso + bx_Torso, trioXYZ[2]*my_Torso + by_Torso, trioXYZ[1]*mz_Torso + bz_Torso, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Head":
                    actuador5.append([trioXYZ[0]*mx_Head + bx_Head, trioXYZ[2]*my_Head + by_Head, trioXYZ[1]*mz_Head + bz_Head, 0.0, 0.0, 0.0])
                contActuador+=1

            elif contActuador == 6 :
                if listaActuadores[contActuador-1] == "RArm":
                    actuador6.append([trioXYZ[0]*mx_RArm + bx_RArm, trioXYZ[2]*my_RArm + by_RArm, trioXYZ[1]*mz_RArm + bz_RArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "RLeg":
                    actuador6.append([trioXYZ[0]*mx_RLeg + bx_RLeg, trioXYZ[2]*my_RLeg + by_RLeg, trioXYZ[1]*mz_RLeg + bz_RLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LLeg":
                    actuador6.append([trioXYZ[0]*mx_LLeg + bx_LLeg, trioXYZ[2]*my_LLeg + by_LLeg, trioXYZ[1]*mz_LLeg + bz_LLeg, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "LArm":
                    actuador6.append([trioXYZ[0]*mx_LArm + bx_LArm, trioXYZ[2]*my_LArm + by_LArm, trioXYZ[1]*mz_LArm + bz_LArm, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Torso":
                    actuador6.append([trioXYZ[0]*mx_Torso + bx_Torso, trioXYZ[2]*my_Torso + by_Torso, trioXYZ[1]*mz_Torso + bz_Torso, 0.0, 0.0, 0.0])
                elif listaActuadores[contActuador-1] == "Head":
                    actuador6.append([trioXYZ[0]*mx_Head + bx_Head, trioXYZ[2]*my_Head + by_Head, trioXYZ[1]*mz_Head + bz_Head, 0.0, 0.0, 0.0])
                contActuador=1

#En este punto ya se tienen los vectores de posiciones XYZ+rotacion para cada
#actuador independiente, en el orden segun el archivo CSV
##Generando Vector completo como lista de vectores para cada actuador
coordenadasCompletas = [actuador3, actuador4, actuador5]

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
#def getTiempos():
#    return tiemposFinales
