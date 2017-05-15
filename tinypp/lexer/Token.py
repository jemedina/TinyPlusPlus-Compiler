class Token:
	"""docstring for Token"""
	def __init__(self, tipo, lexema,row=0,col=0):
		self.tipo = tipo
		self.lexema = lexema
		self.row = row
		self.col = col
	def __str__(self):
		return self.tipo+"# "+self.lexema+" #"+str(self.row)+"#"+str(self.col)