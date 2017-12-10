from os import sys
from enum import Enum
from Instruction import Instruction 
from Mnemonics import Mnemonics

#Constantes globales:
IADDR_SIZE = 1024 #Variable depreciada ya que usamos diccionados B)
DADDR_SIZE = 1024
NO_REGS = 8
PC_REG = 7

class STEPRESULT(Enum):
	OKAY = 1
	HALT = 2
	IMEM_ERR = 3
	DMEM_ERR = 4
	ZERODIVIDE = 5



class Machine:
	def __init__(self,pgm):
		#Guardar archivo de programa
		self.pgm = pgm
		#Definicion de memoria
		self.dMem = []
		#Definicion de los registros
		self.reg = []
		#Instrucciones de memoria (diccionario)
		self.iMem = dict()


		self.readInstructions()

	def readInstructions(self):
		#inicializar la memoria:
		'''
		  dMem[0] = DADDR_SIZE - 1 ;
		  for (loc = 1 ; loc < DADDR_SIZE ; loc++)
		      dMem[loc] = 0 ;
		'''
		self.dMem = [0 for x in range(0,DADDR_SIZE)]
		self.dMem[0] = DADDR_SIZE -1

		#inicializar los registros
		'''
		  for (regNo = 0 ; regNo < NO_REGS ; regNo++)
		      reg[regNo] = 0 ;
		'''
		self.reg = [0 for x in range(0,NO_REGS)]


		for line in self.pgm:
			instruction = Instruction(line)
			self.iMem[instruction.lineNo] = instruction
	
	#Metodo para comenzar la ejecucion de las instrucciones
	'''
			stepResult = srOKAY;
	  if ( stepcnt > 0 )
	  { if ( cmd == 'g' )
	    { stepcnt = 0;
	      while (stepResult == srOKAY)
	      { iloc = reg[PC_REG] ;
	        if ( traceflag ) writeInstruction( iloc ) ;
	        stepResult = stepTM ();
	        stepcnt++;
	      }
	      if ( icountflag )
	        printf("Number of instructions executed = %d\n",stepcnt);
	    }'''
	    
	def run(self):
		stepResult = STEPRESULT.OKAY
		while(stepResult == STEPRESULT.OKAY):
			stepResult = self.stepTM()

	def stepTM(self):

		
		pc = self.reg[PC_REG]
		self.reg[PC_REG] = pc+1

		currentinstruction = self.iMem[ pc ]
		#print(str(currentinstruction))
		if currentinstruction.isRR:
			r = currentinstruction.arg1
			s = currentinstruction.arg2
			t = currentinstruction.arg3
		else: #isRMorRA
			r = currentinstruction.arg1
			s = currentinstruction.arg3
			m = currentinstruction.arg2 + self.reg[s]

		#Evaluar cada mnemonico
		if currentinstruction.iop == Mnemonics.HALT:
			print("HALT: "+str(r)+","+str(s)+","+str(t))
			return STEPRESULT.HALT
		elif currentinstruction.iop == Mnemonics.IN:
			in_Line=input("Enter value for IN instruction: ")
			try:
				self.reg[r] = int(in_Line)
			except:
				print("TM Error: Illegal value",file=sys.stderr)
		elif currentinstruction.iop == Mnemonics.OUT:
			print("OUT instruction prints: "+ str(self.reg[r]))
		elif currentinstruction.iop == Mnemonics.ADD:
			self.reg[r] = self.reg[s] + self.reg[t]
		elif currentinstruction.iop == Mnemonics.SUB:
			self.reg[r] = self.reg[s] - self.reg[t]
		elif currentinstruction.iop == Mnemonics.MUL:
			self.reg[r] = self.reg[s] * self.reg[t]
		elif currentinstruction.iop == Mnemonics.DIV:
			if self.reg[t] != 0:
				self.reg[r] = self.reg[s] / self.reg[t]
			else:
				return STEPRESULT.ZERODIVIDE
		elif currentinstruction.iop == Mnemonics.LD:
			self.reg[r] = self.dMem[m]
		elif currentinstruction.iop == Mnemonics.ST:
			self.dMem[m] = self.reg[r]
		elif currentinstruction.iop == Mnemonics.LDA:
			self.reg[r] = m
		elif currentinstruction.iop == Mnemonics.LDC:
			self.reg[r] = currentinstruction.arg2
		elif currentinstruction.iop == Mnemonics.JLT:
			if self.reg[r] <  0 :
				self.reg[PC_REG] = m
		elif currentinstruction.iop == Mnemonics.JLE:
			if self.reg[r] <=  0 :
				self.reg[PC_REG] = m
		elif currentinstruction.iop == Mnemonics.JGT:
			if self.reg[r] >  0 :
				self.reg[PC_REG] = m
		elif currentinstruction.iop == Mnemonics.JGE:
			if self.reg[r] >=  0 :
				self.reg[PC_REG] = m
		elif currentinstruction.iop == Mnemonics.JEQ:
			if self.reg[r] ==  0 :
				self.reg[PC_REG] = m
		elif currentinstruction.iop == Mnemonics.JNE:
			if self.reg[r] != 0 :
				self.reg[PC_REG] = m
		return STEPRESULT.OKAY
