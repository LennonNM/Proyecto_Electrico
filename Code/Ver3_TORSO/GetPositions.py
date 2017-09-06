import sys
import time
from naoqi import ALProxy
import motion
#CSV edition
import csv
import os
from itertools import islice
from os.path import dirname, abspath


def main(robotIP):
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    space = motion.FRAME_TORSO
    axisMask = [ motion.AXIS_MASK_VEL ]
    useSensorValues = False

    rowsCounter = 0
    rows = 436
    posRArm = []
    posRLeg = []
    posLLeg = []
    posLArm = []
    posTorso = []
    posHead = []
    print "inicia toma de datos"
    while (rowsCounter < rows):

        posRArm.append(motionProxy.getPosition("RArm", space, useSensorValues))
        time.sleep(0.006)
        posRLeg.append(motionProxy.getPosition("RLeg", space, useSensorValues))
        time.sleep(0.006)
        posLLeg.append(motionProxy.getPosition("LLeg", space, useSensorValues))
        time.sleep(0.006)
        posLArm.append(motionProxy.getPosition("LArm", space, useSensorValues))
        time.sleep(0.006)
        posTorso.append(motionProxy.getPosition("Torso", space, useSensorValues))
        time.sleep(0.006)
        posHead.append(motionProxy.getPosition("Head", space, useSensorValues))
        time.sleep(0.006)

        rowsCounter+=1
        #time.sleep(0.033333)

    print "listo toma de datos"


    with open('NuevaCaptura.csv', 'w') as csvfile:
        fieldnames = ['C1', 'C2', 'X RArm', 'Y RArm', 'Z RArm', 'X RLeg', 'Y RLeg', 'Z RLeg',
                        'X LLeg', 'Y LLeg', 'Z LLeg', 'X LArm', 'Y LArm', 'Z LArm',
                        'X Torso', 'Y Torso', 'Z Torso', 'X Head', 'Y Head', 'Z Head']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for x in range(6):
            writer.writerow({})
        writer.writeheader()
        for i in range(rows):
            writer.writerow({'X RArm': posRArm[i][0], 'Y RArm': posRArm[i][1], 'Z RArm': posRArm[i][2],
                                'X RLeg': posRLeg[i][0], 'Y RLeg': posRLeg[i][1], 'Z RLeg': posRLeg[i][2],
                                'X LLeg': posLLeg[i][0], 'Y LLeg': posLLeg[i][1], 'Z LLeg': posLLeg[i][2],
                                'X LArm': posLArm[i][0], 'Y LArm': posLArm[i][1], 'Z LArm': posLArm[i][2],
                                'X Torso': posTorso[i][0], 'Y Torso': posTorso[i][1], 'Z Torso': posTorso[i][2],
                                'X Head': posHead[i][0], 'Y Head': posHead[i][1], 'Z Head': posHead[i][2],
                            })



if __name__ == "__main__":
    robotIp = "10.0.1.128" #Bato PrisNao

    if len(sys.argv) <= 1:
        print "Usage python almotion_advancedcreaterotation.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
