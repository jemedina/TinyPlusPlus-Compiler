from syntax.Tree import *
from syntax.TokensHelper import *
from syntax.Syntax import Syntax
import random
def assertThat(expectedResult,result):
    if expectedResult == result:
        print("TEST OK")
    else:
        print("TEST FAILED: Was expected <"+str(expectedResult)+"> but was end in <"+str(result)+">")

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

if __name__ == "__main__":
    testEvaluator()
    multipleTestCases()
    testTokensHelper()