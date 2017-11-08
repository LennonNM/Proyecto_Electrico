# -*- encoding: UTF-8 -*-
# imports
import sys
import time
import numpy
from naoqi import ALProxy
import motion

import CSV_read #Lectura de los .CSV

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

#Inicializacion de parametros necesarios para el movimiento del NAO

    ##Marco de Referencia a utiliza
    #referencia = motion.FRAME_TORSO #Referencia centro del Torso
    referencia = motion.FRAME_ROBOT #Referencia origen justo debajo del NAO entre los pies

    ##Relacion coordenadas con marco de referencia
    absolutos = False #True para usar coordenadas absolutas respecto al marco de referencia
    useSensor = True #Usar sensores para ubicar los actuadores

    ##Grados de libertad a utilizar
    #axisMask = [ motion.AXIS_MASK_ALL ] #Control de posicion XYZ y rotacion
    axisMask = [ motion.AXIS_MASK_VEL ] #Control de posicion XYZ

    listaCoordenadas = [0.0488456599,
    0.0488456599,
    0.0488456599,
    0.0488456599,
    0.0488456413,
    0.0488442518,
    0.0488396436,
    0.0488259159,
    0.0488085113,
    0.0487673394,
    0.0487040579,
    0.0486594476,
    0.0486279652,
    0.0486015752,
    0.0485816337,
    0.0485702865,
    0.0485735275,
    0.0485943258,
    0.0669711605,
    0.0699636489,
    0.1712833047,
    0.1757912487,
    0.1800001264,
    0.1829434484,
    0.1865603924,
    0.1905511022,
    0.1926448494,
    0.1950657219,
    0.1486934721,
    0.1422346234,
    0.1372394562,
    0.1304036081,
    -0.0069721006,
    -0.0107158283,
    -0.0140931904,
    -0.0170932375,
    -0.0197041202,
    -0.0224044956,
    -0.0237171203,
    -0.0250986982,
    -0.0268862396,
    -0.0268862396,
    -0.0268862396,
    -0.0268862396,
    -0.0268862396]

    coef = 1.0
    listaTiempos = [coef*(i+1) for i in range(len(listaCoordenadas))]

    listaActuadores = ["RArm"]

    motionProxy.positionInterpolations(listaActuadores, referencia, listaCoordenadas, axisMask, listaTiempos, absolutos)
