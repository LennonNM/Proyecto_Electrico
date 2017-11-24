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
def main(polDeg, humanDir, naoDir):
    #Datos para calibrar el movimiento de los brazos
    ###Obtiene datos desde los csv correspondientes para la primer pose de calibracion
    RArmNaoA,RLegNaoA,LLegNaoA,LArmNaoA,TorsoNaoA,HeadNaoA,RArmPA,RLegPA,LLegPA,LArmPA,TorsoPA,HeadPA = cal.setCalData( naoDir + "/" + "Brazos_NAO.csv", humanDir + "/" + "Brazos.csv",True)
    ##Obtiene factores para la regresion polinomial deseada para el ajuste
    print RArmPA[0]
    factRArmA  = cal.getTerms(RArmNaoA, RArmPA, polDeg, True)
    factLArmA  = cal.getTerms(RArmNaoA, LArmPA, polDeg, True)

    ##Repite pasos anteriores para cada una de las poses usadas para los demas actuadores
    ###Pierna derecha
    RArmNaoB,RLegNaoB,LLegNaoB,LArmNaoB,TorsoNaoB,HeadNaoB,RArmPB,RLegPB,LLegPB,LArmPB,TorsoPB,HeadPB = cal.setCalData( naoDir + "/" + "PiernaD_NAO.csv", humanDir + "/" + "PiernaD.csv",True)
    factRLeg  = cal.getTerms(RLegNaoB, RLegPB, polDeg, True)
    ###Pierna izquierda
    RArmNaoC,RLegNaoC,LLegNaoC,LArmNaoC,TorsoNaoC,HeadNaoC,RArmPC,RLegPC,LLegPC,LArmPC,TorsoPC,HeadPC = cal.setCalData( naoDir + "/" + "PiernaI_NAO.csv", humanDir + "/" + "PiernaI.csv",True)
    factLLeg  = cal.getTerms(RLegNaoB, RLegPB, polDeg, True)
    ###Pierna Torso
    RArmNaoD,RLegNaoD,LLegNaoD,LArmNaoD,TorsoNaoD,HeadNaoD,RArmPD,RLegPD,LLegPD,LArmPD,TorsoPD,HeadPD = cal.setCalData( naoDir + "/" + "Torso_NAO.csv", humanDir + "/" + "Torso.csv",True)
    factTorso  = cal.getTerms(RLegNaoB, RLegPB, polDeg, True)

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #Genera archivo CSV con los offsets finales a utilizar
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Writing offsets to default: .../Cal/Offsets/offsets.csv"
    try:
        offset.writeOffsets(polDeg, [factRArmA, factRLeg, factLLeg, factLArmA, factTorso], True)
    except Exception,e:
        error.abort("Offset write unsuccessfull", "not valid parameters to function","OffsetFileFunc", "Calibrate")
    print "Done"
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    polDeg   = 2 #Polinomio grado 2 por defecto
    humanDir = ""
    naoDir = ""

    if len(sys.argv) == 4:
        try:
            polDeg = int(sys.argv[1])
            humanDir = sys.argv[2]
            naoDir = sys.argv[3]
            print "++++++++++++++++++++++++++++++++++++"
            print "Using Pol degree:", polDeg
            print "Reading Human data from dir:", humanDir
            print "Reading NAO data from dir:", naoDir
            print "------------------------------------"
            print "Starting calibration process..."
            print "++++++++++++++++++++++++++++++++++++"
        except ValueError as e:
            error.abort("Expected int as argument in main function", "Calibrate")
    else:
        error.abort("Expected 3 arguments on call.", "Calibrate")

    time.sleep(1.0)
    main(polDeg, humanDir, naoDir)
