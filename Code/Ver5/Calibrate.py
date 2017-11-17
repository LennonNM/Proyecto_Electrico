#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Utiliza las funciones definidas en CalibrateFunc.py para realizar el proceso de
#calibracion para la teleoperacion del NAO, los factores generados por este
#proceso son usados en CSV_read.py para el ajuste de las coordenadas.
##
#Realiza la calibracion segun las grabaciones de datos para calibrar dentro del
#directorio local ../Cal/NAO para las del robot NAO, y ../Cal/Human para las de
#la persona. Las grabaciones del NAO son predefinidas, las de la persona en
#utilizar el sistema deben obtenerse de grabaciones previas al proceso de
#calibracion.
##
#El directorio donde se encuentran los datos de la persona se debe especificar
#y estar contenido en .../Cal/Human con las grabaciones requeridas, cuyos nombres
#deben seguir el formato *LetraMayusculaIndicandoPrueba*_Cal_P.csv, con la
#letra en mayusucla correspondiente a la pose de calibracion del NAO.
#Si no se especifica directorio se considera que se usan los archivos predefinidos
#dentro de .../Cal/Human
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import sys
import time

##Custom
import CalibrateFunc as cal
import ErrorFunc as error
import OffsetFileFunc as offset

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main(polDeg, humanDir=""):
    #Datos para calibrar el movimiento de los brazos
    ###Obtiene datos desde los csv correspondientes para la primer pose de calibracion
    RArmNaoA,RLegNaoA,LLegNaoA,LArmNaoA,TorsoNaoA,HeadNaoA,RArmPA,RLegPA,LLegPA,LArmPA,TorsoPA,HeadPA = cal.setCalData("Brazos_NAO.csv",humanDir + "/" + "Brazos.csv")
    ##Obtiene factores para la regresion polinomial deseada para el ajuste
    print RArmPA[0]
    factRArmA  = cal.getTerms(RArmNaoA, RArmPA, polDeg)
    factLArmA  = cal.getTerms(RArmNaoA, LArmPA, polDeg)

    ##Repite pasos anteriores para cada una de las poses usadas para los demas actuadores
    ###Pierna derecha
    RArmNaoB,RLegNaoB,LLegNaoB,LArmNaoB,TorsoNaoB,HeadNaoB,RArmPB,RLegPB,LLegPB,LArmPB,TorsoPB,HeadPB = cal.setCalData("PiernaD_NAO.csv",humanDir + "/" + "PiernaD.csv")
    factRLeg  = cal.getTerms(RLegNaoB, RLegPB, polDeg)
    ###Pierna izquierda
    RArmNaoC,RLegNaoC,LLegNaoC,LArmNaoC,TorsoNaoC,HeadNaoC,RArmPC,RLegPC,LLegPC,LArmPC,TorsoPC,HeadPC = cal.setCalData("PiernaI_NAO.csv",humanDir + "/" + "PiernaI.csv")
    factLLeg  = cal.getTerms(RLegNaoB, RLegPB, polDeg)
    ###Pierna Torso
    RArmNaoD,RLegNaoD,LLegNaoD,LArmNaoD,TorsoNaoD,HeadNaoD,RArmPD,RLegPD,LLegPD,LArmPD,TorsoPD,HeadPD = cal.setCalData("Torso_NAO.csv",humanDir + "/" + "Torso.csv")
    factTorso  = cal.getTerms(RLegNaoB, RLegPB, polDeg)

    #---------------------------------------------------------------------------
    ##Obtiene ajuste general aplicable a todas las poses involucradas
    #xRArm, yRArm, zRArm = cal.setAdjustAct([factRArmA, factRArmB])
    #---------------------------------------------------------------------------
    #xRLeg, yRLeg, zRLeg = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xLLeg, yLLeg, zLLeg = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xLArm, yLArm, zLArm = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xTorso, yTorso, zTorso = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xHead, yHead, zHead = cal.setAdjustAct()

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #Genera archivo CSV con los offsets finales a utilizar
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Writing offsets to default: .../Cal/Offsets/offsets.csv"
    try:
        offset.writeOffsets(polDeg, [factRArmA, factRLeg, factLLeg, factLArmA, factTorso], True)
    except Exception,e:
        error.abort("Offset write unsuccessfull", "not valid arguments as parameters to function","OffsetFileFunc", "Calibrate")
    print "Done"
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    polDeg   = 2 #Polinomio grado 2 por defecto
    humanDir = ""

    if len(sys.argv) <= 1:
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Default Quadratic Regression"
        print "Human data directory not specified, default directory .../Cal/Human"
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        print "Starting calibration process..."
    elif len(sys.argv) == 2:
        try:
            polDeg = int(sys.argv[1])
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "Human data directory not specified, default directory .../Cal/Human"
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "Starting calibration process..."
        except ValueError as e:
            error.abort("Expected int as argument in main function", "Calibrate")
    elif len(sys.argv) == 3:
        try:
            polDeg = int(sys.argv[1])
            humanDir = sys.argv[2]
            print "++++++++++++++++++++++++++++++++++++"
            print "Using Pol degree:", polDeg
            print "Reading Human dat from dir:", humanDir
            print "Starting calibration process..."
            print "++++++++++++++++++++++++++++++++++++"
        except ValueError as e:
            error.abort("Expected int as argument in main function", "Calibrate")

    time.sleep(1.0)
    main(polDeg, humanDir)
