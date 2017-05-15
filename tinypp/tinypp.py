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

def sintactic(lexFile,outputType):
    syntax= Syntax(lexFile,outputType)
    syntax.go()
    
if __name__ == "__main__":
    #sys.argv = ["tinypp.py","-s","testCases/target_test5/lex/out.lex","none"]
    #Check if by less we have 'python tinypp.py <other_argument>
    if len(sys.argv) > 1:
        #Check for Lexic analysis
        if sys.argv[1] == TAG_LEXIC and len(sys.argv) > 2:
            lexic(sys.argv[2])
            
        #Check for Sintactic analysis
        elif sys.argv[1] == TAG_SINTAX and len(sys.argv) > 2:
            if len(sys.argv) > 3:
                sintactic(sys.argv[2],sys.argv[3])
            else:
                sintactic(sys.argv[2],"json")
        else:    
            error_cmd()
    else:
        error_cmd()
