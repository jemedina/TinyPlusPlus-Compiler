from os import sys
from Mnemonics import Mnemonics
#Clase para guardar las instrucciones
class Instruction:
	'''
	Constructor recibe
	la linea y obtiene 
	los argumentos
	line por default es None
	'''
	def __init__(self,line=None):
		#NOTA: iop, arg1,arg2 y arg3 son siempre strings
		self.iop = Mnemonics.HALT
		self.arg1 = None
		self.arg2 = None
		self.arg3 = None

		if line != None:
			#Separar en partes la instruccion
			#en posicion [0] se guarda el numero
			#de linea, y el [1] es el resto del comando
			lineParts = line.split(":")

			#Guardar el numero de la linea
			#como atributo de este objeto

			#Este atributo si es entero
			#ya que en el diccionario las llaves serán enteros
			self.lineNo = int(lineParts[0].strip())

			#Guardar en otra variable el resto de la instruccion
			instruction = lineParts[1].strip()

			'''
			Separar la instruccion por sus 2 espacios
			en el [0] sería el mnemonico
			y en [1] serían los parametros
			'''
			#IMPORTANTE: notar que entre el mnemonico
			#y sus parametros debe haber 2 espacios siempre
			instructionParts = instruction.split("  ")

			mnemonic = instructionParts[0]
			params = instructionParts[1]
			#Verificar que el mnemonico esté en la lista
			#de mnemonicos
			if not mnemonic in Mnemonics.ALL_MNEMONICS:
				print("TM Error: no se reconoce el mnemonico <"+mnemonic+"> en linea TM:" + self.lineNo,file=sys.stderr) 
				exit(1)
			else:
				self.iop = mnemonic

			
			self.isRMorRA = ("(" in params) and (")" in params)
			self.isRR = not self.isRMorRA

			#Si es RA sacar los parametros sabiendo que hay un parentesis
			if self.isRMorRA:
				commaSeparated = params.split(",")

				#almacenar el argumento 1
				self.arg1 = int(commaSeparated[0].strip())
				parenthesisPart = commaSeparated[1]
				parenthesisSeparated = parenthesisPart.split("(")
				
				#Almacenar el argumento 2
				self.arg2 = int(parenthesisSeparated[0].strip())
				
				#Almacenar el argumento 3
				self.arg3 = int(parenthesisSeparated[1].split(")")[0].strip())

			else: #Es RM (Solo separado por commas)
				commaSeparated = params.split(",")
				self.arg1 = int(commaSeparated[0].strip())
				self.arg2 = int(commaSeparated[1].strip())
				self.arg3 = int(commaSeparated[2].strip())

	def __str__(self):
		return str(self.lineNo) + ": "+str(self.iop) + " " + str(self.arg1)+ " - " + str(self.arg2) + " - " + str(self.arg3)