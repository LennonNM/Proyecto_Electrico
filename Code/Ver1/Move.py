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
    #space = motion.FRAME_ROBOT
    isAbsolute   = True #Absolute coordinates for effectors
    useSensor    = False

    #Starts motors and goes to init position
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)

    #Body effectors to Use
    #  Head, LArm, LLeg, RLeg, RArm, Torso

    #Origin Position for Torso
    origin = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

    # Motion of Arms and Torso with block process
    #effectorList = [ "Head", "LArm", "LLeg", "RLeg", "RArm", "Torso" ] #Order of effectors to receive vectors on setPositionInterpolations
    #axisMaskList = [ motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL,
    #                motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL ]
    effectorList = [ "Head", "LArm", "RArm" ] #Order of effectors to receive vectors on setPositionInterpolations
    axisMaskList = [ motion.AXIS_MASK_ALL ]

    # Initial Time List
    #timeArray = numpy.array( [[1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0], [1.0, 2.0]] ) #seconds
    timeArray = numpy.array ([ [1.0, 2.0], [1.0, 2.0], [1.0, 2.0] ])

    #Coordinates process from file
    index = 0
    coordinate = open("coordinates.txt", "r") #Open text file

    #For initial movement after StanInit
    prevPos_HEAD  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.3]
    prevPos_LARM  = [0.12, 0.12, 0.0, 0.0, 0.0, 0.0]
    prevPos_LLEG  = [0.12, 0.12, 0.0, 0.0, 0.0, 0.0]
    prevPos_RLEG  = [0.12, 0.12, 0.0, 0.0, 0.0, 0.0]
    prevPos_RARM  = [0.12, -0.12, 0.0, 0.0, 0.0, 0.0]
    prevPos_TORSO = [0.12, 0.12, 0.0, 0.0, 0.0, 0.0]

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
            #prevPos_HEAD  = motionProxy.getPosition("Head", space, useSensor)
            #prevPos_LARM  = motionProxy.getPosition("LArm", space, useSensor)
            #prevPos_LLEG  = motionProxy.getPosition("LLeg", space, useSensor)
            #prevPos_RLEG  = motionProxy.getPosition("RLeg", space, useSensor)
            #prevPos_RARM  = motionProxy.getPosition("RArm", space, useSensor)
            #prevPos_TORSO = motionProxy.getPosition("Torso", space, useSensor)

            # Movement Vectors
            #pathList   =   [
            #                [ prevPos_HEAD, nextPos_HEAD ],    #HEAD
            #                [ prevPos_LARM, nextPos_LARM ],    #LArm
            #                [ prevPos_LLEG, nextPos_LLEG ],    #LLEG
            #                [ prevPos_RLEG, nextPos_RLEG ],    #RLEG
            #                [ prevPos_RARM, nextPos_RARM ],    #RARM
            #                [ prevPos_TORSO, nextPos_TORSO ]   #TORSO
            #               ]
            #pathList = [ prevPos_TORSO, nextPos_TORSO ]

            pathList = [ [prevPos_HEAD, nextPos_HEAD], [prevPos_LARM, nextPos_LARM], [prevPos_RARM, nextPos_RARM] ]

            prevPos_HEAD  = nextPos_HEAD
            prevPos_LARM  = nextPos_LARM
            prevPos_LLEG  = nextPos_LLEG
            prevPos_RLEG  = nextPos_RLEG
            prevPos_RARM  = nextPos_RARM
            prevPos_TORSO = nextPos_TORSO

            #Move NAO (Needs timeList)
            #motionProxy.positionInterpolations(effectorList, space, pathList, axisMaskList, timeArray.tolist(), isAbsolute)
    #        motionProxy.positionInterpolations(effectorList, space, pathList, axisMaskList, timeArray.tolist(), isAbsolute)

            #Frames per second
            time.sleep(1)
            #Times List Vectors
            timeArray += 2.0
        #If not collected all 6 effectors vector lists
        else:
            index += 1

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
