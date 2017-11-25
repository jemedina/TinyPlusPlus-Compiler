from Command import *
from ExecutionStack import *
from Memory import *

class ProgramLoader:
	"""docstring for ProgramLoader"""
	def __init__(self, path):
		program = open(path)
		self.commands = []
		self.pointer = 0
		self.completed = False
		self.stack = ExecutionStack()
		self.memory = Memory()

		for l in program:
			self.commands.append(Command(l))

	def exec(self,command):
		if command.name == Command.START:
			print('Programa iniciado')
		
		elif command.name == Command.END:
			print('Programa completado')
			self.completed = True

		elif command.name == Command.PUSH:
			if self.isVariable(command.argument):
				self.stack.push(self.memory.get(command.getPureArgument()))
			else:
				self.stack.push(command.argument)
		
		elif command.name == Command.RD:
			val = input(command.getPureArgument()+ ' > ')
			self.memory.set(command.getPureArgument(),val)
		
		elif command.name == Command.ADD:
			val = self.stack.pop() + self.stack.pop()
			self.stack.push(val)
	
		elif command.name == Command.MUL:
			val = self.stack.pop() * self.stack.pop()
			self.stack.push(val)
	
		elif command.name == Command.DIV:
			val = self.stack.pop() / self.stack.pop()
			self.stack.push(val)
	
		elif command.name == Command.DIFF:
			val = self.stack.pop() - self.stack.pop()
			self.stack.push(val)

		elif command.name == Command.ASSIGN:
			val = self.stack.pop()
			self.memory.set(command.getPureArgument(),val)

		elif command.name == Command.WR:
			val = self.stack.pop()
			print(val)

		elif command.name == Command.DEFINE:
			self.memory.define(command.argument,command.type)

		elif command.name == Command.GT:
			val = self.stack.pop() > self.stack.pop()
			self.stack.push(val)

		elif command.name == Command.LT:
			val = float(self.stack.pop()) < float(self.stack.pop())
			self.stack.push(val)

		elif command.name == Command.EQ:
			val = self.stack.pop() == self.stack.pop()
			self.stack.push(val)

		elif command.name == Command.GE:
			val = self.stack.pop() >= self.stack.pop()
			self.stack.push(val)

		elif command.name == Command.LE:
			val = self.stack.pop() <= self.stack.pop()
			self.stack.push(val)

		elif command.name == Command.JT:
			val = str(self.stack.last())
			if val == 'True' or val == '1':
				self.stack.pop()
				self.movePointerToTag(command.argument)

		elif command.name == Command.JF:
			val = str(self.stack.last())
			if val == 'False' or val == '0':
				self.stack.pop()
				self.movePointerToTag(command.argument)

		elif command.name == Command.J:
			self.movePointerToTag(command.argument)

		#Tags are ignored, just do a step

		self.nextCommand()

	def run(self):
		while(not self.completed):
			self.exec(self.commands[self.pointer])

	def nextCommand(self):
		self.pointer+=1

	def isVariable(self, arg):
		if '@' in str(arg):
			return True
		else:
			return False

	def movePointerToTag(self, tag):
		i = 0
		for c in self.commands:
			if c.name == tag:
				break
			else:
				i += 1
		self.pointer = i