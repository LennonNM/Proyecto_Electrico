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
    ##Cal A
    ###Obtiene datos desde los csv correspondientes para la primer pose de calibracion
    RArmNaoA,RLegNaoA,LLegNaoA,LArmNaoA,TorsoNaoA,HeadNaoA,RArmPA,RLegPA,LLegPA,LArmPA,TorsoPA,HeadPA = cal.setCalData("A_Cal_NAO.csv",humanDir + "A_Cal_P.csv")
    ##Obtiene factores para la regresion polinomial deseada para el ajuste
    factRArmA  = cal.getTerms(RArmNaoA, RArmPA, polDeg)
    factRLegA  = cal.getTerms(RLegNaoA, RLegPA, polDeg)
    factLLegA  = cal.getTerms(LLegNaoA, LLegPA, polDeg)
    factLArmA  = cal.getTerms(RArmNaoA, LArmPA, polDeg)
    factTorsoA = cal.getTerms(TorsoNaoA, TorsoPA, polDeg)
    factHeadA  = cal.getTerms(HeadNaoA, HeadPA, polDeg)

    ##Repite pasos anteriores para cada una de las poses usadas para la calibracion
    ##de los brazos
    ##Cal B
    RArmNaoB,RLegNaoB,LLegNaoB,LArmNaoB,TorsoNaoB,HeadNaoB,RArmPB,RLegPB,LLegPB,LArmPB,TorsoPB,HeadPB = cal.setCalData("A_Cal_NAO.csv",humanDir + "A_Cal_P.csv")
    factRArmB  = cal.getTerms(RArmNaoB, RArmPB, polDeg)
    factRLegB  = cal.getTerms(RLegNaoB, RLegPB, polDeg)
    factLLegB  = cal.getTerms(LLegNaoB, LLegPB, polDeg)
    factLArmB  = cal.getTerms(RArmNaoB, LArmPB, polDeg)
    factTorsoB = cal.getTerms(TorsoNaoB, TorsoPB, polDeg)
    factHeadB  = cal.getTerms(HeadNaoB, HeadPB, polDeg)

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
    print "Writing offsets to default: .../Cal/Offsets/offsets.csv"
    try:
        offset.writeOffsets(polDeg, [factRArmA,factRLegA, factLLegA, factLArmA, factTorsoA, factHeadA])
    except Exception,e:
        error.abort("Offset write unsuccessfull", "not valid arguments received","OffsetFileFunc", "Calibrate")

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    polDeg   = 2 #Polinomio grado 2 por defecto
    humanDir = ""

    if len(sys.argv) <= 1:
        print "Default Quadratic Regression"
        print "Human data directory not specified, default directory .../Cal/Human"
        print "Starting calibration process..."
    elif len(sys.argv) == 2:
        try:
            polDeg = int(sys.argv[1])
            print "Human data directory not specified, default directory .../Cal/Human"
            print "Starting calibration process..."
        except ValueError as e:
            error.abort("Expected int as argument in main function", "Calibrate")
    elif len(sys.argv) == 3:
        try:
            polDeg = int(sys.argv[1])
            humanDir = sys.argv[2]
            print "Using Pol degree:", polDeg
            print "Reading Human dat from dir:", humanDir
            print "Starting calibration process..."
        except ValueError as e:
            error.abort("Expected int as argument in main function", "Calibrate")

    time.sleep(1.0)
    main(polDeg, humanDir)
