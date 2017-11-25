class Memory:
	"""docstring for Memory"""
	def __init__(self):
		self.memory = dict()
	def define(self, register, ty):
		self.memory[register] = Register(ty)

	def set(self,register, value):
		ty = self.memory[register].type
		if ty == 'int':
			if('.' in str(value)):
				self.memory[register].value = int(str(value).split('.')[0])
			else:
				self.memory[register].value = int(value)
		elif ty == 'float':
			self.memory[register].value = float(value)
		elif ty == 'boolean':
			self.memory[register].value = value

	def get(self,register):
		return self.memory[register].value

class Register:
	def __init__(self,ty):
		self.type = ty
		self.value = 0
