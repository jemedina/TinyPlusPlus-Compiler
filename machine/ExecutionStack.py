class ExecutionStack:
	"""docstring for Execution"""
	def __init__(self):
		self.stack = []
	def push(self, val):
		val = str(val)
		if '.' in val:
			self.stack.append(float(val))
		elif val.isdigit() or '-' in val:
			self.stack.append(int(val))
		else:
			self.stack.append(val)
	def pop(self):
		return self.stack.pop()
		
	def last(self):
		return self.stack[len(self.stack)-1]