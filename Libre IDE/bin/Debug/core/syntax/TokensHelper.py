from os import sys
class Token:
	def __init__(self,type,content):
		self.type = type
		self.content = content

	def __str__(self):
		return "{"+self.identifier+":"+self.content+"}"

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
				identifier = tokenText[0:tokenText.find(":")]
				content = tokenText[tokenText.find(":")+1:len(tokenText)-1]
				self.tokens.append(Token(identifier,content))

	def match(self,tokenType):
		if tokenType == self.getCurrentToken().type:
			return getToken()
		else:
			return None
	def getToken(self):
		self.index += 1
		return self.tokens[self.index]

	def getCurrentToken(self):
		return self.tokens[self.index]
