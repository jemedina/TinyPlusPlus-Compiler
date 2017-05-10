from Tree import *
from TokensHelper import *
################### ENDPOINTS
_tipo = ["int","float","boolean"]
_sentencia = ["if","while","do","cin","cout","{"]
_relacion = ["<=", "<", ">" ,">=", "==", "!="]
_suma_op = ["+","-"]
_mult_op = ["*","/"]
#############################




#programa → main “{“ lista-declaración lista-sentencias “}”
def programa():
	#tokensHelper.cliDisplayTokens()
	firstToken = tokensHelper.getToken()	
	tokensHelper.match("main")
	root = Node(firstToken.content)
	tokensHelper.match("{")
	root.addChild( lista_declaracion() )
	root.addChild( lista_sentencias() )
	tokensHelper.match("}")
	print("INFO: Syntax Compilation finished. Tree:")
	TreeUtils.cliDisplay(root)

#lista-declaración -> { declaración; }
def lista_declaracion():
	decl = None
	while tokensHelper.getCurrentToken().content in _tipo:
		if decl == None:
			decl = declaracion()
		else:
			decl.appendBro( declaracion() )
		tokensHelper.match(";")
	
	if decl != None and len(decl.sons) > 0:
		return decl
	else:
		return None
#lista-sentencias → sentencia lista-sentencias | sentencia | vació
#lista-sentencias → { sentencia }
#sentencia → selección | iteración | repetición | sent-cin |sent-out | bloque | asignación
def lista_sentencias():
	tmp = new = None
	while tokensHelper.getCurrentToken().content in _sentencia or tokensHelper.getCurrentToken().type == TokenConstants.ID:
		if tokensHelper.getCurrentToken().content == TokenConstants.IF:
			new = seleccion()
		elif tokensHelper.getCurrentToken().content == TokenConstants.WHILE:
			new = iteracion()
		elif tokensHelper.getCurrentToken().content == TokenConstants.DO:
			new = repeticion()
		elif tokensHelper.getCurrentToken().content == TokenConstants.CIN:
			new = sent_cin()
		elif tokensHelper.getCurrentToken().content == TokenConstants.COUT:
			new = sent_cout()
		elif tokensHelper.getCurrentToken().content == TokenConstants.BRACKET_OPEN:
			new = bloque()
		elif tokensHelper.getCurrentToken().type == TokenConstants.ID:
			new = asignacion()
		
		if tmp == None:
			tmp = new
		else:
			tmp.appendBro( new )
	if len(tmp.sons) > 0:
		return tmp
	else:
		return None
#selección → if ( expresión ) then bloque | if ( expresión ) then bloque else bloque
def seleccion():
	ifStmt = Node( TokenConstants.IF )
	tokensHelper.match( TokenConstants.IF )
	tokensHelper.match( "(" )
	ifStmt.addChild ( expresion() )
	tokensHelper.match( ")" )
	tokensHelper.match( "then" )
	ifStmt.addChild( bloque() )

	if( tokensHelper.getCurrentToken().content == TokenConstants.ELSE ):
		tokensHelper.match( TokenConstants.ELSE )
		ifStmt.addChild( bloque() )
	
	
	return ifStmt
	
#expresión → expresión-simple relación expresión-simple | expresión-simple
def expresion():
	exp = None
	tmp = expresion_simple()
	if( tokensHelper.getCurrentToken().content in _relacion ):
		exp = relacion()
		exp.addChild(tmp)
		exp.addChild( expresion_simple() )
	return exp

def relacion():
	rel = tokensHelper.getCurrentToken().content
	tokensHelper.match(TokenConstants.RELATION,True)
	return Node(rel)

#expresión-simple → expresión-simple suma-op termino | termino
#expresión-simple → termino { suma-op termino }
def expresion_simple():
	tmp = termino()
	while( tokensHelper.getCurrentToken().content in _suma_op):
		new = suma_op()
		new.addChild(tmp)
		new.addChild( termino() )
		tmp = new
	return tmp

def suma_op():
	rel = tokensHelper.getCurrentToken().content
	if(tokensHelper.getCurrentToken().type == TokenConstants.PLUS):
		tokensHelper.match(TokenConstants.PLUS,True)
	elif (tokensHelper.getCurrentToken().type == TokenConstants.LESS):
		tokensHelper.match(TokenConstants.LESS,True)
	return Node(rel)

