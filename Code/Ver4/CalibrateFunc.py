#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Incluye las funciones a utilizar para el proceso de calibracion definido en
#Calibrate.py
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import csv
import os
import numpy as np
from scipy.interpolate import *
from itertools import islice
from os.path import dirname, abspath
from copy import deepcopy

#Custom
import ErrorFunc as error
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Globales
###Listas de coordenadas para cada actuador
RArmPCal  = list()
RLegPCal  = list()
LLegPCal  = list()
LArmPCal  = list()
TorsoPCal = list()
HeadPCal  = list()
###Listas de coordenadas para cada actuador
RArmNaoCal  = list()
RLegNaoCal  = list()
LLegNaoCal  = list()
LArmNaoCal  = list()
TorsoNaoCal = list()
HeadNaoCal  = list()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Recibe archivos con las grabaciones de calibracion de una pose, del NAO y de
#la persona. Devuelve listas individuales para cada actuador del NAO y de la
#persona.
def setCalData(archNao, archP):
    #Limpia listas por usos previos
    RArmPCal[:] = []
    RLegPCal[:] = []
    LLegPCal[:] = []
    LArmPCal[:] = []
    TorsoPCal[:] = []
    HeadPCal[:] = []
    RArmNaoCal[:] = []
    RLegNaoCal[:] = []
    LLegNaoCal[:] = []
    LArmNaoCal[:] = []
    TorsoNaoCal[:] = []
    HeadNaoCal[:] = []

    #Directorios con los datos de calibracion
    ##Root (../Code)
    rootDir = dirname(dirname(abspath(__file__)))
    ##Archivos con posiciones del Nao
    dirNao = os.path.join(rootDir, "Ver4/Cal/NAO/")
    dirNao = os.path.join(dirNao, archNao)
    ##Archivos con posiciones de la PERSONA_ROBOT
    dirPersona = os.path.join(rootDir, "Ver4/Cal/Human/")
    dirPersona = os.path.join(dirPersona, archP)

    #Obteniendo contenidos
    ##Nao
    try:
        fNao = open(dirNao, 'rt')
    except Exception,e:
        error.abort("is not a valid directory", archNao, "Calibrate")

    ##Obteniendo datos completos y cerrando archivo
    reader = csv.reader(fNao)
    filasNao = [r for r in reader]
    fNao.close()
    ##Persona
    try:
        fPersona = open(dirPersona, 'rt')
    except Exception,e:
        error.abort("is not a valid directory", archP, "Calibrate")
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
                    RArmNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                elif (contAct == 1):
                    RLegNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                elif (contAct == 2):
                    LLegNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                elif (contAct == 3):
                    LArmNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                elif (contAct == 4):
                    TorsoNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])
                elif (contAct == 5):
                    HeadNaoCal.append([trioXYZ[0], trioXYZ[1], trioXYZ[2]])

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
                    RArmPCal.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "RLeg":
                    RLegPCal.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "LLeg":
                    LLegPCal.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "LArm":
                    LArmPCal.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "Torso":
                    TorsoPCal.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])
                elif listaActuadores[contAct] == "Head":
                    HeadPCal.append([-1*trioXYZ[0], trioXYZ[2], trioXYZ[1]])

                if (contAct == 5):
                    contAct = 0
                else:
                    contAct+=1

    return RArmNaoCal,RLegNaoCal,LLegNaoCal,LArmNaoCal,TorsoNaoCal,HeadNaoCal,RArmPCal,RLegPCal,LLegPCal,LArmPCal,TorsoPCal,HeadPCal

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Realiza la regresion polinomial deseada para encontrar los terminos del ajuste
#Recibe la lista con datos de coordenadas XYZ para un solo actuador, del NAO
#y de la persona, asi como el grado polinomial.
#Devuelve una lista con los terminos del ajuste polinomial para X, Y y Z del
#actuador recibido
def getTerms(listNAO, listP, degree):
    naoX = list()
    naoY = list()
    naoZ = list()
    pX = list()
    pY = list()
    pZ = list()
    pl = [None]*3

	#Se ocupa que ambos arreglos a comparar tengan la misma cantidad de datos,
	#por lo que se utiliza la longitud mas corta (suele ser la de datos del NAO)
    n = min(len(listNAO),len(listP))

	#Separa datos X, Y y Z en grupos
    for i in range(n):
        naoX.append(listNAO[i][0])
        naoY.append(listNAO[i][1])
        naoZ.append(listNAO[i][2])
        pX.append(listP[i][0])
        pY.append(listP[i][1])
        pZ.append(listP[i][2])

	#Obtiene los terminos de la relacion polinomial con grado 'degree'
	#Por defecto se calcula regresion lineal

    pl[0] = list(np.polyfit(pX,naoX,degree))
    pl[1] = list(np.polyfit(pY,naoY,degree))
    pl[2] = list(np.polyfit(pZ,naoZ,degree))

    return pl

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Obtiene el promedio de los terminos usados en todas las grabaciones bases
#para la calibracion, para un mismo actuador
#Recibe una lista con los terminos polinomiales de cada grabacion utilizada
#para la calibracion. devuelve el promedio del ajuste polinomial para X, Y y Z
def setAdjustAct(listTerms):
    n = len(listTerms[0][0])
    listX = list()
    listY = list()
    listZ = list()
    termsX = [[] for x in range(n)]
    termsY = [[] for x in range(n)]
    termsZ = [[] for x in range(n)]
    promX = [[] for x in range(n)]
    promY = [[] for x in range(n)]
    promZ = [[] for x in range(n)]

    ##Separa datos en grupos de X, Y y Z
    for item in listTerms:
        listX.append(item[0])
        listY.append(item[1])
        listZ.append(item[2])

    ##Separa para X,Y y Z en listas de terminos, segun la cantidad de terminos
    ##definidos por la relacion polinomial utilizada
    for item in listX:
        for i in range(len(item)):
            termsX[i].append(item[i])
    for item in listY:
        for i in range(len(item)):
            termsY[i].append(item[i])
    for item in listZ:
        for i in range(len(item)):
            termsZ[i].append(item[i])

    ##Obtiene el promedio de cada termino para X, Y y Z
    for i in range(n):
        promX[i] = np.mean(termsX[i])
    for i in range(n):
        promY[i] = np.mean(termsY[i])
    for i in range(n):
        promZ[i] = np.mean(termsZ[i])

    ##Retorna los nuevos terminos a utilizar para las relaciones polinomiales
    ##de X, Y y Z para un solo actuador
    return promX,promY,promZ
