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
		self.errors = []
		try:
			self.tokensFile = open(tokensFilePath,"+r")
			self.tokens = []
			self.index = -1
			self.loadTokens()
			self.lastToken = None
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
				self.syntaxError("unexpected token -> <"+self.getCurrentToken().content+"> was expected <"+testChar+">")
		else:
			#print(self.index,self.getCurrentToken(),testChar)
			isAnEmptyBlock = (self.lastToken != None and self.lastToken.content == "{" and testChar == "}")
			if testChar == self.getCurrentToken().content or isAnEmptyBlock:
				if isAnEmptyBlock:
					self.index+=1
					self.getToken()
				else:
					self.getToken()
			else:
				self.syntaxError("unexpected token -> <"+self.getCurrentToken().content+"> was expected <"+testChar+">")

	def cliDisplayTokens(self):
		for t in self.tokens:
			print(t)
	def error(self):
		print("Syntax error in row = "+self.getCurrentToken().row+", col = "+self.getCurrentToken().col+": "+self.getCurrentToken().content,file=sys.stderr)
	
	def syntaxError(self,message):
		self.errors.append("Syntax error at line "+self.getCurrentToken().row+", col = "+self.getCurrentToken().col+": "+message)
		#print("Syntax error at line "+self.getCurrentToken().row+", col = "+self.getCurrentToken().col+": "+message)
	def printErrors(self,errorfile):
		for i in self.errors:
			print(i,file=errorfile)
			print(i,file=sys.stderr)
	
	def manageErrors(self):
		known_links = set()
		newlist = []
		for d in self.errors:
			link = d
			if d in known_links: continue
			newlist.append(d)
			known_links.add(link)
		self.errors[:] = newlist

	def getToken(self):
		self.lastToken = self.tokens[self.index]
		self.index += 1
		if self.index < len(self.tokens):
			if self.lastToken.content == "{" and self.tokens[self.index].content == "}":
				self.tokens.insert(self.index,Token("empty","ε","unknown","unknown"))
			if self.lastToken.type != TokenConstants.ID and self.getCurrentToken().content in ["++","--"]:
				temporalToken = self.getCurrentToken()
				self.tokens.pop(self.index)
				if temporalToken.content == "++":
					self.tokens.insert(self.index,Token("MAS","+",temporalToken.row,temporalToken.col))
					temporalToken.col=str(int(temporalToken.col)+1)
					self.tokens.insert(self.index,Token("MAS","+",temporalToken.row,temporalToken.col))
				elif temporalToken.content == "--":
					self.tokens.insert(self.index,Token("MENOS","-",temporalToken.row,temporalToken.col))
					temporalToken.col=str(int(temporalToken.col)+1)
					self.tokens.insert(self.index,Token("MENOS","-",temporalToken.row,temporalToken.col))
		
		if self.index < len(self.tokens):
			return self.tokens[self.index]
		else:
			return None
	def isEOF(self):
		return self.getCurrentToken().content == TokenConstants.EOF and self.index >= 0
	
	def getCurrentToken(self):
		return self.tokens[self.index]
	
	def getNextToken(self):
		if self.index+1 < len(self.tokens):
			return self.tokens[self.index+1]
		else:
			return None
	
	def scanto(self,synchset):
		while not (self.getCurrentToken().content.lower() in synchset.union(["$"]) \
		or self.getCurrentToken().type.lower() in synchset.union(["$"])):
			self.getToken()
	def scantoNext(self,synchset,nextSet):
		while not (self.getCurrentToken().content.lower() in synchset.union(["$"]) \
		or self.getCurrentToken().type.lower() in synchset.union(["$"]) \
		or self.getNextToken().content in nextSet):
			self.getToken()
	def scantoStillNotExpected(self,synchset,stillNotExpectedSet):
		while not (self.getCurrentToken().content.lower() in synchset.union(["$"]) \
		or self.getCurrentToken().type.lower() in synchset.union(["$"]) \
		or self.getCurrentToken().type.lower() in stillNotExpectedSet):
			self.getToken()
	
	def checkInput(self,first,follow,complementaryset=set(),nextSet=None,stillNotExpectedSet=None,displayErrors=True,traceErrors=False):
		hasError = False
		if nextSet == None and stillNotExpectedSet == None:
			if not (self.getCurrentToken().content.lower() in first.union(complementaryset) or \
			self.getCurrentToken().type.lower() in first.union(complementaryset)):
				hasError = True
				if displayErrors:
					self.syntaxError("unexpected token -> <"+self.getCurrentToken().content+">")
				self.scanto(first.union(follow).union(complementaryset))
		elif nextSet != None:
			if not (self.getCurrentToken().content.lower() in first.union(complementaryset) or \
			self.getCurrentToken().type.lower() in first.union(complementaryset) or \
			self.getNextToken().content in nextSet):
				hasError = True
				if displayErrors:
					self.syntaxError("unexpected token -> <"+self.getCurrentToken().content+">")
				if not traceErrors:
					self.scantoNext(first.union(follow).union(complementaryset),nextSet)
				else:
					self.scantoNext(first.union(follow).union(complementaryset).union(set([self.getNextToken().content])),nextSet)
		elif stillNotExpectedSet != None:
			if not (self.getCurrentToken().content.lower() in first.union(complementaryset) or \
			self.getCurrentToken().type.lower() in first.union(complementaryset) or \
			not self.getCurrentToken().type.lower() in stillNotExpectedSet):
				hasError = True
				if displayErrors:
					self.syntaxError("unexpected token -> <"+self.getCurrentToken().content+">")
				self.scantoStillNotExpected(first.union(follow).union(complementaryset),stillNotExpectedSet)
		return hasError
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
	BRACKET_CLOSE = "}"
	TIMES = "*"
	DIV = "/"
	ELSE = "else"
	EOF = "$"
	REPEAT = "repeat"
	DOT_COMMA = ";"
	BREAK = "break"
