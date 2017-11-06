#Manejo de errores de uso de la aplicacion. Recibe explicacion del error,
#script donde se dio el error, y entrada recibida que ocasiono el error (opcional)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Imports
import sys
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#abort: ocasiona un aborto de la operacion en proceso
def abort(reason, program, value=None):
    if value is not None:
        print "ERROR"
        print value, reason
        print "Aborting program:", program
    else:
        print "ERROR"
        print reason
        print "Aborting program:", program
    sys.exit()
#-------------------------------------------------------------------------------
