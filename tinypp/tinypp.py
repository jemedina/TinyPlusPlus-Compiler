import sys
from lexer.Lexer import *
from syntax.Syntax import *
TAG_SINTAX = "-s"
TAG_LEXIC = "-l"
def error_cmd():
    print("Invalid tinypp command...")

def lexic(file):
    lex = Lexer(file)
    lex.eval()
    lex.close()

def sintactic(lexFile):
    syntax= Syntax(lexFile)
    syntax.go()
    
if __name__ == "__main__":
    #Check if by less we have 'python tinypp.py <other_argument>
    if len(sys.argv) > 1:
        #Check for Lexic analysis
        if sys.argv[1] == TAG_LEXIC and len(sys.argv) > 2:
            lexic(sys.argv[2])
            
        #Check for Sintactic analysis
        elif sys.argv[1] == TAG_SINTAX and len(sys.argv) > 2:
            sintactic(sys.argv[2])
        else:
            error_cmd()
    else:
        error_cmd()
