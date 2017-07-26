# -*- encoding: UTF-8 -*-
#Imports
import sys
import time
import numpy
from naoqi import ALProxy
import motion

#Otros codigos importantes a incluir
import CSV_read #Lectura de los .CSV

#-------------------------------------------------------------------------------
#MAIN
def main(robotIP):
    PORT = 9559

    try:
        #Para poder utilizar funciones de movimiento de los actuadores del NAO
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
        print "hola"
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

##Marco de Referencia a utilizar
#referencia = motion.FRAME_TORSO #Referencia centro del Torso
referencia = motion.FRAME_ROBOT #Referencia origen justo debajo del NAO entre los pies

##Relacion coordenadas con marco de referencia
absolutos   = True #True para usar coordenadas absolutas respecto al marco de referencia

##Grados de libertad a utilizar
#axisMask = [ motion.AXIS_MASK_ALL ] #Control de posicion XYZ y rotacion
axisMask = [ motion.AXIS_MASK_VEL ] #Control de posicion XYZ

#-------------------------------------------------------------------------------
#Obtencion de la informacion del archivo CVS

##Lista de Tiempos
listaTiempos = CSV_read.getTiempos()

##Lista de Actuadores en el orden a ser usadas
listaActuadores = CSV_read.getActuadores()

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

##Llevando al NAO a pose segura de reposo, apagando motores y quitando rigidez
postureProxy.goToPosture("Crouch", 0.5)
motionProxy.rest()
motionProxy.setStiffnesses("Body", 0.0)


#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato en PRISNAO Network
    #robotIp = "10.0.1.193" #Mok en PRISNAO Network

    if len(sys.argv) <= 1:
        print "Usage python almotion_positioninterpolations.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)