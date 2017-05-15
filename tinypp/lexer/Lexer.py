from lexer.LexerFileHandler import LexerFileHandler
from lexer.StateManager import StateManager
from lexer.Token import Token
import sys
import os
import ntpath
class Lexer:

	boolean_operators_pattern = "<|>|=|!"
	operators_pattern = "*|%|{|}|(|)|,|;"
	tokens = []

	def __init__(self,pathOfSouce):
		canonicalFileName = ntpath.basename(pathOfSouce)
		withoutExtention = canonicalFileName[0:canonicalFileName.find(".")]
		lexDirectory = "target_"+withoutExtention+"\\lex\\"
		self.lexFileHandler = LexerFileHandler(pathOfSouce)
		self.stateManager = StateManager()
		self.stateManager.setState("INICIO")
		basepath = ntpath.abspath(pathOfSouce)[0:len(ntpath.abspath(pathOfSouce))-len(canonicalFileName)]
		try:
			os.makedirs(basepath+lexDirectory)
		except OSError:
			pass
		self.errFile = open(basepath+lexDirectory+"err.lex","+w")
		self.outFile = open(basepath+lexDirectory+"out.lex","+w")
	def matchOrPattern(self,charac,pattern):
		patternArray = pattern.split("|")
		return charac in patternArray

	def eval(self):
		while self.lexFileHandler.next() != None:
			lexema = []
			tipo = None
			row = 0
			col = 0
			#INICIO STATE
			if self.stateManager.getState() == self.stateManager.getStateByName("INICIO"):
				row = str(self.lexFileHandler.row+1)
				col = str(self.lexFileHandler.col+1)	
				if self.lexFileHandler.getCurrentValue() == '-':
					self.stateManager.setState("MENOS")
				elif self.lexFileHandler.getCurrentValue() == '+':
					self.stateManager.setState("MAS")
				elif not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue().isdigit():
					self.stateManager.setState("NUMERO")
				elif (not self.lexFileHandler.isEOF()) and ( self.lexFileHandler.getCurrentValue() == "_" or self.lexFileHandler.getCurrentValue().isalpha()):
					self.stateManager.setState("IDENTIFICADOR")
				elif not self.lexFileHandler.isEOF() and self.matchOrPattern(self.lexFileHandler.getCurrentValue(),self.boolean_operators_pattern):
					self.stateManager.setState("OP_BOOLEANO")
				elif self.lexFileHandler.getCurrentValue() == ':':
					self.stateManager.setState("ASIGNACION")
				elif self.lexFileHandler.getCurrentValue() == '/':
					self.stateManager.setState("SLASH")
				elif not self.lexFileHandler.isEOF() and self.matchOrPattern(self.lexFileHandler.getCurrentValue(),self.operators_pattern):
					lexema.append(self.lexFileHandler.getCurrentValue())
					tipo = "CARACTER_ESPECIAL"
					self.stateManager.setState("HECHO")
				elif self.lexFileHandler.getCurrentValue() == ' ' or self.lexFileHandler.getCurrentValue() == '\t' or self.lexFileHandler.getCurrentValue() == '\n' or self.lexFileHandler.isEOF():
					self.stateManager.setState("HECHO")
					tipo = "IGNORE"
				if self.stateManager.getState() == self.stateManager.getStateByName("INICIO"):
					self.stateManager.setState("ERROR")

				#MAS State
				if self.stateManager.getState() == self.stateManager.getStateByName("MAS"):
					lexema.append(self.lexFileHandler.getCurrentValue())
					self.lexFileHandler.next()
					if self.lexFileHandler.getCurrentValue() == '+':
						lexema.append(self.lexFileHandler.getCurrentValue())
						tipo = "INCREMENTO"
						self.stateManager.setState("HECHO")
					elif not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue().isdigit():
						self.stateManager.setState("NUMERO")
					else:
						self.lexFileHandler.previous()
						tipo = "MAS"
						self.stateManager.setState("HECHO")

				#MENOS State
				if self.stateManager.getState() == self.stateManager.getStateByName("MENOS"):
					lexema.append(self.lexFileHandler.getCurrentValue())
					self.lexFileHandler.next()
					if self.lexFileHandler.getCurrentValue() == '-':
						lexema.append(self.lexFileHandler.getCurrentValue())
						tipo = "DECREMENTO"
						self.stateManager.setState("HECHO")
					elif not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue().isdigit():
						self.stateManager.setState("NUMERO")
					else:
						self.lexFileHandler.previous()
						tipo = "MENOS"
						self.stateManager.setState("HECHO")

				#NUMERO State
				if self.stateManager.getState() == self.stateManager.getStateByName("NUMERO"):
					lexema.append(self.lexFileHandler.getCurrentValue())
					self.lexFileHandler.next()
					tipo = "ENTERO"
					self.stateManager.setState("HECHO")
					while not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue().isdigit():
						lexema.append(self.lexFileHandler.getCurrentValue())
						self.lexFileHandler.next()
					if not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue() == '.':
						self.stateManager.setState("PUNTO")
					else:
						self.lexFileHandler.previous()


				#PUNTO STATE
				if self.stateManager.getState() == self.stateManager.getStateByName("PUNTO"):
					lexema.append(".")
					self.lexFileHandler.next()
					if not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue().isdigit():
						self.stateManager.setState("DECIMAL")
					else:
						self.lexFileHandler.previous()
						self.stateManager.setState("ERROR")
						

				#DECIMAL STATE
				if self.stateManager.getState() == self.stateManager.getStateByName("DECIMAL"):
					while not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue().isdigit():
						tipo = "FLOTANTE"
						lexema.append(self.lexFileHandler.getCurrentValue())
						self.lexFileHandler.next()
						self.stateManager.setState("HECHO")
					self.lexFileHandler.previous()

				#IDENTIFICAODR State
				if self.stateManager.getState() == self.stateManager.getStateByName("IDENTIFICADOR"):
					lexema.append(self.lexFileHandler.getCurrentValue())
					self.lexFileHandler.next()
					while (not self.lexFileHandler.isEOF()) and (self.lexFileHandler.getCurrentValue().isalnum() or self.lexFileHandler.getCurrentValue() == '_'):
						lexema.append(self.lexFileHandler.getCurrentValue())
						self.lexFileHandler.next()
					self.lexFileHandler.previous()
					self.stateManager.setState("HECHO")
					tipo="IDENTIFICADOR"

				#OP_BOOLEANO State
				if self.stateManager.getState() == self.stateManager.getStateByName("OP_BOOLEANO"):
					lexema.append(self.lexFileHandler.getCurrentValue())
					if self.lexFileHandler.getCurrentValue() == '=' or self.lexFileHandler.getCurrentValue() == '!':
						self.lexFileHandler.next()
						if self.lexFileHandler.getCurrentValue() == '=':
							lexema.append(self.lexFileHandler.getCurrentValue())
							self.stateManager.setState("HECHO")
							tipo="COMPARACION"
						else:
							self.lexFileHandler.previous()
							self.stateManager.setState("ERROR")
					else:
						self.stateManager.setState("HECHO")
						tipo="COMPARACION"
						if self.lexFileHandler.next() == '=':
							lexema.append(self.lexFileHandler.getCurrentValue())
						else:
							self.lexFileHandler.previous()
					 	
				#ASIGNACION State
				if self.stateManager.getState() == self.stateManager.getStateByName("ASIGNACION"):
					lexema.append(self.lexFileHandler.getCurrentValue())
					self.lexFileHandler.next()
					if self.lexFileHandler.getCurrentValue() == '=':
						lexema.append(self.lexFileHandler.getCurrentValue())
						self.stateManager.setState("HECHO")
						tipo="ASIGNACION" 
					else:
						self.lexFileHandler.previous()
						self.stateManager.setState("ERROR")

				#SLASH State
				if self.stateManager.getState() == self.stateManager.getStateByName("SLASH"):
					lexema.append(self.lexFileHandler.getCurrentValue())
					
					tipo="CARACTER_ESPECIAL"
					self.stateManager.setState("HECHO")
					self.lexFileHandler.next()

					if self.lexFileHandler.getCurrentValue() == '/':
						self.lexFileHandler.next()
						while not self.lexFileHandler.isEOF() and not self.lexFileHandler.getCurrentValue() == '\n':
							self.lexFileHandler.next()
						self.stateManager.setState("INICIO")
					elif self.lexFileHandler.getCurrentValue() == '*':
						self.lexFileHandler.next()
						hecho = False
						while not self.lexFileHandler.isEOF() and not hecho:
							while not self.lexFileHandler.isEOF() and self.lexFileHandler.getCurrentValue() != '*':
								self.lexFileHandler.next()
							self.lexFileHandler.next()
							if self.lexFileHandler.getCurrentValue() == '/':
								hecho = True
								self.stateManager.setState("INICIO")

						if self.stateManager.getState() != self.stateManager.getStateByName("INICIO"):
							self.stateManager.setState("ERROR")
					if self.stateManager.getState() != self.stateManager.getStateByName("INICIO") and not self.lexFileHandler.isEOF():
						self.lexFileHandler.previous()
						#print("ENTRO row ",self.lexFileHandler.row)
				#ERROR State
				if self.stateManager.getState() == self.stateManager.getStateByName("ERROR"):
					if len(lexema)>1:
						strd = "".join(lexema)
					else:
						strd = self.lexFileHandler.getCurrentValue()
					errLine = "ERROR UNEXPECTED CHARACTER IN row="+str(self.lexFileHandler.row+1)+", col="+str(self.lexFileHandler.col+1)+": '"+str(strd)+"'"
					print(errLine,file=sys.stderr)
					self.errFile.write(errLine+'\n')
					self.stateManager.setState("INICIO")

				#HECHO State
				if self.stateManager.getState() == self.stateManager.getStateByName("HECHO"):
					if tipo != "IGNORE":
						newToken = Token(tipo,"".join(lexema),row,col)
						self.tokens.append(newToken)
						self.outFile.write(str(newToken)+'\n')
						print(newToken)
					self.stateManager.setState("INICIO")

	def close(self):
		self.lexFileHandler.close()
		self.errFile.flush();
		self.errFile.close();
		self.outFile.flush();
		self.outFile.close();