#termino → termino mult-op factor | factor
#termino → factor { mult-op factor }
def termino():
	tmp = factor()
	while ( tokensHelper.getCurrentToken().content in _mult_op):
		new = mult_op();
		new.addChild(tmp)
		new.addChild( factor() )
		tmp = new
	return tmp

def mult_op():
	rel = tokensHelper.getCurrentToken().content
	if(tokensHelper.getCurrentToken().content == TokenConstants.TIMES):
		tokensHelper.match(TokenConstants.TIMES)
	elif (tokensHelper.getCurrentToken().content == TokenConstants.DIV):
		tokensHelper.match(TokenConstants.DIV)
	return Node(rel)

#factor → ( expresión ) | numero | identificador
def factor():
	new = None
	if tokensHelper.getCurrentToken().content == "(":
		tokensHelper.match("(")
		new = expresion()
		tokensHelper.match(")")
	
	elif tokensHelper.getCurrentToken().type == TokenConstants.INT:
		new = Node(tokensHelper.getCurrentToken().content)
		tokensHelper.match(TokenConstants.INT,True)

	elif tokensHelper.getCurrentToken().type == TokenConstants.ID:
		new = Node(tokensHelper.getCurrentToken().content)
		tokensHelper.match(TokenConstants.ID,True)

	return new

#iteración → while ( expresión ) bloque
def iteracion():
	new = Node( TokenConstants.WHILE )
	tokensHelper.match( TokenConstants.WHILE )
	tokensHelper.match("(")
	new.addChild( expresion() )
	tokensHelper.match(")")
	new.addChild( bloque() )
	return new

#repetición → do bloque until ( expresión ) ;
def repeticion():
	new = Node( TokenConstants.DO )
	tokensHelper.match( TokenConstants.DO )
	new.addChild( bloque() )
	tokensHelper.match("until")
	tokensHelper.match("(")
	new.addChild( expresion() )
	tokensHelper.match(")")
	tokensHelper.match(";")
	return new


#sent-cin → cin identificador ;
def sent_cin():
	new = Node("cin")
	tokensHelper.match("cin")
	new.addChild( Node(tokensHelper.getCurrentToken().content ) )
	tokensHelper.match(TokenConstants.ID,True)
	tokensHelper.match(";")	
	return new

#sent-cout → cout expresión ;
def sent_cout():	
	new = Node("cout")
	tokensHelper.match("cout")
	new.addChild( Node(tokensHelper.getCurrentToken().content ) )
	tokensHelper.match(TokenConstants.ID,True)
	tokensHelper.match(";")	
	return new

def bloque():
	tokensHelper.match("{")
	new = lista_sentencias()
	tokensHelper.match("}")
	return new
#asignación → identificador := expresión ;
def asignacion():
	new = Node(":=")
	new.addChild( Node(tokensHelper.getCurrentToken().content) )
	tokensHelper.match(TokenConstants.ID,True)
	tokensHelper.match(":=")
	new.addChild( expresion() )
	tokensHelper.match(";")	
	return new

#declaración → tipo lista-variables
def declaracion():
	tmp = Node(tokensHelper.getCurrentToken().content)
	tokensHelper.match(TokenConstants.ID,True)
	lista_variables(tmp)
	return tmp

#lista-variables → { identificador, } identificador
def lista_variables(parent):
	parent.addChild(Node(tokensHelper.getCurrentToken().content))
	tokensHelper.match(TokenConstants.ID,True)

	while tokensHelper.getCurrentToken().content == ",":
		tokensHelper.match(",")
		parent.addChild(Node(tokensHelper.getCurrentToken().content))
		tokensHelper.match(TokenConstants.ID,True)


if __name__ == "__main__":
	if len(sys.argv) > 0:
		sys.argv = ["Syntax.py","C:/Users/Eduardo/Dev/TinyPlusPlus-Compiler/Libre IDE/bin/Debug/core/syntax/goodBoy.lex"]

		#Tests:
		if sys.argv[1] == "-t":
			print("#### Tests for Syntax.py ####")
		else:
			tokensHelper = TokensHelper(sys.argv[1])
			programa()
	else:
		print("Invalid call to Syntax program... plase use:\n[python] Syntax.py tokensFile.out",file=sys.stderr)