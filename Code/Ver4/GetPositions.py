#Al ejecutarse inicia la toma de datos de las posiciones de los actuadores
#correspondientes a los 6 efectores finales del robot humanoide NAO
#(RArm, RLeg, LLeg, LArm, Torso, Head). Se toman "rows" cantidad de sets de
#coordenadas. Se incluye coordenadas XYZ (+rotaciones si se especifica por el
#usuario)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import sys
import time
from naoqi import ALProxy
import motion
import csv
import os
from itertools import islice
from os.path import dirname, abspath

##Custom
import errorFunc
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main(robotIP, frame, rotation):
    PORT = 9559
    print "Using Port:", PORT
    if rotation.lower() == "no":
        includeW = False
    elif rotation.lower() == "yes":
        includeW = True
    else:
        errorFunc.abort("Expected a yes or no input for rotation data inclussion", "GetPositions")

    try:
        print "Trying to create ALMotion proxy"
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
        sys.exit(1)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Ajustes iniciales

    #Marco de referencia para la obtencion de datos
    if frame == "ROBOT":
        space = motion.FRAME_ROBOT
    elif frame == "TORSO":
        space = motion.FRAME_TORSO
    else:
        errorFunc.abort("is not a valid frame for function", "GetPositions", frame)
    #Uso de sensores adicionales para aproximar el estado del actuador
    useSensorValues = False
#-------------------------------------------------------------------------------
#Obtencion de los datos

    rowsCounter = 0
    rows = 220 #Tamano de la muestra
    posRArm = []
    posRLeg = []
    posLLeg = []
    posLArm = []
    posTorso = []
    posHead = []

    print "Starting to collect data, interrupt the process only is necessary"
    print "Wait for completion"
    time.sleep(0.5)

    while (rowsCounter < rows):
        posRArm.append(motionProxy.getPosition("RArm", space, useSensorValues))
        time.sleep(0.006) #Aproximacion de 0.033333/6 (tiempo de un cuadro/actuadores)
        posRLeg.append(motionProxy.getPosition("RLeg", space, useSensorValues))
        time.sleep(0.006)
        posLLeg.append(motionProxy.getPosition("LLeg", space, useSensorValues))
        time.sleep(0.006)
        posLArm.append(motionProxy.getPosition("LArm", space, useSensorValues))
        time.sleep(0.006)
        posTorso.append(motionProxy.getPosition("Torso", space, useSensorValues))
        time.sleep(0.006)
        posHead.append(motionProxy.getPosition("Head", space, useSensorValues))
        time.sleep(0.006)

        rowsCounter+=1

    print "Data collection finished"
    print "Writing CSV with data"
    time.sleep(0.25)
