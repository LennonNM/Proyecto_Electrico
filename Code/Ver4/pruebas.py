import Calibrate

RArmNao,RLegNao,LLegNao,LArmNao,TorsoNao,HeadNao,RArmP,RLegP,LLegP,LArmP,TorsoP,HeadP = Calibrate.getCalData("PosA_Mod.csv","PruebaA_Mod.csv")
factRArm = Calibrate.startCalibrate(RArmNao, RArmP, 2)
print (factRArm)
