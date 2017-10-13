# -*- encoding: UTF-8 -*-
# imports
import sys
import time
import numpy
from naoqi import ALProxy
import motion

import CSV_read #Lectura de los .CSV
#-------------------------------------------------------------------------------
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
    PORT = 9559 #Puerto por defecto
    #creacion de objetos para usar los metodos de los API's del Nao
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
#-------------------------------------------------------------------------------
#Inicializacion de parametros necesarios para el movimiento del NAO

    ##Marco de Referencia a utilizar
    #referencia = motion.FRAME_TORSO #Referencia centro del Torso
                                    #Vale 0
    #referencia = motion.FRAME_WORLD #Referencia estado inicial del robot al iniciar animacion
                                    #Vale 1
    referencia = motion.FRAME_ROBOT #Referencia origen justo debajo del NAO entre los pies
                                    #Vale 2

    ##Relacion coordenadas con marco de referencia
    absolutos = False #True para usar coordenadas absolutas respecto al marco de referencia

    ##Grados de libertad a utilizar
    ###Debe incluir un elemento por cada actuador a controlar
    #### AXIS_MASK_ALL controla XYZ y rotacion
    #### AXIS_MASK_VEL controla solo XYZ
    #axisMask = [ motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL ]
    axisMask = [ motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL ]

#-------------------------------------------------------------------------------
#Obtencion de la informacion del archivo CVS

    ##Lista con vectores de las posiciones de los actuadores en orden correspondiente
    ##al orden de los actuadores a utilizar
    if (referencia == 2):
        #Marco de referencia ROBOT
        listaCoordenadas = CSV_read.getCoordenadasROBOT()
    elif (referencia == 0):
        #Con ajuste respecto al TORSO
        listaCoordenadas = CSV_read.getCoordenadasTORSO()

    ##Lista de Tiempos
    listaTiempos = CSV_read.getTiempos()

    ##Lista de Actuadores en el orden a ser usadas
    ###Orden Preferido "RArm", "RLeg", "LLeg", "LArm", "Torso", "Head"
    #listaActuadores = CSV_read.getActuadores() #en caso de no querer usar orden
                                                #preferente
    #listaActuadores = ["RArm", "LArm", "Torso"] # sin piernas ni cabeza
    listaActuadores = ["RArm", "RLeg", "LLeg", "LArm", "Torso", "Head"]

#-------------------------------------------------------------------------------
#Control del movimiento del NAO
    #---------------------------------------------------------------------------
    #Ajustes iniciales

    ##Iniciando motores y activando rigidez para poder iniciar el movimiento
    ##en el NAO, si la rigidez no esta puesta el Nao no se mueve
    #motionProxy.wakeUp()
    StiffnessOn(motionProxy)

    ##Llevando al NAO a una pose segura para moverse
    postureProxy.goToPosture("StandInit", 0.5)
    #postureProxy.goToPosture("Stand", 0.5) #Pose preferente
    ##Una vez que esta en una posicion segura se puede inhabilitar el contorlador
    ##automatico de caidas, esto para que no restrinja ciertas posiciones del Nao
    ### **Tener en cuenta que ahora corre peligro de caidas dañinas, el Nao Debe
    ### estar en un ambiente controlado y el usuario atento a caidas para que
    ### no sufra daños evitables**
    motionProxy.setFallManagerEnabled(False)

    ##Habilita Balanceo de Cuerpo Completo Automatico
    activarBalance = True
    motionProxy.wbEnable(activarBalance)

    ##Restriccion de soporte para las piernas
    ###Modo de restriccion
    estadoFijo   = "Fixed" # Posicion Fija
    estadoPlano = "Plane" # Permite desplazamiento sobre el plano
    estadoLibre = "Free"  # Libre movimiento en el espacio
    ###Actuador de soporte
    #### Legs usa ambas piernas, sin embargo se puede manejar la restriccion
    #### para cada pierna de manera independiente
    soportePiernas = "Legs" # Ambas piernas
    soporteIzq = "LLeg" # Pierna izquierda
    soporteDer = "RLeg" # Pierna derecha

    ###Habilita soporte de piernas con restricciones
    motionProxy.wbFootState(estadoFijo, soportePiernas)
    ###Para usar piernas con estados individuales
    #motionProxy.wbFootState(estadoFijo, soporteDer)
    #motionProxy.wbFootState(estadoFijo, soporteIzq)
    ##Habilita balance del cuerpo sobre el soporte definido
    soporteActivo = True
    motionProxy.wbEnableBalanceConstraint(soporteActivo, soportePiernas)
    #---------------------------------------------------------------------------
    #Inicio del movimiento

    ##Tiempo de espera para iniciar movimiento
    time.sleep(1.0)
    ##Ejecucion de las posiciones obtenidas del archivo CSV_read
    motionProxy.positionInterpolations(listaActuadores, referencia, listaCoordenadas, axisMask, listaTiempos, absolutos)
    #for a in range(len(listaCoordenadas)-1):

    #    motionProxy.positionInterpolations(listaActuadores, referencia, [listaCoordenadas[0][a::a+1], listaCoordenadas[1][a::a+1], listaCoordenadas[2][a::a+1]],
    #        axisMask, [listaTiempos[0][a::a+1], listaTiempos[1][a::a+1], listaTiempos[2][a::a+1]], absolutos)

    ##Tiempo de espera entre ultimo movimiento y estado de reposo del Nao, para
    ##agregar estabilidad
    time.sleep(1.0)

    #Se habilita nuevamente el controlador automatico de caidas
    motionProxy.setFallManagerEnabled(True)
    ##Desactiva Balance de Cuerpo Completo **Debe ir al final del movimiento**
    activarBalance = False
    motionProxy.wbEnable(activarBalance)

    ##Posicion de reposo seguras para finalizar la accion
    postureProxy.goToPosture("Crouch", 0.5)
    motionProxy.rest() # Apaga los motores del Nao
    ## **Si no se apagan es posible que se sobrecalienten aun estando en reposo**

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato por red PrisNao
    #robotIp = "169.254.42.173" #Bato Local

    if len(sys.argv) <= 1:
        print "Usage python almotion_positioninterpolations.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
