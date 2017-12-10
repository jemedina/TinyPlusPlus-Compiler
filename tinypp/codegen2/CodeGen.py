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