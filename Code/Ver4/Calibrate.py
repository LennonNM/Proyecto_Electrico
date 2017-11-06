import sys
import CalibrateFunc as cal
import abortFunc
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main(polDeg):
#Realiza la calibracion segun las grabaciones de datos para calibrar dentro del
#directorio local ../Cal/
    ##Obtiene datos desde los csv correspondientes para la primer pose de calibracion
    RArmNao,RLegNao,LLegNao,LArmNao,TorsoNao,HeadNao,RArmP,RLegP,LLegP,LArmP,TorsoP,HeadP = cal.getCalData("PosA_Mod.csv","PruebaA_Mod.csv")
    ##Obtiene factores para la regresion polinomial deseada para el ajuste
    #polDeg = 1 #regresion lineal
    polDeg = 2 #polinomio de grado 2
    factRArmA  = cal.getTerms(RArmNao, RArmP, polDeg)
    factRLegA  = cal.getTerms(RLegNao, RLegP, polDeg)
    factLLegA  = cal.getTerms(LLegNao, LLegP, polDeg)
    factLArmA  = cal.getTerms(RArmNao, LArmP, polDeg)
    factTorsoA = cal.getTerms(TorsoNao, TorsoP, polDeg)
    factHeadA  = cal.getTerms(HeadNao, HeadP, polDeg)
    ##Repite pasos anteriores para cada una de las poses usadas para la calibracion


    #---------------------------------------------------------------------------
    ##Obtiene ajuste general aplicable a todas las poses involucradas
    #xRArm = cal.setAdjustAct()
    #yRArm = cal.setAdjustAct()
    #zRArm = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xRLeg = cal.setAdjustAct()
    #yRLeg = cal.setAdjustAct()
    #zRLeg = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xLLeg = cal.setAdjustAct()
    #yLLeg = cal.setAdjustAct()
    #zLLeg = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xLArm = cal.setAdjustAct()
    #yLArm = cal.setAdjustAct()
    #zLArm = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xTorso = cal.setAdjustAct()
    #yTorso = cal.setAdjustAct()
    #zTorso = cal.setAdjustAct()
    #---------------------------------------------------------------------------
    #xHead = cal.setAdjustAct()
    #yHead = cal.setAdjustAct()
    #zHead = cal.setAdjustAct()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    polDeg = 2

    if len(sys.argv) <= 1:
        print "Default Linear Regression"
        print "Starting calibration process..."
    elif len(sys.argv) == 2:
        try:
            polDeg = int(sys.argv[1])
        except ValueError as e:
            abortFunc.abort("Expected int as argument in main function", "Calibrate")
            
    time.sleep(1.0)
    main(polDeg)
