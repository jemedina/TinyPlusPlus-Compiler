from os import sys
from Machine import Machine

'''
	Metodo principal (main)
	Se debe mandar como parametro
	el archivo del codigo objeto
	generado con el siguiente
	formato:

	> python main.py <arhivo_objeto>
'''
if __name__ == '__main__':
	#Verificar que exista el argumento del archivo objeto
	if len(sys.argv) > 1:

		#Leer el archivo de programa
		pgm_path = sys.argv[1]
		try:
			pgm = open(pgm_path,"r")
		except:
			print("TM Error: no se existe el archivo '"+pgm_path+"'",file=sys.stderr)
			exit(1)

		machine = Machine(pgm)
		machine.run()
	else:
		print("TM Error: formato del programa 'python main.py <arhivo_objeto>'")
		