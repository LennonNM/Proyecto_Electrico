# -*- encoding: UTF-8 -*-

import sys
import time
import numpy
from naoqi import ALProxy
import motion
import CSV_read #Lectura de los .CSV
def main(robotIP):
#---------------------------------------------------------
    #SetUp
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

#---------------------------------------------------------

    # Send NAO to Pose Init for Safety
    #postureProxy.goToPosture("StandInit", 0.5)

    # Motion SetUp
    referencia        = motion.FRAME_TORSO
    #space = motion.FRAME_ROBOT
    absolutos   = True #Absolute coordinates for effectors
    useSensor    = False
    axisMask = [ motion.AXIS_MASK_VEL ]

    #Starts motors and goes to init position
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)

#Lista de Tiempos
    listaTiempos = CSV_read.getTiempos()
    print listaTiempos

    ##Lista de Actuadores en el orden a ser usadas
    listaActuadores = ["RArm", "RLeg", "LLeg", "LArm", "Torso", "Head"]

    ##Lista con vectores de las posiciones de los actuadores en orden correspondiente
    ##al orden de los actuadores a utilizar
    listaCoordenadas = CSV_read.getCoordenadas()

    #-------------------------------------------------------------------------------
    #Control del movimiento del NAO

    ##Iniciando motores y activando rigidez para poder iniciar el movimiento en el NAO
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)

    ##Llevando al NAO a una pose segura para moverse
    postureProxy.goToPosture("StandInit", 0.5)

    ##Ejecucion de las posiciones obtenidas del archivo CSV_read
    motionProxy.positionInterpolations(listaActuadores, referencia, listaCoordenadas, axisMask, listaTiempos, absolutos)


    #Posicion de reposo
    #postureProxy.goToPosture("Crouch", 0.5)
    motionProxy.rest() #Rest the NAO motors
    motionProxy.setStiffnesses("Body", 0.0)

    coordinate.close() #Close text file and free resources


if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato
    #robotIp = "10.0.1.193"

    if len(sys.argv) <= 1:
        print "Usage python almotion_positioninterpolations.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
