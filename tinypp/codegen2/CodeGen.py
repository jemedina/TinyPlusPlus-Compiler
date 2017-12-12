import ntpath

STATEMENTS = [':=', 'if', 'repeat', 'while','cout','cin','break']
BOOL_OPERATORS = ['>', '<', '>=', '<=', '==', '!=']
MATH_OPERATORS = ['+', '-', '*', '/']

class CodeGen:

	"""docstring for CodeGen"""
	def __init__(self,semanticTree,hashTable,filename):
		self.filename = filename
		self.semanticTree = semanticTree
		self.hashTable = hashTable
		self.buffer = ""
		self.lastEndTag = None
		#Variables de emisión
		self.emitLoc = 0
		self.highEmitLoc=0 #localidada TM mas alta que se puede alzanar para usarla junto con emitSkip, emitBackup y emitRestore

		self.pc=7 #contador del programa 
		self.mp=6 #apuntador de memoria
		self.gp=5 #apuntador global
		self.ac=0 #acumulador
		self.ac1=1 #segundo acumulador
		self.tmpOffset = 0
		self.inloop = False;

		self.breakActive = False

		#hashTable.cliDisplayTable()
		self.buildDefinitions()
		self.buildBody()
		print(self.buffer)
		self.writeBuffer()
	def buildDefinitions(self):
		for key in self.hashTable.table:
			var = self.hashTable.table[key]
			self.emit("DEFINE:  "+key+","+var.type+","+str(var.memory))
	def emit(self,anything):
		self.buffer += anything + '\n'

	def emitRM(self,op,r,d,s):
		self.buffer +=str(self.emitLoc)+": "+str(op)+"  "+str(r)+","+str(d)+"("+str(s)+")\n"
		self.emitLoc+=1

	def emitRO(self,op,r,s,t):
		self.buffer += str(self.emitLoc)+": "+str(op)+"  "+str(r)+","+str(s)+","+str(t)+"\n"
		self.emitLoc+=1

	def buildBody(self):
		if len(self.semanticTree["sons"]) > 1:
			self.tree = self.semanticTree["sons"][1]
		elif self.semanticTree["sons"][0]["name"] not in ['int','real','boolean']:
			self.tree = self.semanticTree["sons"][0]
		else:
			return		
		
		self.emitRM("LD",self.mp,0,self.ac)# * load maxaddress from location 0
		self.emitRM("ST",self.ac,0,self.ac)# * clear location 0"
		self.eval(self.tree)
		self.emitRO("HALT",0,0,0)

	def eval(self, r):
		if r["name"] == 'cout':
			self.eval(r["sons"][0])
			self.emitRO("OUT",self.ac,0,0)
		
		elif r["name"] == 'coutln':
			if len(r["sons"]) > 0:
				self.eval(r["sons"][0])
			else:
				self.emitRM("LDC",self.ac,"*",self.ac)
			self.emitRO("OUTLN",self.ac,0,0)

		elif r["name"] == 'cin':
			dataType = self.hashTable.getKey(r["sons"][0]["name"]).type
			if dataType == None or dataType == 'int':
				self.emitRO("IN",self.ac,0,0)
			elif dataType == 'real':
				self.emitRO("INR",self.ac,0,0)
			elif dataType == 'boolean':
				self.emitRO("INB",self.ac,0,0)
			loc = self.hashTable.getKey(r["sons"][0]["name"]).memory
			self.emitRM("ST",self.ac,loc,self.gp)

		elif r["name"] == ':=':
			self.eval(r["sons"][1])
			loc = self.hashTable.getKey(r["sons"][0]["name"]).memory
			self.emitRM("ST",self.ac,loc,self.gp)
		elif r["name"] == "if":
			self.eval(r["sons"][0])
			savedLoc1 = self.emitSkip(1)

			self.eval(r["sons"][1])
			savedLoc2 = self.emitSkip(1)
			currentLoc = self.emitSkip(0) 
			self.emitBackup(savedLoc1)
			self.emitRM_Abs("JEQ",self.ac,currentLoc)
			self.emitRestore()
			if len(r["sons"]) > 2:
				self.eval(r["sons"][2])
			currentLoc = self.emitSkip(0)
			self.emitBackup(savedLoc2)
			self.emitRM_Abs("LDA",self.pc,currentLoc)
			self.emitRestore() 
		elif r["name"] == "repeat":
			savedLoc1 = self.emitSkip(0)
			self.eval(r["sons"][0])
			self.eval(r["sons"][1])
			
			if self.breakActive:
				currentLoc = self.emitSkip(0)
				self.emitBackup(self.breakLoc)
				self.emitRM_Abs("LDA",self.pc,currentLoc+1)
				self.breakActive = False
				self.emitRestore()
			self.emitRM_Abs("JEQ",self.ac,savedLoc1)

		elif r["name"] == "while":
			locTest = self.emitSkip(0)
			self.eval(r["sons"][0])
			locBody = self.emitSkip(1)
			self.eval(r["sons"][1])
			currentLoc = self.emitSkip(0) 
			self.emitBackup(locBody)
			self.emitRM_Abs("JEQ",self.ac,currentLoc+1)
			if self.breakActive:
				self.emitBackup(self.breakLoc)
				self.emitRM_Abs("LDA",self.pc,currentLoc+1)
				self.breakActive = False
			self.emitRestore()
			self.emitRM_Abs("LDA",self.pc,locTest)
		elif r["name"] == "break":
			self.breakActive = True
			self.breakLoc = self.emitSkip(1)
		elif r["name"] in MATH_OPERATORS or r["name"] in BOOL_OPERATORS:
			self.eval(r["sons"][0])
			self.emitRM("ST",self.ac,self.tmpOffset,self.mp)
			self.tmpOffset -= 1

			self.eval(r["sons"][1])
			self.tmpOffset += 1
			self.emitRM("LD",self.ac1,self.tmpOffset,self.mp)
			if r["name"] == '+':
				self.emitRO("ADD",self.ac,self.ac1,self.ac)
			elif r["name"] == '-':
				self.emitRO("SUB",self.ac,self.ac1,self.ac)
			elif r["name"] == '*':
				self.emitRO("MUL",self.ac,self.ac1,self.ac)
			elif r["name"] == '/':
				self.emitRO("DIV",self.ac,self.ac1,self.ac)

			elif r["name"] == "<":
				self.emitRO("SUB",self.ac,self.ac1,self.ac) 
				self.emitRM("JLT",self.ac,2,self.pc) 
				self.emitRM("LDC",self.ac,0,self.ac) 
				self.emitRM("LDA",self.pc,1,self.pc) 
				self.emitRM("LDC",self.ac,1,self.ac)
			elif r["name"] == "<=":
				self.emitRO("SUB",self.ac,self.ac1,self.ac) 
				self.emitRM("JLE",self.ac,2,self.pc) 
				self.emitRM("LDC",self.ac,0,self.ac) 
				self.emitRM("LDA",self.pc,1,self.pc) 
				self.emitRM("LDC",self.ac,1,self.ac)
			elif r["name"] == ">":
				self.emitRO("SUB",self.ac,self.ac1,self.ac) 
				self.emitRM("JGT",self.ac,2,self.pc) 
				self.emitRM("LDC",self.ac,0,self.ac) 
				self.emitRM("LDA",self.pc,1,self.pc) 
				self.emitRM("LDC",self.ac,1,self.ac)
			elif r["name"] == ">=":
				self.emitRO("SUB",self.ac,self.ac1,self.ac) 
				self.emitRM("JGE",self.ac,2,self.pc) 
				self.emitRM("LDC",self.ac,0,self.ac) 
				self.emitRM("LDA",self.pc,1,self.pc) 
				self.emitRM("LDC",self.ac,1,self.ac)
			elif r["name"] == "==":
				self.emitRO("SUB",self.ac,self.ac1,self.ac) 
				self.emitRM("JEQ",self.ac,2,self.pc) 
				self.emitRM("LDC",self.ac,0,self.ac) 
				self.emitRM("LDA",self.pc,1,self.pc) 
				self.emitRM("LDC",self.ac,1,self.ac)
			elif r["name"] == "!=":
				self.emitRO("SUB",self.ac,self.ac1,self.ac) 
				self.emitRM("JNE",self.ac,2,self.pc) 
				self.emitRM("LDC",self.ac,0,self.ac) 
				self.emitRM("LDA",self.pc,1,self.pc) 
				self.emitRM("LDC",self.ac,1,self.ac)
			


		elif self.es_id(r["name"]):
			loc = self.hashTable.getKey(r["name"]).memory
			self.emitRM("LD",self.ac,loc,self.gp)

		elif self.es_num(r["name"]):
			self.emitRM("LDC",self.ac,r["name"],0)
		if r["bro"] != None:
			self.eval(r["bro"])

		#elif r.type == ''
