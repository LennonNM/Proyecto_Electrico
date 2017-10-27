#Imports
import csv
import os
import numpy as np
from itertools import islice
from os.path import dirname, abspath
from copy import deepcopy
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
###Listas de coordenadas para cada actuador
RArmP  = list()
RLegP  = list()
LLegP  = list()
LArmP  = list()
TorsoP = list()
HeadP  = list()
###Listas de coordenadas para cada actuador
RArmNao  = list()
RLegNao  = list()
LLegNao  = list()
LArmNao  = list()
TorsoNao = list()
HeadNao  = list()

##Gets data lists from Nao and person
def getCalData():
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
    #NOTA: ejes Y y Z estan invertidos
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
                    RArmP.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "RLeg":
                    RLegP.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "LLeg":
                    LLegP.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "LArm":
                    LArmP.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "Torso":
                    TorsoP.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "Head":
                    HeadP.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])

                if (contAct == 5):
                    contAct = 0
                else:
                    contAct+=1
    return RArmNao,RLegNao,LLegNao,LArmNao,TorsoNao,HeadNao,RArmP,RLegP,LLegP,LArmP,TorsoP,HeadP
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def startCalibrate():
    naoX = list()
    naoY = list()
    naoZ = list()
    pX = list()
    pY = list()
    pZ = list()
    ArmNao = np.array(RArmNao)
    ArmP   = np.array(RArmP)
    n      = min(len(ArmNao),len(ArmP))

    ##Obtencion de media
    meanNao = [0.0,0.0,0.0]
    meanP   = [0.0,0.0,0.0]
    for i in range(n):
        naoX.append(ArmNao[i][0])
        naoY.append(ArmNao[i][1])
        naoZ.append(ArmNao[i][2])
        pX.append(ArmP[i][0])
        pY.append(ArmP[i][1])
        pZ.append(ArmP[i][2])

    meanNao[0] = np.mean(naoX)
    meanP[0]   = np.mean(pX)
    meanNao[1] = np.mean(naoY)
    meanP[1]   = np.mean(pY)
    meanNao[2] = np.mean(naoZ)
    meanP[2]   = np.mean(pZ)

    ##Obtencion varianza y covarianza
    varNao = [0.0,0.0,0.0]
    cov = [0.0,0.0,0.0]

    cov[0] = np.sum(pX*naoX - n*meanP[0]*meanNao[0])
    cov[1] = np.sum(pX*naoX - n*meanP[1]*meanNao[1])
    cov[2] = np.sum(pX*naoX - n*meanP[2]*meanNao[2])

    varNao[0] = np.sum(naoX*naoX - n*meanNao[0]*meanNao[0])
    varNao[1] = np.sum(naoX*naoX - n*meanNao[1]*meanNao[1])
    varNao[2] = np.sum(naoX*naoX - n*meanNao[2]*meanNao[2])

    ##Estimacion de los coeficientes de la relacion lineal
    m = [0.0,0.0,0.0]
    b = [0.0,0.0,0.0]

    for i in range(len(m)):
        m[i] = cov[i]/varNao[i]
    for i in range(len(b)):
        b[i] = meanP[i]-m[i]*meanNao[i]




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
