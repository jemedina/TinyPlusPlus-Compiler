from syntax.Tree import *
from syntax.TokensHelper import *
from syntax.Syntax import *
import random
import sys
GREEN = '\x1b[6;30;42m'
RED   = "\033[1;30;31m"

def assertThat(expectedResult,result):
    if expectedResult == result:
        sys.stdout.write(GREEN)
        print("TEST OK")
    else:
        sys.stdout.write(RED)
        print("TEST FAILED: Was expected <"+str(expectedResult)+"> but was end in <"+str(result)+">")
    sys.stdout.write("\033[0;0m")
def evaluator(node):
    if node.name.isnumeric() or len(node.name)>1 and node.name[1:].isnumeric():
        return float(node.name)
    elif node.name == "+":
        return float(evaluator(node.getChild(0)))+float(evaluator(node.getChild(1)))
    elif node.name == "-":
        return float(evaluator(node.getChild(0)))-float(evaluator(node.getChild(1)))
    elif node.name == "*":
        return float(evaluator(node.getChild(0)))*float(evaluator(node.getChild(1)))
    elif node.name == "/":
        return float(evaluator(node.getChild(0)))/float(evaluator(node.getChild(1)))

def testEvaluator():
    print("="*6,"testEvaluator","="*6)
    root = Node("+")
    root.addChild(Node("2"))
    root.addChild(Node("2"))
    result = evaluator(root)
    assertThat(4,result)
    root = Node("*")
    root.addChild(Node("2"))
    root.addChild(Node("3"))
    result = evaluator(root)
    assertThat(6,result)
    root = Node("/")
    root.addChild(Node("2"))
    root.addChild(Node("2"))
    result = evaluator(root)
    assertThat(1,result)
    root = Node("-")
    root.addChild(Node("2"))
    root.addChild(Node("2"))
    result = evaluator(root)
    assertThat(0,result)

def multipleTestCases():
    print("="*6,"multipleTestCases","="*6)
    
    s=Syntax("testCases/target_test1/lex/out.lex","none")
    s.go()
    result = evaluator(s.root.getChild(0).getChild(1))
    assertThat(5+1+1+1+1+1,result)

    s=Syntax("testCases/target_test2/lex/out.lex","none")
    s.go()
    result = evaluator(s.root.getChild(0).getChild(1))
    assertThat(5+1*3-4/5*6-1*2-3*4,result)

    s=Syntax("testCases/target_test4/lex/out.lex","none")
    s.go()
    result = evaluator(s.root.getChild(0).getChild(1))
    assertThat(24+4-1*3/2+34-1,result)

    s=Syntax("testCases/target_test3/lex/out.lex","none")
    s.go()
    result = evaluator(s.root.getChild(0).getChild(1))
    assertThat(-19-8-7-6-5-4-3-2-1*(2+3+4+3+2),result)
#####TokensHelper Tests#####
def testTokensHelper():
    print("="*6,"TokensHelper","="*6)

    testIsEOF()

def testIsEOF():
    print("-- test isEOF() -- ")
    #This Test Case has 12 tokens + eof
    t = TokensHelper("testCases/target_test1/lex/out.lex")
    t.loadTokens()
    
    endOfFile = False
    assertThat(endOfFile,t.isEOF())
    
    #Consume the 13 tokens
    numOfTokens = 13 #13 token is $ 
    for i in range(numOfTokens):
        t.getToken()

    endOfFile = True
    assertThat(endOfFile,t.isEOF())

def testConjuntoPrimero():
    print("="*6,"test conjunto primero","="*6)
    print("--main--")
    expected = set(["main"])
    assertThat(expected,set(primero("main")))
    print("--lista-declaracion--")
    expected =set(["$","int","float","boolean"])
    assertThat(expected,set(primero("lista-declaracion")))
    print("--declaracion--")
    expected =set(["int","float","boolean"])
    assertThat(expected,set(primero("declaracion")))
    print("--tipo--")
    expected =set(["int","float","boolean"])
    assertThat(expected,set(primero("tipo")))
    print("--lista-variables--")
    expected =set(["identificador"])
    assertThat(expected,set(primero("lista-variables")))
    print("--lista-sentencias--")
    expected =set(["if","while","do","cin","cout","{","identificador","$"])
    assertThat(expected,set(primero("lista-sentencias")))
    print("--sentencia--")
    expected =set(["if","while","do","cin","cout","{","identificador"])
    assertThat(expected,set(primero("sentencia")))
    print("--seleccion--")
    expected =set(["if"])
    assertThat(expected,set(primero("seleccion")))
    print("--iteracion--")
    expected =set(["while"])
    assertThat(expected,set(primero("iteracion")))
    print("--repeticion--")
    expected =set(["do"])
    assertThat(expected,set(primero("repeticion")))
    print("--sent-cin--")
    expected =set(["cin"])
    assertThat(expected,set(primero("sent-cin")))
    print("--sent-cout--")
    expected =set(["cout"])
    assertThat(expected,set(primero("sent-cout")))
    print("--bloque--")
    expected =set(["{"])
    assertThat(expected,set(primero("bloque")))
    print("--asignacion--")
    expected =set(["identificador"])
    assertThat(expected,set(primero("asignacion")))
    print("--expresion--")
    #TODO Ask if this is correct
    expected =set(['-', 'identificador', '*', '(', 'numero', '/', '+'])
    assertThat(expected,set(primero("expresion")))
    print("--expresion-simple--")
    expected =set(['-', 'identificador', '*', '(', 'numero', '/', '+'])
    assertThat(expected,set(primero("expresion-simple")))
    print("--suma-op--")
    expected =set(['-', '+'])
    assertThat(expected,set(primero("suma-op")))
    print("--mult-op--")
    expected =set(['*', '/'])
    assertThat(expected,set(primero("mult-op")))
    print("--factor--")
    expected =set(['(', 'numero', 'identificador'])
    assertThat(expected,set(primero("factor")))
if __name__ == "__main__":
    testEvaluator()
    multipleTestCases()
    testTokensHelper()
    testConjuntoPrimero()