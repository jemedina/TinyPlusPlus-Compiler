from Tree import *
from TokensHelper import *
################### ENDPOINTS
tipo = ["int","float","boolean"]

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

def lista_sentencias():

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