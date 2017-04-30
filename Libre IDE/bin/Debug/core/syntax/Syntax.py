from Tree import *
from TokensHelper import *
################### ENDPOINTS
tipo = ["int","float","boolean"]
sentencia = ["if","while","do","cin","cout","{"]
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
	tmp = Node("lista-declaracion")
	while tokensHelper.getCurrentToken().content in tipo:
		tmp.addChild(declaracion())
		tokensHelper.match(";")
	if len(tmp.sons) > 0:
		return tmp
	else:
		return None
#lista-sentencias → sentencia lista-sentencias | sentencia | vació
#lista-sentencias → { sentencia }
#sentencia → selección | iteración | repetición | sent-cin |sent-out | bloque | asignación
def lista_sentencias():
	tmp = Node("lista-sentencias")
	while tokensHelper.getCurrentToken().content in tipo or tokensHelper.getCurrentToken().type == TokenConstants.ID:
		if tokensHelper.getCurrentToken().content == TokenConstants.IF:
			tmp.addChild( seleccion() )
		elif tokensHelper.getCurrentToken().content == TokenConstants.WHILE:
			tmp.addChild( iteracion() )
		elif tokensHelper.getCurrentToken().content == TokenConstants.CIN:
			tmp.addChild( sent_cin() )
		elif tokensHelper.getCurrentToken().content == TokenConstants.COUT:
			tmp.addChild( sent_cout() )
		elif tokensHelper.getCurrentToken().content == TokenConstants.BRACKET_OPEN:
			tmp.addChild( bloque() )
		elif tokensHelper.getCurrentToken().type == TokenConstants.ID:
			tmp.addChild( asignacion() )

	if len(tmp.sons) > 0:
		return tmp
	else:
		return None

def seleccion():
	return None

def iteracion():
	return None

#sent-cin → cin identificador ;
def sent_cin():
	new = Node("cin")
	tokensHelper.match("cin")
	new.addChild( Node(tokensHelper.getCurrentToken().content ) )
	tokensHelper.match(TokenConstants.ID,True)
	tokensHelper.match(";")	
	return new
	
def sent_cout():	
	new = Node("cout")
	tokensHelper.match("cout")
	new.addChild( Node(tokensHelper.getCurrentToken().content ) )
	tokensHelper.match(TokenConstants.ID,True)
	tokensHelper.match(";")	
	return new

def bloque():
	return None

def asignacion():
	return None

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
	if len(sys.argv) > 1:

		#Tests:
		if sys.argv[1] == "-t":
			print("#### Tests for Syntax.py ####")
		else:
			tokensHelper = TokensHelper(sys.argv[1])
			programa()
	else:
		print("Invalid call to Syntax program... plase use:\n[python] Syntax.py tokensFile.out",file=sys.stderr)