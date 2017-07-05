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
    useSensor    = False

    #Body effectors
    LArm = "LArm"
    RArm = "RArm"
    Torso = "Torso"
    Head = "Head"
    RLeg = "RLeg"
    LLeg = "LLeg"

    #Origin Position for Torso
    origin = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

    # Motion of Arms and Torso with block process
    effectorList = [ Head, LArm, LLeg, RLeg, RArm, Torso ]
    axisMaskList = [ motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL,
                    motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL, motion.AXIS_MASK_ALL ]

    # Initial Time List
    timeArray = numpy.array( [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0]] ) #seconds

    #Coordinates list declaration
    LARM_C  =    0
    RARM_C  =    0
    TORSO_C =    0
    HEAD_C  =    0
    RLEG_C  =    0
    LLEG_C  =    0

    #Coordinates process from file
    coordinate = open("coordinates.txt", "r") #Open text file

    for line in coordinate.readlines():
        LARM_C = map(float, line.split()) #Transforms string list to float

        #Get Previous Positions
        prevPos_LARM = motionProxy.getPosition(LArm, space, useSensor)
        prevPos_RARM = motionProxy.getPosition(RArm, space, useSensor)
        prevPos_TORSO = motionProxy.getPosition(Torso, space, useSensor)
        prevPos_HEAD = motionProxy.getPosition(Head, space, useSensor)
        prevPos_RLEG = motionProxy.getPosition(RLeg, space, useSensor)
        prevPos_LLEG = motionProxy.getPosition(LLeg, space, useSensor)

        #Set Next Positions
            #Left Arm
        nextPos_LARM = [
                         prevPos_LARM[0] + LARM_C[0],
                         prevPos_LARM[1] + LARM_C[1],
                         prevPos_LARM[2] + LARM_C[2],
                         prevPos_LARM[3] + LARM_C[3],
                         prevPos_LARM[4] + LARM_C[4],
                         prevPos_LARM[5] + LARM_C[5]
                         ]
            #Right Arm
        nextPos_RARM = [
                          prevPos_RARM[0] + 0.00,
                          prevPos_RARM[1] + 0.00,
                          prevPos_RARM[2] + 0.00,
                          prevPos_RARM[3] + 0.00,
                          prevPos_RARM[4] + 0.00,
                          prevPos_RARM[5] + 0.00
                          ]
            #Torso
        nextPos_TORSO = [
                         prevPos_TORSO[0] + 0.00,
                         prevPos_TORSO[1] + 0.00,
                         prevPos_TORSO[2] + 0.00,
                         prevPos_TORSO[3] + 0.00,
                         prevPos_TORSO[4] + 0.00,
                         prevPos_TORSO[5] + 0.00
                         ]
            #Head
        nextPos_HEAD = [
                         prevPos_HEAD[0] + 0.00,
                         prevPos_HEAD[1] + 0.00,
                         prevPos_HEAD[2] + 0.00,
                         prevPos_HEAD[3] + 0.00,
                         prevPos_HEAD[4] + 0.00,
                         prevPos_HEAD[5] + 0.00
                         ]
            #Right LEG
        nextPos_RLEG = [
                         prevPos_RLEG[0] + 0.00,
                         prevPos_RLEG[1] + 0.00,
                         prevPos_RLEG[2] + 0.00,
                         prevPos_RLEG[3] + 0.00,
                         prevPos_RLEG[4] + 0.00,
                         prevPos_RLEG[5] + 0.00
                         ]
            #Left LEG
        nextPos_LLEG = [
                         prevPos_LLEG[0] + 0.00,
                         prevPos_LLEG[1] + 0.00,
                         prevPos_LLEG[2] + 0.00,
                         prevPos_LLEG[3] + 0.00,
                         prevPos_LLEG[4] + 0.00,
                         prevPos_LLEG[5] + 0.00
                         ]

        # Movement Vectors
        pathList   =   [
                        [ prevPos_LARM, nextPos_LARM ],    #LArm
                        [ prevPos_RARM, nextPos_RARM ],    #RARM
                        [ prevPos_TORSO, nextPos_TORSO ],  #TORSO
                        [ prevPos_HEAD, nextPos_HEAD ],    #HEAD
                        [ prevPos_RLEG, nextPos_RLEG ],    #RLEG
                        [ prevPos_LLEG, nextPos_LLEG ],    #LLEG
                       ]

        #Convert array Times to Times List
        timeList = timeArray.tolist()

        #Move NAO
        motionProxy.positionInterpolations(effectorList, space, pathList, axisMaskList, timeList, isAbsolute)

        #Times List Vectors
        timeArray += 1.0

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