#		elif r["name"].isdigit() or self.isFloat(r["name"]):

	def es_id(self,texto):
	    try:
	        if texto[0].isalpha():
	            if texto in STATEMENTS:
	                return False
	            else:
	                return True
	        else:
	            return False
	    except IndexError:
	        return False

	def es_num(self,texto):
		try:
			float(texto)
			return True
		except ValueError:
			return False
	def emitSkip(self,hm):
	    i=self.emitLoc
	    self.emitLoc+=hm
	    if self.highEmitLoc < self.emitLoc:
	        self.highEmitLoc = self.emitLoc
	    return i

	def emitBackup(self,loc):
		self.emitLoc = loc ;
	
	#convierte una referencia absoluta a una referencia relativa de pc que emite una instruccion RM        
	def emitRM_Abs(self,op,r,a):
		x=a-(self.emitLoc+1)
		self.buffer+=str(self.emitLoc)+":  "+str(op)+"  "+str(r)+","+str(x)+"("+str(self.pc)+")\n"
		self.emitLoc+=1
		if self.highEmitLoc < self.emitLoc:
			self.highEmitLoc = self.emitLoc
	def emitRestore(self):
		self.emitLoc = self.highEmitLoc

	def writeBuffer(self):
		canonicalFileName = ntpath.basename(self.filename)
		fpath = ntpath.abspath(canonicalFileName)
		fpath = "\\".join(fpath.split("\\")[:-1])+"\\code.tm"
		
		f = open(fpath,'+w')
		print(self.buffer, file=f,end='')
