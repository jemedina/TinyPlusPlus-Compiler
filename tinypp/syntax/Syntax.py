from syntax.Tree import *
from syntax.TokensHelper import *
import json

################### ENDPOINTS
_tipo = ["int","float","boolean"]
_sentencia = ["if","while","do","cin","cout","{"]
_relacion = ["<=", "<", ">" ,">=", "==", "!="]
_suma_op = ["+","-"]
_mult_op = ["*","/"]
#############################



class Syntax:
	#programa → main “{“ lista-declaración lista-sentencias “}”
	def programa(self):
		#self.tokensHelper.cliDisplayTokens()
		firstToken = self.tokensHelper.getToken()	
		self.tokensHelper.match("main")
		self.root = Node(firstToken.content)
		self.tokensHelper.match("{")
		self.root.addChild( self.lista_declaracion() )
		self.root.addChild( self.lista_sentencias() )
		self.tokensHelper.match("}")
		print("INFO: Syntax Compilation finished. Tree:")
		#TreeUtils.cliDisplay(root)
		if self.outputType == "json":
			print(json.dumps(self.root.__dict__, indent=4, sort_keys=False))
		elif self.outputType == "tree":
			TreeUtils.cliDisplay(self.root)
		elif self.outputType == "none":
			print("== No output ==")
		else:
			print("Invalid argument: "+self.outputType)
	#lista-declaración -> { declaración; }
	def lista_declaracion(self):
		decl = None
		while self.tokensHelper.getCurrentToken().content in _tipo:
			if decl == None:
				decl = self.declaracion()
			else:
				decl.appendBro( self.declaracion() )
			self.tokensHelper.match(";")
		
		if decl != None and len(decl.sons) > 0:
			return decl
		else:
			return None

	#lista-sentencias → { sentencia }
	#sentencia → selección | iteración | repetición | sent-cin |sent-out | bloque | asignación
	def lista_sentencias(self):
		tmp = new = None
		while self.tokensHelper.getCurrentToken().content in _sentencia or self.tokensHelper.getCurrentToken().type == TokenConstants.ID:
			if self.tokensHelper.getCurrentToken().content == TokenConstants.IF:
				new = self.seleccion()
			elif self.tokensHelper.getCurrentToken().content == TokenConstants.WHILE:
				new = self.iteracion()
			elif self.tokensHelper.getCurrentToken().content == TokenConstants.DO:
				new = self.repeticion()
			elif self.tokensHelper.getCurrentToken().content == TokenConstants.CIN:
				new = self.sent_cin()
			elif self.tokensHelper.getCurrentToken().content == TokenConstants.COUT:
				new = self.sent_cout()
			elif self.tokensHelper.getCurrentToken().content == TokenConstants.BRACKET_OPEN:
				new = self.bloque()
			elif self.tokensHelper.getCurrentToken().type == TokenConstants.ID:
				new = self.asignacion()
			
			if tmp == None:
				tmp = new
			else:
				tmp.appendBro( new )
		if tmp != None and len(tmp.sons) > 0:
			return tmp
		else:
			return None
			
	#selección → if ( expresión ) then bloque | if ( expresión ) then bloque else bloque
	def seleccion(self):
		ifStmt = Node( TokenConstants.IF )
		self.tokensHelper.match( TokenConstants.IF )
		self.tokensHelper.match( "(" )
		ifStmt.addChild ( self.expresion() )
		self.tokensHelper.match( ")" )
		self.tokensHelper.match( "then" )
		ifStmt.addChild( self.bloque() )

		if( self.tokensHelper.getCurrentToken().content == TokenConstants.ELSE ):
			self.tokensHelper.match( TokenConstants.ELSE )
			ifStmt.addChild( self.bloque() )
			
		return ifStmt
		
	#expresión → expresión-simple { relación expresión-simple }
	def expresion(self):
		exp = None
		tmp = self.expresion_simple()
		if( self.tokensHelper.getCurrentToken().content in _relacion ):
			exp = self.relacion()
			exp.addChild(tmp)
			exp.addChild( self.expresion_simple() )
		if exp == None:
			exp = tmp
		return exp

	def relacion(self):
		rel = self.tokensHelper.getCurrentToken().content
		self.tokensHelper.match(TokenConstants.RELATION,True)
		return Node(rel)

	#expresión-simple → termino { suma-op termino }
	def expresion_simple(self):
		tmp = self.termino()
		while( self.tokensHelper.getCurrentToken().content[0] in _suma_op):
			new = self.suma_op()
			new.addChild(tmp)
			comesFromALess = self.tokensHelper.getCurrentToken().content[0]=="-"
			term = self.termino(comesFromALess)
			#new.addChild( termino() )
			#Here we're validating if the operation symbol is less and
			#the second number of the operation is a negative number
			if new.name == "-" and term.name[0] == "-":
				#remove the negative number
				term.name = term.name[1:]
			new.addChild( term )
			tmp = new
		return tmp

	def suma_op(self):
		rel = self.tokensHelper.getCurrentToken().content[0]
		if(self.tokensHelper.getCurrentToken().type == TokenConstants.PLUS):
			self.tokensHelper.match(TokenConstants.PLUS,True)
		elif (self.tokensHelper.getCurrentToken().type == TokenConstants.LESS):
			self.tokensHelper.match(TokenConstants.LESS,True)
		return Node(rel)

	#termino → factor { mult-op factor }
	def termino(self,comesFromALess=False):
		tmp = self.factor()
		#Verify if the parent is a less
		#and check if the number is a negative number
		if comesFromALess and tmp.name[0] == "-":
			tmp.name = tmp.name[1:]

		while ( self.tokensHelper.getCurrentToken().content in _mult_op):
			new = self.mult_op();
			new.addChild(tmp)
			new.addChild( self.factor() )
			tmp = new
		return tmp

	def mult_op(self):
		rel = self.tokensHelper.getCurrentToken().content
		if(self.tokensHelper.getCurrentToken().content == TokenConstants.TIMES):
			self.tokensHelper.match(TokenConstants.TIMES)
		elif (self.tokensHelper.getCurrentToken().content == TokenConstants.DIV):
			self.tokensHelper.match(TokenConstants.DIV)
		return Node(rel)

	#factor → ( expresión ) | numero | identificador
	def factor(self):
		new = None
		if self.tokensHelper.getCurrentToken().content == "(":
			self.tokensHelper.match("(")
			new = self.expresion()
			self.tokensHelper.match(")")
		elif self.tokensHelper.getCurrentToken().type == TokenConstants.INT:
			if self.tokensHelper.getCurrentToken().content[0] == "+":
				valueWithoutPlus = self.tokensHelper.getCurrentToken().content[1:]
			else:
				valueWithoutPlus = self.tokensHelper.getCurrentToken().content
			new = Node(valueWithoutPlus)
			self.tokensHelper.match(TokenConstants.INT,True)
		
		elif self.tokensHelper.getCurrentToken().type == TokenConstants.FLOAT:
			if self.tokensHelper.getCurrentToken().content[0] == "+":
				valueWithoutPlus = self.tokensHelper.getCurrentToken().content[1:]
			else:
				valueWithoutPlus = self.tokensHelper.getCurrentToken().content
			new = Node(valueWithoutPlus)
			self.tokensHelper.match(TokenConstants.FLOAT,True)

		elif self.tokensHelper.getCurrentToken().type == TokenConstants.ID:
			new = Node(self.tokensHelper.getCurrentToken().content)
			self.tokensHelper.match(TokenConstants.ID,True)

		return new

	#iteración → while ( expresión ) bloque
	def iteracion(self):
		new = Node( TokenConstants.WHILE )
		self.tokensHelper.match( TokenConstants.WHILE )
		self.tokensHelper.match("(")
		new.addChild( self.expresion() )
		self.tokensHelper.match(")")
		new.addChild( self.bloque() )
		return new

	#repetición → do bloque until ( expresión ) ;
	def repeticion(self):
		new = Node( TokenConstants.DO )
		self.tokensHelper.match( TokenConstants.DO )
		new.addChild( self.bloque() )
		self.tokensHelper.match("until")
		self.tokensHelper.match("(")
		new.addChild( self.expresion() )
		self.tokensHelper.match(")")
		self.tokensHelper.match(";")
		return new


	#sent-cin → cin identificador ;
	def sent_cin(self):
		new = Node("cin")
		self.tokensHelper.match("cin")
		new.addChild( Node(self.tokensHelper.getCurrentToken().content ) )
		self.tokensHelper.match(TokenConstants.ID,True)
		self.tokensHelper.match(";")	
		return new

	#sent-cout → cout expresión ;
	def sent_cout(self):	
		new = Node("cout")
		self.tokensHelper.match("cout")
		new.addChild( Node(self.tokensHelper.getCurrentToken().content ) )
		self.tokensHelper.match(TokenConstants.ID,True)
		self.tokensHelper.match(";")	
		return new

	def bloque(self):
		self.tokensHelper.match("{")
		new = self.lista_sentencias()
		self.tokensHelper.match("}")
		return new

	#asignación → identificador := expresión ;
	def asignacion(self):
		new = Node(":=")
		ide = Node(self.tokensHelper.getCurrentToken().content)
		new.addChild(ide)
		self.tokensHelper.match(TokenConstants.ID,True)
		if self.tokensHelper.getCurrentToken().type == TokenConstants.INCREMENT:
			plusNode = Node("+")
			plusNode.addChild( ide )
			self.tokensHelper.match(TokenConstants.INCREMENT,True)
			plusNode.addChild(Node("1"))
			new.addChild(plusNode)	
		elif self.tokensHelper.getCurrentToken().type == TokenConstants.DECREMENT:
			lessNode = Node("-")
			lessNode.addChild( ide )
			self.tokensHelper.match(TokenConstants.DECREMENT,True)
			lessNode.addChild(Node("1"))
			new.addChild(lessNode)
		else:
			self.tokensHelper.match(":=")
			asignExp = self.expresion()
			new.addChild( asignExp )
		self.tokensHelper.match(";")
		return new

	#declaración → tipo lista-variables
	def declaracion(self):
		tmp = Node(self.tokensHelper.getCurrentToken().content)
		self.tokensHelper.match(TokenConstants.ID,True)
		self.lista_variables(tmp)
		return tmp

	#lista-variables → { identificador, } identificador
	def lista_variables(self,parent):
		parent.addChild(Node(self.tokensHelper.getCurrentToken().content))
		self.tokensHelper.match(TokenConstants.ID,True)

		while self.tokensHelper.getCurrentToken().content == ",":
			self.tokensHelper.match(",")
			parent.addChild(Node(self.tokensHelper.getCurrentToken().content))
			self.tokensHelper.match(TokenConstants.ID,True)


	def __init__(self,arg,outputType="json"):
		self.tokensHelper = TokensHelper(arg)
		self.outputType = outputType
	def go(self):
		self.programa()
