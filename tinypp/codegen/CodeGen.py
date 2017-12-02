import ntpath

STATEMENTS = [':=', 'if', 'repeat', 'while','cout','cin','break']
BOOL_OPERATORS = ['>', '<', '>=', '<=', '==', '!=']
MATH_OPERATORS = ['+', '-', '*', '/']

class CodeGen:

	"""docstring for CodeGen"""
	def __init__(self,syntaxTree,hashTable,filename):
		self.filename = filename
		self.tagindex = 1000
		self.syntaxTree = syntaxTree
		self.hashTable = hashTable
		self.buffer = ""
		self.lastEndTag = None
		#hashTable.cliDisplayTable()
		self.buildDefinitions()
		self.writeCommand("START")
		self.buildBody()
		self.writeCommand("END")
		self.showBuffer()
		self.writeBuffer()

	def buildDefinitions(self):
		for key in self.hashTable.table:
			var = self.hashTable.table[key]
			self.writeCommand("DEFINE "+key+" "+var.type)

	def buildBody(self):
		if len(self.syntaxTree.sons) > 1:
			self.tree = self.syntaxTree.sons[1]
		elif self.syntaxTree.sons[0].name not in ['int','real','boolean']:
			self.tree = self.syntaxTree.sons[0]
		else:
			return
		
		self.eval(self.tree)

	def eval(self, r):
		if r.name == 'cin':
			self.writeCommand("RD @"+r.sons[0].name)
		elif r.name == 'cout':
			self.eval(r.sons[0])
			self.writeCommand("WR")
		elif r.name in MATH_OPERATORS or r.name in BOOL_OPERATORS:
			self.eval(r.sons[1])
			self.eval(r.sons[0])

			if r.name == '+':
				self.writeCommand("ADD")
			elif r.name == '-':
				self.writeCommand("DIFF")
			elif r.name == '*':
				self.writeCommand("MUL")
			elif r.name == '/':
				self.writeCommand("DIV")
			elif r.name == '==':
				self.writeCommand("EQ")
			elif r.name == '>=':
				self.writeCommand("GE")
			elif r.name == '<=':
				self.writeCommand("LE")
			elif r.name == '>':
				self.writeCommand("GT")
			elif r.name == '<':
				self.writeCommand("LT")
		elif r.name == 'if':
			self.eval(r.sons[0])
			tagTrue = self.genTag()
			tagFalse = self.genTag()
			tagEnd = self.genTag()

			self.writeCommand("JT "+tagTrue)
			self.writeCommand("JF "+tagFalse)

			self.writeCommand(tagTrue+":")
			self.eval(r.sons[1])
			self.writeCommand("J "+tagEnd)
			self.writeCommand(tagFalse+":")
				
			if len(r.sons) > 2:
				self.eval(r.sons[2])

			self.writeCommand(tagEnd+":")

		elif r.name == 'while':
			tagEval = self.genTag()
			tagBody = self.genTag()
			tagEnd = self.genTag()
			self.lastEndTag = tagEnd
			self.writeCommand(tagEval+":")
			self.eval(r.sons[0])
			self.writeCommand("JT "+tagBody)
			self.writeCommand("JF "+tagEnd)

			self.writeCommand(tagBody+":")
			self.eval(r.sons[1])
			self.writeCommand("J "+tagEval)
			
			self.writeCommand(tagEnd+":")
			self.lastEndTag = None
		elif r.name == 'repeat':
			tagBody = self.genTag()
			tagEnd = self.genTag()
			self.lastEndTag = tagEnd

			self.writeCommand(tagBody+":")
			self.eval(r.sons[0])

			self.eval(r.sons[1])
			self.writeCommand("JF "+tagBody)
			self.writeCommand("JT "+tagEnd)
			
			self.writeCommand(tagEnd+":")
			
			self.lastEndTag = None
		elif r.name == 'break':
			if self.lastEndTag != None:
				self.writeCommand("J " + self.lastEndTag)

		elif r.name == ':=':
			self.eval(r.sons[1])
			self.writeCommand('ASSIGN @'+r.sons[0].name)
			
		elif r.name.isdigit() or self.isFloat(r.name):
			self.writeCommand("PUSH "+r.name)
		
		elif not r.name.isdigit(): #Is identificador
			self.writeCommand("PUSH @"+r.name)

	
		if r.bro != None:
			self.eval(r.bro)

	def writeCommand(self,cmd):
		self.buffer += cmd + '\n'

	def showBuffer(self):
		print(self.buffer)

	def genTag(self):
		tg = '#'+str(self.tagindex)
		self.tagindex += 1
		return tg

	def isFloat(self, strs):
		try:
			return float(strs) and '.' in strs
		except ValueError:
			return False

	def writeBuffer(self):
		canonicalFileName = ntpath.basename(self.filename)
		fpath = ntpath.abspath(canonicalFileName)
		fpath = "\\".join(fpath.split("\\")[:-1])+"\\code.ox"
		
		f = open(fpath,'+w')
		print(self.buffer, file=f,end='')

