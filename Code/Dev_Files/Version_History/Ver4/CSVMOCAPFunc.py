#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Incluye funciones para la lectura del archivo CSV y ajuste a los datos de la
#grabacion del movimiento capturado en MoCap que se quiere ejecutar.
##
#Recibe los terminos del ajuste de calibracion del archivo CSV
#.../Cal/Offsets/offsets.csv. Devuelve listas con los actuadores y vectores de
#coordenadas y tiempos, Las coordenadas pueden ser obtenidas en los marcos de
#referencia ROBOT y TORSO, segun se solicite.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Imports
import csv
import os
from itertools import islice
from os.path import dirname, abspath
from copy import deepcopy

##Custom
import OffsetFileFunc as offset
import ErrorFunc as error

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Globales
coordenadasArriba = list()
coordenadasCompletasROBOT = list()
coordenadasCompletasTORSO = list()

#Inicia el procesamiento de los archivos CSV necesarios para el ajuste de datos
#Recibe como parametro el nombre del archivo CSV con las coordenadas a leer
def startAdjustData(nombreArchivo):
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Starting coordinates adjustment for", nombreArchivo
    #Coeficientes de Ajuste para valores del MoCap, considerando relacion lineal
    #entre datos del MoCap y datos del Nao
    ##Lectura del archivo con los parametros
    try:
        listaOffsets,degree = offset.getOffsets()
    except Exception,e:
        error.abort("Failed to get offsets from file offset.csv, check file", "CSVMOCAPFunc")

    offRArm  = [[] for x in range(3)]
    offRLeg  = [[] for x in range(3)]
    offLLeg  = [[] for x in range(3)]
    offLArm  = [[] for x in range(3)]
    offTorso = [[] for x in range(3)]
    offHead  = [[] for x in range(3)]

    #RArm
    for j in range(degree+1):
        offRArm[0].append(round(float(listaOffsets[0][j]),4))
        offRArm[1].append(round(float(listaOffsets[1][j]),4))
        offRArm[2].append(round(float(listaOffsets[2][j]),4))
    #RLeg
    for j in range(degree+1):
        offRLeg[0].append(round(float(listaOffsets[3][j]),4))
        offRLeg[1].append(round(float(listaOffsets[4][j]),4))
        offRLeg[2].append(round(float(listaOffsets[5][j]),4))
    #LLeg
    for j in range(degree+1):
        offLLeg[0].append(round(float(listaOffsets[6][j]),4))
        offLLeg[1].append(round(float(listaOffsets[7][j]),4))
        offLLeg[2].append(round(float(listaOffsets[8][j]),4))

    #LArm
    for j in range(degree+1):
        offLArm[0].append(round(float(listaOffsets[9][j]),4))
        offLArm[1].append(round(float(listaOffsets[10][j]),4))
        offLArm[2].append(round(float(listaOffsets[11][j]),4))

    #Torso
    for j in range(degree+1):
        offTorso[0].append(round(float(listaOffsets[12][j]),4))
        offTorso[1].append(round(float(listaOffsets[13][j]),4))
        offTorso[2].append(round(float(listaOffsets[14][j]),4))

    #Head
    for j in range(degree+1):
        offHead[0].append(round(float(listaOffsets[15][j]),4))
        offHead[1].append(round(float(listaOffsets[16][j]),4))
        offHead[2].append(round(float(listaOffsets[17][j]),4))

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    print "    Reading choreography file"
    #Obtencion de directorio base
    rootDir = dirname(dirname(abspath(__file__)))
    #Declarando directorio para abrir archivo CSV
    ##Nombre del archivo CSV a leer
    archivo = os.path.join(rootDir, "Ver4/Choreography/")
    archivo = os.path.join(archivo, nombreArchivo)

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
    for i, item in enumerate(filasActuadores):
        #Se repite el nombre del marcador 3 veces(XYZ)
        if i==0 or i==3 or i==6 or i==9 or i==12 or i==15:
            listaActuadores[j] = str(item)
            j+=1

    #-------------------------------------------------------------------------------
    ##Obtencion datos de posiciones, estas se muestran hasta la fila #8 del archivo
    ##incluyen numero de cuadro, tiempo en segundos y coordenadas XYZ en orden segun los
    ##actuadores obtenidos
    filasCoordenadas = filasIniciales[7::]

    ###Eliminado numero de cuadro, no se utiliza
    for i,item in enumerate(filasCoordenadas):
        del filasCoordenadas[i][0]

    ###Elimina columna de tiempos, y a su vez extrae los tiempos en caso de usarse
    ###estos en vez de la lista generada mas adelante por defecto
    tiempos = [None]*len(filasCoordenadas)
    for i,item in enumerate(filasCoordenadas):
        tiempos[i] = round(float(filasCoordenadas[i].pop(0)), 2)

    print "    Generating new coordinates"
    ###Ordenando coordenadas para generar lista de posiciones XYZ segun el orden de los actuadores
    contXYZ = 0
    contActuador = 0
    basura = 0
    trioXYZ = [0.0,0.0,0.0,0.0,0.0,0.0] #XYZ+rotacion
    trioTemp = trioXYZ #Temporal por si se pierde la informacion del marcador
    ####Manejando cada actuador con su propia lista de posiciones
    actuador = [None]*6
    for i in range(len(listaActuadores)):
        actuador[i] = list()

    try:
        for i, item in enumerate(filasCoordenadas):
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
                    ### Rotaciones en 0.0, X*-1
                    ####Sin importar el orden de los actuadores en el archivo aqui
                    ####se acomodan en el orden preferente y se aplica la correccion
                    ####con los offsets
                    if listaActuadores[contActuador] == "RArm":
                        actuador[0].append([round((trioXYZ[0]**2)*offRArm[0][0]+(-1)*trioXYZ[0]*offRArm[0][1]+offRArm[0][2], 2),
                                            round((trioXYZ[2]**2)*offRArm[1][0]+trioXYZ[2]*offRArm[1][1]+offRArm[1][2], 2),
                                            round((trioXYZ[1]**2)*offRArm[2][0]+trioXYZ[1]*offRArm[2][1]+offRArm[2][2], 2),
                                            0.0, 0.0, 0.0])
                    elif listaActuadores[contActuador] == "RLeg":
                        actuador[1].append([round((trioXYZ[0]**2)*offRLeg[0][2]+(-1)*trioXYZ[0]*offRLeg[0][1]+offRLeg[0][0], 2),
                                            round((trioXYZ[2]**2)*offRLeg[1][2]+trioXYZ[2]*offRLeg[1][1]+offRLeg[1][0], 2),
                                            round((trioXYZ[1]**2)*offRLeg[2][2]+trioXYZ[1]*offRLeg[2][1]+offRLeg[2][0], 2),
                                            0.0, 0.0, 0.0])
                    elif listaActuadores[contActuador] == "LLeg":
                        actuador[2].append([round((trioXYZ[0]**2)*offLLeg[0][2]+(-1)*trioXYZ[0]*offLLeg[0][1]+offLLeg[0][0], 2),
                                            round((trioXYZ[2]**2)*offLLeg[1][2]+trioXYZ[2]*offLLeg[1][1]+offLLeg[1][0], 2),
                                            round((trioXYZ[1]**2)*offLLeg[2][2]+trioXYZ[1]*offLLeg[2][1]+offLLeg[2][0], 2),
                                            0.0, 0.0, 0.0])
                    elif listaActuadores[contActuador] == "LArm":
                        actuador[3].append([round((trioXYZ[0]**2)*offLArm[0][2]+(-1)*trioXYZ[0]*offLArm[0][1]+offLArm[0][0], 2),
                                            round((trioXYZ[2]**2)*offLArm[1][2]+trioXYZ[2]*offLArm[1][1]+offLArm[1][0], 2),
                                            round((trioXYZ[1]**2)*offLArm[2][2]+trioXYZ[1]*offLArm[2][1]+offLArm[2][0], 2),
                                            0.0, 0.0, 0.0])
                    elif listaActuadores[contActuador] == "Torso":
                        actuador[4].append([round((trioXYZ[0]**2)*offTorso[0][2]+(-1)*trioXYZ[0]*offTorso[0][1]+offTorso[0][0], 2),
                                            round((trioXYZ[2]**2)*offTorso[1][2]+trioXYZ[2]*offTorso[1][1]+offTorso[1][0], 2),
                                            round((trioXYZ[1]**2)*offTorso[2][2]+trioXYZ[1]*offTorso[2][1]+offTorso[2][0], 2),
                                            0.0, 0.0, 0.0])
                    elif listaActuadores[contActuador] == "Head":
                        actuador[5].append([round((trioXYZ[0]**2)*offHead[0][2]+(-1)*trioXYZ[0]*offHead[0][1]+offHead[0][0], 2),
                                            round((trioXYZ[2]**2)*offHead[1][2]+trioXYZ[2]*offHead[1][1]+offHead[1][0], 2),
                                            round((trioXYZ[1]**2)*offHead[2][2]+trioXYZ[1]*offHead[2][1]+offHead[2][0], 2),
                                            0.0, 0.0, 0.0])
                    contActuador+=1
                    if contActuador == 6:
                        contActuador = 0
    except Exception,e:
        error.abort("Check file data, not able to read all of it", "CSVMOCAPFunc", "Move")

    #En este punto ya se tienen los vectores de posiciones XYZ+rotacion(0.0) para cada
    #actuador independiente, en el orden segun el archivo CSV

    ##Generando Vector completo como lista de vectores para cada actuador
    global coordenadasCompletasROBOT
    coordenadasCompletasROBOT = [actuador[0], actuador[1], actuador[2], actuador[3], actuador[4], actuador[5]]
    global coordenadasArriba
    coordenadasArriba = [actuador[0], actuador[3], actuador[4]]

    ##Si los datos obtenidos vienen con referencia al TORSO no es necesario este
    ##proceso de cambio de referencia
    listaDeActuadores = deepcopy(coordenadasCompletasROBOT)
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
    ## Head
    for i, item in enumerate(listaDeActuadores[5]):
        for j, item2 in enumerate(listaDeActuadores[5][j]):
            listaDeActuadores[5][i][j] = round((listaDeActuadores[5][i][j] - listaDeActuadores[5][i][j]), 2)
    ## TORSO
    for i, item in enumerate(listaDeActuadores[4]):
        for j, item2 in enumerate(listaDeActuadores[4][j]):
            listaDeActuadores[4][i][j] = round((listaDeActuadores[4][i][j] - listaDeActuadores[4][i][j]), 2)
    #Genera vector con datos respecto al TORSO
    global coordenadasCompletasTORSO
    coordenadasCompletasTORSO = [listaDeActuadores[0], listaDeActuadores[1], listaDeActuadores[2], listaDeActuadores[3], listaDeActuadores[5]]

    #-------------------------------------------------------------------------------
    #Base de tiempo predeterminado para cada vector de la animacion
    ##Debe ser mayor a 20 ms (tiempo que dura en resolver el balance de cuerpo completo)
    ##y dar al menos 30 ms entre cambios
    ##coef depende de los cuadros por segundo de la animacion en Motive en el momento
    ##de exportar los datos
    coef = 0.05
    global listaTiempos
    #listaTiempos = [None]*len(coordenadasCompletasTORSO)
    #for i in range(len(coordenadasCompletasTORSO)):
    #    listaTiempos[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasCompletasTORSO[i]))]
    #Se maneja un vector de tiempos independiente para cada actuador, con longitud
    #correspondiente a la lista con coordenadas respectivo al actuador
    listaTiempos = [None]*len(coordenadasArriba)
    for i in range(len(coordenadasArriba)):
        listaTiempos[i]  = [round(coef*(j+1),2) for j in range(len(coordenadasArriba[i]))]

    print "Coordinates generated. Ready for movement."
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Interfaz de extraccion de datos
##Devuelve lista de actuadores en el CSV, con orden a usar, si no se quiere el
##orden preferente
def getActuadores(frame):
    #return ["RArm", "RLeg", "LLeg", "LArm", "Head"]
    return ["RArm", "LArm", "Torso"] #Si se va a controlar solo area superior
    #return ["RArm", "RLeg", "LLeg", "LArm", "Torso", "Head"]

##Devuelve posiciones X,Y,Z+rot en orden correspondiente a los actuadores obtenidos
##segun el marco ROBOT
def getCoordenadasROBOT():
    #return coordenadasCompletasROBOT
    return coordenadasArriba

##Devuelve posiciones X,Y,Z+rot en orden correspondiente a los actuadores obtenidos
##segun el marco ROBOT
def getCoordenadasTORSO():
    return coordenadasCompletasTORSO

##Devuelve lista de Tiempos del movimiento
def getTiempos():
    return listaTiempos
