from os import sys
class Token:
	def __init__(self,type,content):
		self.type = type
		self.content = content

	def __str__(self):
		return "{"+self.type+":"+self.content+"}"

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
			if tokenText.find(":") > 0:
				identifier = tokenText[0:tokenText.find(":")].strip()
				content = tokenText[tokenText.find(":")+1:len(tokenText)-1].strip()
				self.tokens.append(Token(identifier,content))

	def match(self,testChar,byType=False):
		if byType == True:
			if testChar == self.getCurrentToken().type:
				return self.getToken()
			else:
				self.error()
				return None
		else:
			#print(self.index,self.getCurrentToken(),testChar)
			if testChar == self.getCurrentToken().content:
				return self.getToken()
			else:
				self.error()
				return None
	def cliDisplayTokens(self):
		for t in self.tokens:
			print(t)
	def error(self):
		print("Syntax error near: "+self.getCurrentToken().content)
		
	def getToken(self):
		self.index += 1
		if self.index < len(self.tokens):
			return self.tokens[self.index]
		else:
			return None

	def getCurrentToken(self):
		return self.tokens[self.index]
		
class TokenConstants:
	CHAR_SP = "CARACTER_ESPECIAL"
	ID = "IDENTIFICADOR"
	INT = "ENTERO"
	COMP = "COMPARACION"
	PLUS = "MAS"
	LESS = "MENOS"
	NUM = "NUMERO"
	OP_BOOL = "OP_BOOLEANO"
	ASSIGN = "ASIGNACION"
	SLASH = "SLASH"
	DECREMENT = "DECREMENTO"
	INCREMENT = "INCREMENTO"
	FLOAT = "DECIMAL"
	BOOLEAN = "BOLEANO"
	IF = "if"
	WHILE = "while"
	DO = "do"
	CIN = "cin"
	COUT = "cout"
	BRACKET_OPEN = "{"