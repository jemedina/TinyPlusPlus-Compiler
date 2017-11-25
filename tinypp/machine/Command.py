class Command:
	DEFINE = 'DEFINE'
	START = 'START'
	END = 'END'
	PUSH = 'PUSH'
	RD = 'RD'
	ADD = 'ADD'
	MUL = 'MUL'
	DIFF = 'DIFF'
	DIV = 'DIV'
	ASSIGN = 'ASSIGN'
	WR = 'WR'
	GT = 'GT'
	LT = 'LT'
	EQ = 'EQ'
	GE = 'GE'
	LE = 'LE'
	JT = 'JT'
	JF = 'JF'
	J = 'J'
	"""docstring for Command"""
	def __init__(self, cmd):
		self.genCommand(cmd)
		
	def genCommand(self, cmd):
		cmd = cmd.replace("\n","")
		components = cmd.split(" ")
		if components[0][0] == '#':
			components[0] = components[0][:-1]
		self.name = components[0] #Obtener el nombre del comando
		self.argument = components[1] if len(components) > 1 else None

		if len(components) > 2:
			self.type = components[2]

	def getPureArgument(self):
		return self.argument[1:]

