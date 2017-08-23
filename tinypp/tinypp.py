import sys
from lexer.Lexer import *
from syntax.Syntax import *

SINTAX_RUNMODE = "-s"
LEXIC_RUNMODE = "-l"

LEXIC_SECTION_LABEL = ("="*30)+" LEXIC "+("="*30)
SINTAX_SECTION_LABEL =("="*30)+" SYNTAX "+("="*30)

def error_cmd():
    print("Invalid tinypp command...")

def lexic(file):
    lex = Lexer(file)
    lex.eval()
    lex.close()

def sintactic(file,outputType):
    syntax= Syntax(file,outputType)
    syntax.go(file)
    
if __name__ == "__main__":
    #Check if by less we have 'python tinypp.py <other_argument>
    if len(sys.argv) > 1:
        ''' Get the command parameters '''
        runmode = sys.argv[1] # -l (Lexic) | -s (Sintax) | <none> (All)
        
        #Check for Lexic analysis
        if runmode == LEXIC_RUNMODE and len(sys.argv) > 2:
            lexic(sys.argv[2])
            
        #Check for Sintactic analysis
        elif runmode == SINTAX_RUNMODE and len(sys.argv) > 2:
            if len(sys.argv) > 3:
                sintactic(sys.argv[2],sys.argv[3])
            else:
                sintactic(sys.argv[2],Syntax.TYPE_JSON)
        else: # Run all
            filename = sys.argv[1]
            print(LEXIC_SECTION_LABEL)
            lexic(filename)
            print(SINTAX_SECTION_LABEL)
            sintactic(filename, Syntax.TYPE_TREE)
    else:
        error_cmd()
