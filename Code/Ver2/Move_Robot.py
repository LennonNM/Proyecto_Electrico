# -*- encoding: UTF-8 -*-

import sys
import time
import numpy
from naoqi import ALProxy
import motion

#Otros codigos importantes
import CSV_read #Lectura de los .CSV

#Def
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
#Lectura del archivo CSV y obtencion de la informacion
    columnas = CSV_read.getColumna()
    print columnas[0]
#---------------------------------------------------------
#Control del movimiento del NAO




if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato en PRISNAO Network
    #robotIp = "10.0.1.193" #Mok en PRISNAO Network

    if len(sys.argv) <= 1:
        print "Usage python almotion_positioninterpolations.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