#-------------------------------------------------------------------------------
#Guardado de los datos en un archivo CSV

    #Se utiliza el formato de Motive para el acomodo de los datos en el CSV
    ## 2 columnas con cuadros y tiempos (no se ocupan), 3 columnas (XYZ) por cada
    ## marcador involucrado(actuador) /// Filas 1 a 6 no dan informacion valiosa,
    ## en la fila 7 va el identificador de cada columna, a partir de la fila 8
    ## inician los datos de las posiciones
    archivo = "NAO_"
    archivo += frame
    if inlcudeW == True:
        archivo += "-wROT"
    archivo += time.strftime("_%Y-%m-%d")
    archivo += ".csv"

    #Archivo incluyendo rotaciones del NAO
    if includeW == True:
        with open(archivo, 'w') as csvfile:
            fieldnames = ['C1', 'C2', 'X RArm', 'Y RArm', 'Z RArm', 'WX RArm', 'WY RArm', 'WZ RArm', 'X RLeg', 'Y RLeg', 'Z RLeg', 'WX RLeg', 'WY RLeg', 'WZ RLeg',
                            'X LLeg', 'Y LLeg', 'Z LLeg', 'WX LLeg', 'WY LLeg', 'WZ LLeg', 'X LArm', 'Y LArm', 'Z LArm', 'WX LArm', 'WY LArm', 'WZ LArm',
                            'X Torso', 'Y Torso', 'Z Torso', 'WX Torso', 'WY Torso', 'WZ Torso', 'X Head', 'Y Head', 'Z Head', 'WX Head', 'WY Head', 'WZ Head']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for x in range(6):
                writer.writerow({})
            writer.writeheader()
            for i in range(rows):
                writer.writerow({'X RArm': posRArm[i][0], 'Y RArm': posRArm[i][1], 'Z RArm': posRArm[i][2], 'WX RArm': posRArm[i][0], 'WY RArm': posRArm[i][1], 'WZ RArm': posRArm[i][2],
                                    'X RLeg': posRLeg[i][0], 'Y RLeg': posRLeg[i][1], 'Z RLeg': posRLeg[i][2], 'WX RLeg': posRLeg[i][0], 'WY RLeg': posRLeg[i][1], 'WZ RLeg': posRLeg[i][2],
                                    'X LLeg': posLLeg[i][0], 'Y LLeg': posLLeg[i][1], 'Z LLeg': posLLeg[i][2], 'WX LLeg': posLLeg[i][0], 'WY LLeg': posLLeg[i][1], 'WZ LLeg': posLLeg[i][2],
                                    'X LArm': posLArm[i][0], 'Y LArm': posLArm[i][1], 'Z LArm': posLArm[i][2], 'WX LArm': posLArm[i][0], 'WY LArm': posLArm[i][1], 'WZ LArm': posLArm[i][2],
                                    'X Torso': posTorso[i][0], 'Y Torso': posTorso[i][1], 'Z Torso': posTorso[i][2], 'WX Torso': posTorso[i][0], 'WY Torso': posTorso[i][1], 'WZ Torso': posTorso[i][2],
                                    'X Head': posHead[i][0], 'Y Head': posHead[i][1], 'Z Head': posHead[i][2], 'WX Head': posHead[i][0], 'WY Head': posHead[i][1], 'WZ Head': posHead[i][2],
                                })
        #Archivo sin rotaciones
    else:
            with open(archivo, 'w') as csvfile:
                fieldnames = ['C1', 'C2', 'X RArm', 'Y RArm', 'Z RArm', 'X RLeg', 'Y RLeg', 'Z RLeg', 'X LLeg', 'Y LLeg', 'Z LLeg', 'X LArm', 'Y LArm', 'Z LArm',
                                  'X Torso', 'Y Torso', 'Z Torso', 'X Head', 'Y Head', 'Z Head']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for x in range(6):
                    writer.writerow({})
                writer.writeheader()
                for i in range(rows):
                    writer.writerow({'X RArm': posRArm[i][0], 'Y RArm': posRArm[i][1], 'Z RArm': posRArm[i][2], 'X RLeg': posRLeg[i][0], 'Y RLeg': posRLeg[i][1], 'Z RLeg': posRLeg[i][2],
                                        'X LLeg': posLLeg[i][0], 'Y LLeg': posLLeg[i][1], 'Z LLeg': posLLeg[i][2], 'X LArm': posLArm[i][0], 'Y LArm': posLArm[i][1], 'Z LArm': posLArm[i][2],
                                        'X Torso': posTorso[i][0], 'Y Torso': posTorso[i][1], 'Z Torso': posTorso[i][2], 'X Head': posHead[i][0], 'Y Head': posHead[i][1], 'Z Head': posHead[i][2],
                                    })

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIP = "10.0.1.128" #Bato en red PrisNAO
    frame = "ROBOT"
    rotation = "no"

    if len(sys.argv) <= 1:
        print "Default robot IP", robotIP, " with default frame: ROBOT"
        print "Include rotations: no"
    elif len(sys.argv) == 2:
        robotIP = sys.argv[1]
        print "Using robot IP:", sys.argv[1], " with default frame: ROBOT"
        print "Include rotations: no"
    elif len(sys.argv) == 3:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        print "Using robot IP:", sys.argv[1], " with frame:", frame
        print "Include rotations: no"
    elif len(sys.argv) == 4:
        robotIP = sys.argv[1]
        frame = sys.argv[2]
        rotation = sys.argv[3]
        print "Using robot IP:", sys.argv[1], " with frame:", frame
        print "Include rotations:", rotation

    time.sleep(1.0)
    main(robotIP, frame, rotation)
