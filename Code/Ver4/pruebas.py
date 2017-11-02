import Calibrate

RArmNao,RLegNao,LLegNao,LArmNao,TorsoNao,HeadNao,RArmP,RLegP,LLegP,LArmP,TorsoP,HeadP = Calibrate.getCalData("PosA.csv","PruebaA.csv")
Calibrate.startCalibrate()
