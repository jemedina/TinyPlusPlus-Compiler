import sys
from lexer.Lexer import *
from syntax.Syntax import *
from semantic.Semantic import *
from codegen2.CodeGen import *
SINTAX_RUNMODE = "-s"
LEXIC_RUNMODE = "-l"
SEMANTIC_RUNMODE = "-c"
CODEGEN_RUNMODE = "-g"

LEXIC_SECTION_LABEL = ("="*30)+" LEXIC "+("="*30)
SINTAX_SECTION_LABEL =("="*30)+" SYNTAX "+("="*30)
SEMANTIC_SECTION_LABEL =("="*30)+" SEMANTIC "+("="*30)
CODEGEN_SECTION_LABEL =("="*30)+" CODE GEN "+("="*30)

def error_cmd():
    print("Invalid tinypp command...")

def lexic(file):
    lex = Lexer(file)
    lex.eval()
    lex.close()
    #LEX_ERROR = lex.hasErrors
def sintactic(file,outputType):
    syntax= Syntax(file,outputType)
    global syntaxTree
    syntaxTree = syntax.go(file)

    #SIN_ERROR = syntax.hasErrors
    
def semantic(file,isCli=False,noOutputs=False):
    global hashTable
    semantic = Semantic(file,isCli,noOutputs)
    global semanticTree
    hashTable = semantic.getHashTable()
    semanticTree = semantic.getSemanticTree()

    #SEM_ERROR = semantic.hasErrors
    #global SOME_ERROR
    #SOME_ERROR = SEM_ERROR or SIN_ERROR or LEX_ERROR
def codegen(file):
    codegen = CodeGen(semanticTree,hashTable,file)

if __name__ == "__main__":
    #Check if by less we have 'python tinypp.py <other_argument>
    #sys.argv = ['C:\\Users\\Eduardo\\Dev\\TinyPlusPlus-Compiler\\tinypp\\tinypp.py',"C:\\Users\\Eduardo\\Desktop\\tinytests\\valid1.tiny"]
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
        elif runmode == SEMANTIC_RUNMODE and len(sys.argv) > 2:
            semantic(sys.argv[2])
        elif runmode == CODEGEN_RUNMODE and len(sys.argv) > 2 :
            semantic(sys.argv[2],noOutputs=True)
            codegen(sys.argv[2])
        else: # Run all
            filename = sys.argv[1]
            print(LEXIC_SECTION_LABEL)
            lexic(filename)
            print(SINTAX_SECTION_LABEL)
            sintactic(filename, Syntax.TYPE_TREE)
            print(SEMANTIC_SECTION_LABEL)
            semantic(filename,True)
            
            print(CODEGEN_SECTION_LABEL)
            codegen(filename)
            print("Ejecucion==============:")
            os.system("tinym.bat code.tm")            
    else:
        error_cmd()
