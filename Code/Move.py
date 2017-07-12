# -*- encoding: UTF-8 -*-

import sys
import time
import numpy
from naoqi import ALProxy
import motion

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
    space        = motion.FRAME_TORSO
    isAbsolute   = False
    useSensor    = True

    #Starts motors and goes to init position
    motionProxy.wakeUp()

    #Body effectors to Use
    #  Head, LArm, LLeg, RLeg, RArm, Torso

    #Origin Position for Torso
    origin = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

    # Motion of Arms and Torso with block process
    effectorList = [ "Head", "LArm", "LLeg", "RLeg", "RArm", "Torso" ] #Order of effectors to receive vectors on setPositionInterpolations
    axisMaskList = [ motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL,
                    motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL ]

    # Initial Time List
    timeArray = numpy.array( [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0]] ) #seconds

    #Coordinates process from file
    coordinate = open("coordinates.txt", "r") #Open text file
    index = 0

    for line in coordinate.readlines():
        #Assign Coordinates to respective effector vector
        if (index == 0):
            nextPos_HEAD = map(float, line.split()) #Transforms string list to float
        elif (index == 1 ):
            nextPos_LARM = map(float, line.split())
        elif (index == 2 ):
            nextPos_LLEG = map(float, line.split())
        elif (index == 3 ):
            nextPos_RLEG = map(float, line.split())
        elif (index == 4 ):
            nextPos_RARM = map(float, line.split())
        elif (index == 5 ):
            nextPos_TORSO = map(float, line.split())
        #Line #7 is a separator for coordinates groups

        if (index == 6):
            #All 6 effectors vector lists collected
            index = 0

            #Get Previous Positions
            prevPos_HEAD  = motionProxy.getPosition("Head", space, useSensor)
            prevPos_LARM  = motionProxy.getPosition("LArm", space, useSensor)
            prevPos_LLEG  = motionProxy.getPosition("LLeg", space, useSensor)
            prevPos_RARM  = motionProxy.getPosition("RArm", space, useSensor)
            prevPos_RLEG  = motionProxy.getPosition("RLeg", space, useSensor)
            prevPos_TORSO = motionProxy.getPosition("Torso", space, useSensor)

            # Movement Vectors
            pathList   =   [
                            [ prevPos_HEAD, nextPos_HEAD ],    #HEAD
                            [ prevPos_LARM, nextPos_LARM ],    #LArm
                            [ prevPos_LLEG, nextPos_LLEG ],    #LLEG
                            [ prevPos_RARM, nextPos_RARM ],    #RARM
                            [ prevPos_RLEG, nextPos_RLEG ],    #RLEG
                            [ prevPos_TORSO, nextPos_TORSO ]   #TORSO
                           ]


            #Move NAO
            motionProxy.positionInterpolations(effectorList, space, pathList, axisMaskList, timeArray.tolist(), isAbsolute)
                                                                                            #Needs timeList
            print(pathList)
            #Times List Vectors
            timeArray += 1.0
        #If not collected all 6 effectors vector lists
        else:
            index += 1

    #Posicion de reposo
    postureProxy.goToPosture("Crouch", 0.5)
    motionProxy.rest() #Rest the NAO motors

    coordinate.close() #Close text file and free resources


if __name__ == "__main__":
    #robotIp = "192.168.18.214"
    #robotIp = "10.0.1.154"
    #robotIp = "169.254.113.113"
    robotIp = "10.0.1.128"

    if len(sys.argv) <= 1:
        print "Usage python almotion_positioninterpolations.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
