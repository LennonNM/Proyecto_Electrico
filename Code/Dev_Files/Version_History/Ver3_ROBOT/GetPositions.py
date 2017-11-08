import sys
import time
from naoqi import ALProxy
import motion

#CSV edition
import csv
import os
from itertools import islice
from os.path import dirname, abspath
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main(robotIP):
    PORT = 9559
    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Ajustes iniciales

    #Marco de referencia para la obtencion de datos
    space = motion.FRAME_ROBOT
    #Uso de sensores adicionales para aproximar el estado del actuador
    useSensorValues = False
#-------------------------------------------------------------------------------
#Obtencion de los datos

    rowsCounter = 0
    rows = 436 #Tamaño de la muestra
    posRArm = []
    posRLeg = []
    posLLeg = []
    posLArm = []
    posTorso = []
    posHead = []

    print "Inicia toma de datos"

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

    print "Terminada toma de datos"
#-------------------------------------------------------------------------------
#Guardado de los datos en un archivo CSV

    #Se utiliza el formato de Motive para el acomodo de los datos en el CSV
    ## 2 columnas con cuadros y tiempos (no se ocupan), 3 columnas (XYZ) por cada
    ## marcador involucrado(actuador) /// Filas 1 a 6 no dan informacion valiosa,
    ## en la fila 7 va el identificador de cada columna, a partir de la fila 8
    ## inician los datos de las posiciones
    with open('NuevaCaptura.csv', 'w') as csvfile:
        fieldnames = ['C1', 'C2', 'X RArm', 'Y RArm', 'Z RArm', 'X RLeg', 'Y RLeg', 'Z RLeg',
                        'X LLeg', 'Y LLeg', 'Z LLeg', 'X LArm', 'Y LArm', 'Z LArm',
                        'X Torso', 'Y Torso', 'Z Torso', 'X Head', 'Y Head', 'Z Head']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for x in range(6):
            writer.writerow({})
        writer.writeheader()
        for i in range(rows):
            writer.writerow({'X RArm': posRArm[i][0], 'Y RArm': posRArm[i][1], 'Z RArm': posRArm[i][2],
                                'X RLeg': posRLeg[i][0], 'Y RLeg': posRLeg[i][1], 'Z RLeg': posRLeg[i][2],
                                'X LLeg': posLLeg[i][0], 'Y LLeg': posLLeg[i][1], 'Z LLeg': posLLeg[i][2],
                                'X LArm': posLArm[i][0], 'Y LArm': posLArm[i][1], 'Z LArm': posLArm[i][2],
                                'X Torso': posTorso[i][0], 'Y Torso': posTorso[i][1], 'Z Torso': posTorso[i][2],
                                'X Head': posHead[i][0], 'Y Head': posHead[i][1], 'Z Head': posHead[i][2],
                            })
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato en red PrisNao

    if len(sys.argv) <= 1:
        print "Usage python almotion_advancedcreaterotation.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
