from syntax.Tree import *
from syntax.TokensHelper import *
import json
import os
import ntpath
################### ENDPOINTS
_tipo = ["int","float","boolean"]
_sentencia = ["if","while","do","cin","cout","{"]
_relacion = ["<=", "<", ">" ,">=", "==", "!="]
_suma_op = ["+","-"]
_mult_op = ["*","/"]
EMPTY = "ε";
#############################
#PRIMARY SETS
_p_programa=set(["main"])
_p_lista_declaracion=set(["int","float","boolean",EMPTY])
_p_declaracion=set(["int","float","boolean"])
_p_tipo=set(["int","float","boolean"])
_p_lista_variables=set(["identificador"])
_p_lista_sentencias=set(["if","while","until","cin","cout","{","identificador",EMPTY])
_p_sentencia=set(["if","while","repeat","cin","cout","{","identificador"])
_p_seleccion=set(["if"])
_p_iteracion=set(["while"])
_p_repeticion=set(["repeat"])
_p_sent_cin=set(["cin"])
_p_sent_cout=set(["cout"])
_p_bloque=set(["{"])
_p_asignacion=set(["identificador"])
_p_expresion=set(["(","numero","identificador"])
_p_relacion=set(["<=","<",">",">=","==","!="])
_p_expresion_simple=set(["(","numero","identificador"])
_p_suma_op=set(['-', '+'])
_p_termino=set(["(","numero","identificador"])
_p_mult_op=set(['*', '/'])
_p_factor=set(['(', 'numero', 'identificador'])

#NEXT SETS
_s_programa=set(["$"])
#TODO: Verify is this set needs the EMPTY item
_s_lista_declaracion=set(["$","if","while","repeat","cin","cout","{"])
_s_declaracion=set([";"])
_s_tipo=set(["identificador"])
_s_lista_variables=set([";"])
_s_lista_sentencias=set(["}"])
_s_sentencia=set(["if","while","repeat","cin","cout","{","identificador","}"])
_s_seleccion=set(["if","while","repeat","cin","cout","{","identificador","}"])
_s_iteracion=set(["if","while","repeat","cin","cout","{","identificador","}"])
_s_repeticion=set(["if","while","repeat","cin","cout","{","identificador","}"])
_s_sent_cin=set(["if","while","repeat","cin","cout","{","identificador","}"])
_s_sent_cout=set(["if","while","repeat","cin","cout","{","identificador","}"])
_s_bloque=set(["if","while","repeat","cin","cout","{","identificador","}","until","else"])
_s_asignacion=set(["if","while","repeat","cin","cout","{","identificador","}"])
_s_expresion=set([")",";"])
_s_relacion=set(["(","numero","identificaodr"])
_s_expresion_simple=set([")",";","+","-","<","<=",">",">=","==","!="])
_s_suma_op=set(["(","numero","identificaodr"])
_s_termino=set([")",";","+","-","*","/","<","<=",">",">=","==","!="])
_s_mult_op=set(["(","numero","identificaodr"])
_s_factor=set([")",";","+","-","*","/","<","<=",">",">=","==","!="])

