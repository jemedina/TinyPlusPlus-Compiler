from Tree import *
from TokensHelper import *

def main():
	tokensHelper.match()
#programa → main “{“ lista-declaración lista-sentencias “}”
def programa():
	print("Unimplemented prorgama method")


if __name__ == "__main__":
	if len(sys.argv) > 1:

		#Tests:
		if sys.argv[1] == "-t":
			print("#### Tests for Syntax.py ####")
		else:
			tokensHelper = TokensHelper()
			main()
	else:
		print("Invalid call to Syntax program... plase use:\n[python] Syntax.py tokensFile.out",file=sys.stderr)