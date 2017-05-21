from os import sys
class Token:
	def __init__(self,type,content,row=0,col=0):
		self.type = type
		self.content = content
		self.row = row
		self.col = col
	def __str__(self):
		return "{"+self.type+","+self.content+","+self.row+","+self.col+"}"

class TokensHelper:

	def __init__(self,tokensFilePath):
		try:
			self.tokensFile = open(tokensFilePath,"+r")
			self.tokens = []
			self.index = -1
			self.loadTokens()
		except Exception as e:
			print("File ["+tokensFilePath+"] was not found...",file=sys.stderr)
			self.tokensFile = None
			sys.exit(1)

	def loadTokens(self):
		for tokenText in self.tokensFile:
			if tokenText.find("#") > 0:
				tokenInfo = tokenText.split("#")
				identifier = tokenInfo[0].strip()
				content = tokenInfo[1].strip()
				row = tokenInfo[2].strip()
				col = tokenInfo[3].strip()
				newToken = Token(identifier,content,row,col)
				self.tokens.append(newToken)

	def match(self,testChar,byType=False):
		if byType == True:
			if testChar == self.getCurrentToken().type:
				self.getToken()
			else:
				self.error()
		else:
			#print(self.index,self.getCurrentToken(),testChar)
			if testChar == self.getCurrentToken().content:
				self.getToken()
			else:
				self.error()

	def cliDisplayTokens(self):
		for t in self.tokens:
			print(t)
	def error(self):
		print("Syntax error in row = "+self.getCurrentToken().row+", col = "+self.getCurrentToken().col+": "+self.getCurrentToken().content,file=sys.stderr)
	
	def syntaxError(message):
		print("Syntax error at line "+self.getCurrentToken().row+", col = "+self.getCurrentToken().col+": "+message,file=sys.stderr)
		
	def getToken(self):
		self.index += 1
		if self.index < len(self.tokens):
			return self.tokens[self.index]
		else:
			return None
	def isEOF(self):
		return self.getCurrentToken().content == TokenConstants.EOF and self.index >= 0
	
	def getCurrentToken(self):
		return self.tokens[self.index]
	
	#def scanto(self,synchset):
	#	while not self.getCurrentToken().content in synchset 

class TokenConstants:
	CHAR_SP = "CARACTER_ESPECIAL"
	ID = "IDENTIFICADOR"
	INT = "ENTERO"
	RELATION = "COMPARACION"
	PLUS = "MAS"
	LESS = "MENOS"
	NUM = "NUMERO"
	OP_BOOL = "OP_BOOLEANO"
	ASSIGN = "ASIGNACION"
	SLASH = "SLASH"
	DECREMENT = "DECREMENTO"
	INCREMENT = "INCREMENTO"
	FLOAT = "FLOTANTE"
	BOOLEAN = "BOLEANO"
	IF = "if"
	WHILE = "while"
	DO = "do"
	CIN = "cin"
	COUT = "cout"
	BRACKET_OPEN = "{"
	TIMES = "*"
	DIV = "/"
	ELSE = "else"
	EOF = "$"
