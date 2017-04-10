from LexerSourceNotFoundException import LexerSourceNotFoundException

class LexerFileHandler:
	eof = False
	def __init__(self,sourcePath):
		self.sourcePath = sourcePath
		self.col = -1
		self.row = 0
		self.fileContent = []
		self.file = None
		try:
			self.load()
		except IOError as e:
			raise LexerSourceNotFoundException("Lexer can't open the file ["+sourcePath+"] or it doesn't exists")

	def open(self):
		self.file = open(self.sourcePath,"r")

	def load(self):
		self.open()
		for line in self.file:
			self.fileContent.append(line)
		if len(self.fileContent) == 0:
			self.eof = True
	def next(self):
		if(len(self.fileContent) > 0 and self.col < (len(self.fileContent[self.row])-1)):
			self.col+=1
			return self.fileContent[self.row][self.col]
		else:
			if(self.row < (len(self.fileContent)-1)):
				self.row+=1
				self.col=0
				return self.fileContent[self.row][self.col]
			else:
				self.eof = True
				return None
					
	def resetPointer(self):
		self.col = -1
		self.row = 0

	def getCurrentValue(self):
		if self.eof:
			return None
		else:

			return self.fileContent[self.row][self.col]

	def close(self):
		self.file.close()

	def isEOF(self):
		return self.eof

	def previous(self):
		if self.eof:
			self.eof = False
		else:
			if self.col-1 >= 0:
				self.col-=1
			else:
				self.row-=1
				self.col = len(self.fileContent[self.row])-1