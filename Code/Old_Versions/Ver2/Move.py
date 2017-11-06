# -*- encoding: UTF-8 -*-
# imports
import sys
import time
import numpy
from naoqi import ALProxy
import motion

import CSV_read #Lectura de los .CSV

#-------------------------------------------------------------------------------
# control de la rigidez de los motores
def StiffnessOn(proxy):
    # Body representa elconjunto de todas las articulaciones
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

#-------------------------------------------------------------------------------
def main(robotIP):
    #SetUp
    PORT = 9559

    try:
        #Para poder utilizar funciones de movimiento de los actuadores del NAO
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    try:
        #Para utilizar posiciones preestablecidas del NAO
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

#-------------------------------------------------------------------------------
#Inicializacion de parametros necesarios para el movimiento del NAO

    ##Marco de Referencia a utiliza
    #referencia = motion.FRAME_TORSO #Referencia centro del Torso
    referencia = motion.FRAME_WORLD #Referencia estado inicial del robot al iniciar animacion
    #referencia = motion.FRAME_ROBOT #Referencia origen justo debajo del NAO entre los pies

    ##Relacion coordenadas con marco de referencia
    absolutos = False #True para usar coordenadas absolutas respecto al marco de referencia
    useSensor = True #Usar sensores para ubicar los actuadores

    ##Grados de libertad a utilizar
    #axisMask = [ motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL ] #Control de posicion XYZ y rotacion
    axisMask = [ motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL, ] #Control de posicion XYZ

#-------------------------------------------------------------------------------
#Obtencion de la informacion del archivo CVS

    ##Lista con vectores de las posiciones de los actuadores en orden correspondiente
    ##al orden de los actuadores a utilizar
    listaCoordenadas = CSV_read.getCoordenadas()

    ##Lista de Tiempos
    #listaTiempos = CSV_read.getTiempos

    coef = 0.033333 # de acuerdo a tiempos de MoCap
    #coef = 1
    listaTiempos  = [ [coef*(i+1) for i in range(len(listaCoordenadas[0]))],
                        [coef*(i+1) for i in range(len(listaCoordenadas[1]))],
                        [coef*(i+1) for i in range(len(listaCoordenadas[2]))],
                        [coef*(i+1) for i in range(len(listaCoordenadas[3]))],
                        #[coef*(i+1) for i in range(len(listaCoordenadas[4]))],
                        #[coef*(i+1) for i in range(len(listaCoordenadas[5]))]
                    ]

    #print listaCoordenadas[0][0][0]
    ##Lista de Actuadores en el orden a ser usadas
    #listaActuadores = ["RArm", "RLeg", "LLeg", "LArm", "Torso", "Head"]
    listaActuadores = ["RArm", "LArm", "Torso", "Head"] # sin piernas
    #listaActuadores = ["RArm"]

#-------------------------------------------------------------------------------
#Control del movimiento del NAO

    ##Iniciando motores y activando rigidez para poder iniciar el movimiento en el NAO
    #motionProxy.wakeUp()
    StiffnessOn(motionProxy)
    #motionProxy.setStiffnesses("Body", 1.0)

    ##Llevando al NAO a una pose segura para moverse
    #postureProxy.goToPosture("StandInit", 0.5)
    postureProxy.goToPosture("Stand", 0.5)

    ##Ejecucion de las posiciones obtenidas del archivo CSV_read
    motionProxy.positionInterpolations(listaActuadores, referencia, listaCoordenadas, axisMask, listaTiempos, absolutos)

    ##Posicion de reposo
    postureProxy.goToPosture("Crouch", 0.5)
    motionProxy.rest() #Rest the NAO motors
    #motionProxy.setStiffnesses("Body", 0.0)

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato PrisNao
    #robotIp = "169.254.42.173" #Bato Local

    if len(sys.argv) <= 1:
        print "Usage python almotion_positioninterpolations.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
