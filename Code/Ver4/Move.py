#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Programa principal para la ejecucion de la Teleoperacion del robot NAO.
#Se encarga del control del NAO por grabaciones guardadas.. Recibe vectores
#de tiempos y coordenadas listos para ser enviados directamente al robot NAO.
#Solicita al usuario IP del robot a conectarse y nombre del archivo CSV que
#contiene los datos de la grabacion de MoCap que se quiere utilizar para que el
#robot "imite" los movimientos. (Primer argumento es el nombre del archivo y
#el segundo es la direccion IP)
##
#Utiliza los API's del robot NAO para efectuar su control.
##
#Permite utilizar marco de referencia ROBOT y TORSO, segun defina el usuario, por
#defecto se trabaja con ROBOT.
##
#Hace uso del balanceador de cuerpo completo incluido en las herramientas de
#desarrollo de las librerias del robot humanoide NAO. Para realizar un mejor
#balance se requiere manipular los puntos de apoyo del balance segun la
#posicion que se esta llevando a cabo.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -*- encoding: UTF-8 -*-
#Imports
import sys
import time
import numpy
from naoqi import ALProxy
import motion

##Custom
import CSVMOCAPFunc as csvMocap
import errorFunc as error

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Control de la rigidez de los motores
def StiffnessOn(proxy):
    # Body representa elconjunto de todas las articulaciones
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
#-------------------------------------------------------------------------------
def main(robotIP,coreo,marcoRef=None):
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
    if marcoRef is not None:
        referencia = marcoRef
    else: #Usa predeterminados
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
    #axisMask = [ motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL ]
    axisMask = [ motion.AXIS_MASK_VEL ]*3

#-------------------------------------------------------------------------------
#Obtencion de la informacion del archivo CVS

    try:
        csvMocap.startAdjustData(coreo)
    except Exception, e:
        error.abort(coreo, "Cannot access file to adjust", "Move")
    ##Lista con vectores de las posiciones de los actuadores en orden correspondiente
    ##al orden de los actuadores a utilizar
    if (referencia == 2):
        #Marco de referencia ROBOT
        listaCoordenadas = csvMocap.getCoordenadasROBOT()
    elif (referencia == 0):
        #Con ajuste respecto al TORSO
        listaCoordenadas = csvMocap.getCoordenadasTORSO()

    ##Lista de Tiempos
    listaTiempos = csvMocap.getTiempos()

    ##Lista de Actuadores en el orden a ser usadas
    ###Orden Preferido "RArm", "RLeg", "LLeg", "LArm", "Torso", "Head"
    listaActuadores = csvMocap.getActuadores()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Control del movimiento del NAO -- Teleoperacion
    #---------------------------------------------------------------------------
    #Preparativos iniciales para mover el NAO

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
    motionProxy.wbEnable(True)

    ##Restriccion de soporte para las piernas
    ###Condicion de operacion
    estadoFijo  = "Fixed" # Posicion Fija
    estadoPlano = "Plane" # Permite desplazamiento sobre el plano
    estadoLibre = "Free"  # Libre movimiento en el espacio
    ###Actuador de soporte
    #### Legs usa ambas piernas, sin embargo se puede manejar la restriccion
    #### para cada pierna de manera independiente
    soportePiernas = "Legs" # Ambas piernas
    soporteIzq     = "LLeg" # Pierna izquierda
    soporteDer     = "RLeg" # Pierna derecha

    ###Habilita soporte de ambas piernas con restricciones
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
    ##Ejecucion de las posiciones obtenidas del archivo csvMocap
    motionProxy.positionInterpolations(listaActuadores, referencia, listaCoordenadas, axisMask, listaTiempos, absolutos)
    #for a in range(len(listaCoordenadas)-1):

    #    motionProxy.positionInterpolations(listaActuadores, referencia, [listaCoordenadas[0][a::a+1], listaCoordenadas[1][a::a+1], listaCoordenadas[2][a::a+1]],
    #        axisMask, [listaTiempos[0][a::a+1], listaTiempos[1][a::a+1], listaTiempos[2][a::a+1]], absolutos)

    ##Tiempo de espera entre ultimo movimiento y estado de reposo del Nao, para
    ##agregar estabilidad
    time.sleep(1.0)

    #Se habilita nuevamente el controlador automatico de caidas
    ##****IMPORTANTE REALIZAR ESTE PASO****##
    motionProxy.setFallManagerEnabled(True)
    ##Desactiva Balance de Cuerpo Completo **Debe ir al final del movimiento**
    motionProxy.wbEnable(False)

    ##Posicion de reposo seguras para finalizar la accion
    postureProxy.goToPosture("Crouch", 0.5)
    motionProxy.rest() # Apaga los motores del Nao
    ## **Si no se apagan es posible que se sobrecalienten aun estando en reposo**

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato por red PrisNao
    #robotIp = "169.254.42.173" #Bato Local
    coreo = ""
    marcoRef = ""

    if len(sys.argv) <= 1:
        errorFunc.abort("None choreography file name received", "Move")
    elif len(sys.argv) == 2:
        coreo = sys.argv[1]
        print "Using default robot IP: 10.0.1.128 (Optional default: 127.0.0.1)"
        print "Choreograph file to read:", coreo
    elif len(sys.argv) == 3:
        coreo   = sys.argv[1]
        robotIp = sys.argv[2]
        print "Using robot IP:", robotIp
        print "Choreograph file to read:", coreo
        time.sleep(1.5) #Tiempo para que el usuario lea las indicaciones
        main(robotIp,coreo)
    elif len(sys.argv) >= 4:
        coreo    = sys.argv[1]
        robotIp  = sys.argv[2]
        marcoRef = sys.argv[2]
        print "Using robot IP:", robotIp
        print "Choreograph file to read:", coreo
        print "Using reference plane:", marcoRef
        time.sleep(1.5) #Tiempo para que el usuario lea las indicaciones
        main(robotIp,coreo,marcoRef)
