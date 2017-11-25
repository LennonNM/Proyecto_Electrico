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
def main(polDeg, humanDir, naoDir, wRot):
    #Datos para calibrar el movimiento de los brazos
    ###Obtiene datos desde los csv correspondientes para la primer pose de calibracion
    RArmNaoA,RLegNaoA,LLegNaoA,LArmNaoA,TorsoNaoA,HeadNaoA,RArmPA,RLegPA,LLegPA,LArmPA,TorsoPA,HeadPA = cal.setCalData( naoDir + "/" + "Brazos_NAO.csv", humanDir + "/" + "Brazos_P.csv", wRot)
    ##Obtiene factores para la regresion polinomial deseada para el ajuste
    factRArm  = cal.getTerms(RArmNaoA, RArmPA, polDeg, wRot)
    factLArm  = cal.getTerms(LArmNaoA, LArmPA, polDeg, wRot)



    ##Repite pasos anteriores para cada una de las poses usadas para los demas actuadores
    ###Pierna derecha
    RArmNaoB,RLegNaoB,LLegNaoB,LArmNaoB,TorsoNaoB,HeadNaoB,RArmPB,RLegPB,LLegPB,LArmPB,TorsoPB,HeadPB = cal.setCalData( naoDir + "/" + "PiernaD_NAO.csv", humanDir + "/" + "PiernaD_P.csv", wRot)
    factRLeg  = cal.getTerms(RLegNaoB, RLegPB, polDeg, wRot)
    ###Pierna izquierda
    RArmNaoC,RLegNaoC,LLegNaoC,LArmNaoC,TorsoNaoC,HeadNaoC,RArmPC,RLegPC,LLegPC,LArmPC,TorsoPC,HeadPC = cal.setCalData( naoDir + "/" + "PiernaI_NAO.csv", humanDir + "/" + "PiernaI_P.csv", wRot)
    factLLeg  = cal.getTerms(LLegNaoB, LLegPB, polDeg, wRot)
    ###Pierna Torso
    RArmNaoD,RLegNaoD,LLegNaoD,LArmNaoD,TorsoNaoD,HeadNaoD,RArmPD,RLegPD,LLegPD,LArmPD,TorsoPD,HeadPD = cal.setCalData( naoDir + "/" + "Torso_NAO.csv", humanDir + "/" + "Torso_P.csv", wRot)
    factTorso  = cal.getTerms(TorsoNaoB, TorsoPB, polDeg, wRot)

    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    #Genera archivo CSV con los offsets finales a utilizar
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Writing offsets to default: .../Cal/Offsets/offsets.csv"
    try:
        offset.writeOffsets(polDeg, [factRArm, factRLeg, factLLeg, factLArm, factTorso],  wRot)
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
    wRot = "yes"

    if len(sys.argv) == 5:
        try:
            polDeg = int(sys.argv[1])
            humanDir = sys.argv[2]
            naoDir = sys.argv[3]
            wRot = (sys.argv[4]).lower()
            print "++++++++++++++++++++++++++++++++++++"
            print "Using Pol degree:", polDeg
            print "Include rotations:", wRot
            print "Reading Human data from dir:", humanDir
            print "Reading NAO data from dir:", naoDir
            print "------------------------------------"
            print "Starting calibration process..."
            print "++++++++++++++++++++++++++++++++++++"
        except ValueError as e:
            error.abort("Expected int as argument in main function", None,"Calibrate")
    else:
        error.abort("Expected 4 arguments on call.", None, "Calibrate")

    time.sleep(1.0)
    main(polDeg, humanDir, naoDir, wRot)
