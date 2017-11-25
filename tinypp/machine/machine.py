from ProgramLoader import *
from os import sys
#TEST
if __name__ == '__main__':
	if len(sys.argv) > 1:
		ruta = sys.argv[1]
		pl = ProgramLoader(ruta)
		pl.run()
	else:
		print("No se encontro el parametro del archivo a ejecutar")