class Syntax:
	#programa → main “{“ lista-declaración lista-sentencias “}”
	def programa(self):
		sync = _s_programa
		firstToken = self.tokensHelper.getToken()
		self.tokensHelper.checkInput(_p_programa,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			self.tokensHelper.match("main")
			self.root = Node(firstToken.content)
			self.tokensHelper.match("{")
			self.root.addChild( self.lista_declaracion(_s_lista_declaracion) )
			self.root.addChild( self.lista_sentencias(_s_lista_sentencias) )
			self.tokensHelper.match("}")
			#print("INFO: Syntax Compilation finished. Tree:")
			#TreeUtils.cliDisplay(root)
			if self.outputType == "json":
				print(json.dumps(self.root.__dict__, indent=4, sort_keys=False))
			elif self.outputType == "tree":
				TreeUtils.cliDisplay(self.root)
			elif self.outputType == "none":
				print("== No output ==")
			else:
				print("Invalid argument: "+self.outputType)
			self.tokensHelper.checkInput(sync,_p_programa)
	#lista-declaración -> { declaración; }
	def lista_declaracion(self,sync):
		self.tokensHelper.checkInput(_p_lista_declaracion,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			decl = None
			while self.tokensHelper.getCurrentToken().content in _tipo:
				if decl == None:
					decl = self.declaracion(_s_declaracion)
				else:
					decl.appendBro( self.declaracion(_s_declaracion) )
				self.tokensHelper.match(";")
			
			if decl != None and len(decl.sons) > 0:
				return decl
			else:
				return None
			self.tokensHelper.checkInput(sync,_p_lista_declaracion)

	#lista-sentencias → { sentencia }
	#sentencia → selección | iteración | repetición | sent-cin |sent-out | bloque | asignación
	def lista_sentencias(self,sync):
		self.tokensHelper.checkInput(_p_lista_sentencias,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			tmp = new = None
			while self.tokensHelper.getCurrentToken().content in _sentencia or self.tokensHelper.getCurrentToken().type == TokenConstants.ID:
				if self.tokensHelper.getCurrentToken().content == TokenConstants.IF:
					new = self.seleccion(_s_seleccion)
				elif self.tokensHelper.getCurrentToken().content == TokenConstants.WHILE:
					new = self.iteracion(_s_iteracion)
				elif self.tokensHelper.getCurrentToken().content == TokenConstants.DO:
					new = self.repeticion(_s_repeticion)
				elif self.tokensHelper.getCurrentToken().content == TokenConstants.CIN:
					new = self.sent_cin(_s_sent_cin)
				elif self.tokensHelper.getCurrentToken().content == TokenConstants.COUT:
					new = self.sent_cout(_s_sent_cout)
				elif self.tokensHelper.getCurrentToken().content == TokenConstants.BRACKET_OPEN:
					new = self.bloque(_s_bloque)
				elif self.tokensHelper.getCurrentToken().type == TokenConstants.ID:
					new = self.asignacion(_s_asignacion)
				
				if tmp == None:
					tmp = new
				else:
					tmp.appendBro( new )
			if tmp != None and len(tmp.sons) > 0:
				return tmp
			else:
				return None
			self.tokensHelper.checkInput(sync,_p_lista_sentencias)
			
	#selección → if ( expresión ) then bloque | if ( expresión ) then bloque else bloque
	def seleccion(self,sync):
		self.tokensHelper.checkInput(_p_seleccion,sync)
		if not self.tokensHelper.getCurrentToken().content in sync.difference(["if"]):
			ifStmt = Node( TokenConstants.IF )
			self.tokensHelper.match( TokenConstants.IF )
			self.tokensHelper.match( "(" )
			ifStmt.addChild ( self.expresion(_s_expresion) )
			self.tokensHelper.match( ")" )
			self.tokensHelper.match( "then" )
			ifStmt.addChild( self.bloque(_s_bloque) )

			if( self.tokensHelper.getCurrentToken().content == TokenConstants.ELSE ):
				self.tokensHelper.match( TokenConstants.ELSE )
				ifStmt.addChild( self.bloque(_s_bloque) )
				
			return ifStmt
			self.tokensHelper.checkInput(sync,_p_seleccion,set(["entero","flotante"]))
	#expresión → expresión-simple { relación expresión-simple }
	def expresion(self,sync):
		self.tokensHelper.checkInput(_p_expresion,sync,set(["entero","flotante"]))
		if not self.tokensHelper.getCurrentToken().content in sync:
			exp = None
			tmp = self.expresion_simple(_s_expresion_simple)
			if( self.tokensHelper.getCurrentToken().content in _relacion ):
				exp = self.relacion(_s_relacion)
				exp.addChild(tmp)
				exp.addChild( self.expresion_simple(_s_expresion_simple) )
			if exp == None:
				exp = tmp
			return exp
			self.tokensHelper.checkInput(sync,_p_expresion)

	def relacion(self,sync):
		self.tokensHelper.checkInput(_p_relacion,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			rel = self.tokensHelper.getCurrentToken().content
			self.tokensHelper.match(TokenConstants.RELATION,True)
			return Node(rel)
			self.tokensHelper.checkInput(sync,_p_relacion)

	#expresión-simple → termino { suma-op termino }
	def expresion_simple(self,sync):
		self.tokensHelper.checkInput(_p_expresion_simple,sync,set(["entero","flotante"]))
		if not self.tokensHelper.getCurrentToken().content in sync.union(set(["entero","flotante"])):
			tmp = self.termino(_s_termino)
			while( self.tokensHelper.getCurrentToken().content[0] in _suma_op):
				new = self.suma_op(_s_suma_op)
				new.addChild(tmp)
				comesFromALess = self.tokensHelper.getCurrentToken().content[0]=="-"
				term = self.termino(_s_termino,comesFromALess)
				#new.addChild( termino() )
				#Here we're validating if the operation symbol is less and
				#the second number of the operation is a negative number
				if new != None and term != None and new.name == "-" and term.name[0] == "-":
					#remove the negative number
					term.name = term.name[1:]
				new.addChild( term )
				tmp = new
			return tmp
			self.tokensHelper.checkInput(sync,_p_expresion_simple)
			

	def suma_op(self,sync):
		self.tokensHelper.checkInput(_p_suma_op,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			rel = self.tokensHelper.getCurrentToken().content[0]
			if(self.tokensHelper.getCurrentToken().type == TokenConstants.PLUS):
				self.tokensHelper.match(TokenConstants.PLUS,True)
			elif (self.tokensHelper.getCurrentToken().type == TokenConstants.LESS):
				self.tokensHelper.match(TokenConstants.LESS,True)
			return Node(rel)
			self.tokensHelper.checkInput(sync,_p_suma_op)
	#termino → factor { mult-op factor }
	def termino(self,sync,comesFromALess=False):

		self.tokensHelper.checkInput(_p_termino,sync,set(["entero","flotante"]))
		if not self.tokensHelper.getCurrentToken().content in sync.union(set(["entero","flotante"])):
			tmp = self.factor(_s_factor)
			#Verify if the parent is a less
			#and check if the number is a negative number
			#if comesFromALess and tmp.name[0] == "-":
			#	tmp.name = tmp.name[1:]
		
			while ( self.tokensHelper.getCurrentToken().content in _mult_op):
				new = self.mult_op(_s_mult_op);
				new.addChild(tmp)
				new.addChild( self.factor(_s_factor) )
				tmp = new
			return tmp
			self.tokensHelper.checkInput(sync,_p_termino,_p_termino)

	def mult_op(self,sync):
		self.tokensHelper.checkInput(_p_mult_op,sync)
		if self.tokensHelper.getCurrentToken().content in sync.union(_p_mult_op):
			rel = self.tokensHelper.getCurrentToken().content
			if(self.tokensHelper.getCurrentToken().content == TokenConstants.TIMES):
				self.tokensHelper.match(TokenConstants.TIMES)
			elif (self.tokensHelper.getCurrentToken().content == TokenConstants.DIV):
				self.tokensHelper.match(TokenConstants.DIV)
			return Node(rel)
			self.tokensHelper.checkInput(sync,_p_mult_op)

	#factor → ( expresión ) | numero | identificador
	def factor(self,sync):
		sync = sync.union(set(["entero","flotante"])).union(_p_factor)
		self.tokensHelper.checkInput(_p_factor,sync,set(["entero","flotante"]))
		if self.tokensHelper.getCurrentToken().content in sync or self.tokensHelper.getCurrentToken().type.lower() in sync:
			new = None
			if self.tokensHelper.getCurrentToken().content == "(":
				self.tokensHelper.match("(")
				new = self.expresion(_s_expresion)
				self.tokensHelper.match(")")
			elif self.tokensHelper.getCurrentToken().type == TokenConstants.INT:
				new = Node(self.tokensHelper.getCurrentToken().content)
				self.tokensHelper.match(TokenConstants.INT,True)
			
			elif self.tokensHelper.getCurrentToken().type == TokenConstants.FLOAT:
				new = Node(self.tokensHelper.getCurrentToken().content)
				self.tokensHelper.match(TokenConstants.FLOAT,True)
			else:
				new = Node(self.tokensHelper.getCurrentToken().content)
				self.tokensHelper.match(TokenConstants.ID,True)

			return new
			self.tokensHelper.checkInput(_p_factor,sync)

	#iteración → while ( expresión ) bloque
	def iteracion(self,sync):
		self.tokensHelper.checkInput(_p_iteracion,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			new = Node( TokenConstants.WHILE )
			self.tokensHelper.match( TokenConstants.WHILE )
			self.tokensHelper.match("(")
			new.addChild( self.expresion(_s_expresion) )
			self.tokensHelper.match(")")
			new.addChild( self.bloque(_s_bloque) )
			return new
			self.tokensHelper.checkInput(_p_iteracion,sync)
	#repetición → do bloque until ( expresión ) ;
	def repeticion(self,sync):
		self.tokensHelper.checkInput(_p_repeticion,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			new = Node( TokenConstants.DO )
			self.tokensHelper.match( TokenConstants.DO )
			new.addChild( self.bloque(_s_bloque) )
			self.tokensHelper.match("until")
			self.tokensHelper.match("(")
			new.addChild( self.expresion(_s_expresion) )
			self.tokensHelper.match(")")
			self.tokensHelper.match(";")
			return new
			self.tokensHelper.checkInput(_p_repeticion,sync)

	#sent-cin → cin identificador ;
	def sent_cin(self,sync):
		self.tokensHelper.checkInput(_p_sent_cin,sync)
		if not self.tokensHelper.getCurrentToken().content in sync.difference(["cin"]):
			new = Node("cin")
			self.tokensHelper.match("cin")
			new.addChild( Node(self.tokensHelper.getCurrentToken().content ) )
			self.tokensHelper.match(TokenConstants.ID,True)
			self.tokensHelper.match(";")	
			return new
			self.tokensHelper.checkInput(_p_sent_cin,sync)
	#sent-cout → cout expresión ;
	def sent_cout(self,sync):
		self.tokensHelper.checkInput(_p_sent_cout,sync)
		if not self.tokensHelper.getCurrentToken().content in sync.difference(["cout"]):	
			new = Node("cout")
			self.tokensHelper.match("cout")
			exp = self.expresion(_s_expresion)
			new.addChild( exp ) 
			self.tokensHelper.match(";")	
			return new
			self.tokensHelper.checkInput(_p_sent_cout,sync)


	def bloque(self,sync):
		self.tokensHelper.checkInput(_p_bloque,sync)
		if not self.tokensHelper.getCurrentToken().content in sync.difference(["{"]):	
			self.tokensHelper.match("{")
			new = self.lista_sentencias(_s_lista_sentencias)
			self.tokensHelper.match("}")
			return new
			self.tokensHelper.checkInput(_p_bloque,sync)

	#asignación → identificador := expresión ;
	def asignacion(self,sync):
		self.tokensHelper.checkInput(_p_asignacion,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:	
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
				asignExp = self.expresion(_s_expresion)
				new.addChild( asignExp )
			self.tokensHelper.match(";")
			return new
			self.tokensHelper.checkInput(_p_asignacion,sync)

	#declaración → tipo lista-variables
	def declaracion(self,sync):
		self.tokensHelper.checkInput(_p_declaracion,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:	
			tmp = Node(self.tokensHelper.getCurrentToken().content)
			self.tokensHelper.match(TokenConstants.ID,True)
			self.lista_variables(tmp,_s_lista_variables)
			self.tokensHelper.checkInput(_p_declaracion,sync,set([";"]))
			return tmp
			
			
	#lista-variables → { identificador, } identificador
	def lista_variables(self,parent,sync):
		self.tokensHelper.checkInput(_p_lista_variables,sync)
		if not self.tokensHelper.getCurrentToken().content in sync:
			parent.addChild(Node(self.tokensHelper.getCurrentToken().content))
			self.tokensHelper.match(TokenConstants.ID,True)
			while self.tokensHelper.getCurrentToken().content == ",":
				self.tokensHelper.match(",")
				parent.addChild(Node(self.tokensHelper.getCurrentToken().content))
				self.tokensHelper.match(TokenConstants.ID,True)
			self.tokensHelper.checkInput(_p_lista_variables,sync,set([";"]))

	def __init__(self,pathOfSouce,outputType="json"):
		canonicalFileName = ntpath.basename(pathOfSouce)
		withoutExtention = canonicalFileName[0:canonicalFileName.find(".")]
		lexDirectory = "target_"+withoutExtention+"\\lex\\"
		basepath = ntpath.abspath(pathOfSouce)[0:len(ntpath.abspath(pathOfSouce))-len(canonicalFileName)]
		arg = basepath+lexDirectory+"out.lex"	
		if not os.path.exists(arg):
			basepath = basepath.replace("\\","/")
			arg = basepath+"out.lex"
			if not os.path.exists(arg):
				arg = basepath+lexDirectory+"out.lex"	
				arg = arg.replace("\\","/")
				if not os.path.exists(arg):
					print("Error, analisis lexico aun no ejecutado",file=sys.stderr)
					exit(1)
		self.tokensHelper = TokensHelper(arg)
		self.outputType = outputType
	def go(self):
		self.programa()
		return self.root