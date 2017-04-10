class Token:
	"""docstring for Token"""
	def __init__(self, tipo, lexema):
		self.tipo = tipo
		self.lexema = lexema
	def __str__(self):
		return self.tipo+": "+self.lexema