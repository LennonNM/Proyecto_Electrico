#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Directorios con los datos de calibracion
##Root (../Code)
rootDir = dirname(dirname(abspath(__file__)))
##Archivos con posiciones del Nao
dirNaoA = os.path.join(rootDir, "Ver4/Cal/Nao/PosA.csv")
##Archivos con posiciones de la PERSONA_ROBOT
dirPersonaA = os.path.join(rootDir, "Ver4/Cal/Person/DATA/PruebaA.csv")

#Obteniendo contenidos
##Nao
fNao = open(dirNaoA, 'rt')
##Obteniendo datos completos y cerrando archivo
reader = csv.reader(fNao)
filasNao = [r for r in reader]
fNao.close()
##Persona
fPersona = open(dirPersonaA, 'rt')
##Obteniendo datos completos y cerrando archivo
reader = csv.reader(fPersona)
filasPersona = [r for r in reader]
fPersona.close()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Extraccion datos del Nao
##Datos numericos a partir de la fila #8
filasDatosNao = filasNao[7::]
##Eliminando columnas de Cuadro y Tiempos
for i,item in enumerate(filasDatosNao):
    del filasDatosNao[i][0]
    del filasDatosNao[i][0]
###Listas de coordenadas para cada actuador
RArmNao  = list()
RLegNao  = list()
LLegNao  = list()
LArmNao  = list()
TorsoNao = list()
HeadNao  = list()

contXYZ = 0
trioXYZ = [0.0,0.0,0.0]
contAct = 0

for i,item in enumerate(filasDatosNao):
    for contTrio in range(0,18):
        if contXYZ < 2:
            trioXYZ[contXYZ] = float(filasDatosNao[i].pop(0))
            contXYZ+=1
        elif contXYZ == 2:
            trioXYZ[contXYZ] = float(filasDatosNao[i].pop(0))
            contXYZ = 0

            if (contAct == 0):
                RArmNao.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif (contAct == 1):
                RLegNao.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif (contAct == 2):
                LLegNao.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif (contAct == 3):
                LArmNao.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif (contAct == 4):
                TorsoNao.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif (contAct == 5):
                HeadNao.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])

            if (contAct == 5):
                contAct = 0
            else:
                contAct+=1

#-------------------------------------------------------------------------------
#Extraccion datos de la persona
##Obtencion del orden de aparicion de los marcadores(actuadores)
filasActuadores = filasPersona[3]
###Remueve primeros dos espacios siempre en blanco
filasActuadores.remove('')
filasActuadores.remove('')
j = 0
listaActuadores = [None]*6 #Se trabaja con 6 marcadores
for i, item in enumerate(filasActuadores):
    #Se repite el nombre del marcador 3 veces(XYZ)
    if i==0 or i==3 or i==6 or i==9 or i==12 or i==15:
        listaActuadores[j] = str(item)
        j+=1

##Datos numericos a partir de la fila #8
filasDatosP = filasPersona[7::]
##Eliminando columnas de Cuadro y Tiempos
for i,item in enumerate(filasDatosP):
    del filasDatosP[i][0]
    del filasDatosP[i][0]
###Listas de coordenadas para cada actuador
RArmP  = list()
RLegP  = list()
LLegP  = list()
LArmP  = list()
TorsoP = list()
HeadP  = list()

contXYZ = 0
trioXYZ = [0.0,0.0,0.0]
contAct = 0

for i,item in enumerate(filasDatosP):
    for contTrio in range(0,18):
        if contXYZ < 2:
            trioXYZ[contXYZ] = float(filasDatosP[i].pop(0))
            contXYZ+=1
        elif contXYZ == 2:
            trioXYZ[contXYZ] = float(filasDatosP[i].pop(0))
            contXYZ = 0

            if listaActuadores[contAct] == "RArm":
                RArmP.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif listaActuadores[contAct] == "RLeg":
                RLegP.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif listaActuadores[contAct] == "LLeg":
                LLegP.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif listaActuadores[contAct] == "LArm":
                LArmP.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif listaActuadores[contAct] == "Torso":
                TorsoP.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
            elif listaActuadores[contAct] == "Head":
                HeadP.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])

            if (contAct == 5):
                contAct = 0
            else:
                contAct+=1

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Ajuste LINEAL entre los datos. Se considera una relacion Nao(x) = P(x)*M + B,
#donde M y B son un coeficiente de escalamiento y un corrimiento que relacionan
#los datos de las coordenadas segun el cuerpo de la persona, P(x), con los del
#Nao, Nao(x).
#
#Inicialmente los coeficientes tienen el valor de 1 y los corrimientos de 0
mx_RArm = 1
bx_RArm = 0
my_RArm = 1
by_RArm = 0
mz_RArm = 1
bz_RArm = 0
## RLeg
mx_RLeg = 1
bx_RLeg = 0
my_RLeg = 1
by_RLeg = 0
mz_RLeg = 1
bz_RLeg = 0
## LLeg
mx_LLeg = 1
bx_LLeg = 0
my_LLeg = 1
by_LLeg = 0
mz_LLeg = 1
bz_LLeg = 0
## LArm
mx_LArm = 1
bx_LArm = 0
my_LArm = 1
by_LArm = 0
mz_LArm = 1
bz_LArm = 0
## Torso
mx_Torso = 1
bx_Torso = 0
my_Torso = 1
by_Torso = 0
mz_Torso = 1
bz_Torso = 0
## Head
mx_Head = 1
bx_Head = 0
my_Head = 1
by_Head = 0
mz_Head = 1
bz_Head = 0

#Lista de coordenadas resultantes de las modificaciones