from syntax.Tree import *
from syntax.TokensHelper import *
from syntax.Syntax import *
from unitTests import *
import random
import sys

def testWithoutErrors1():
    print("="*6,"Perfect test","="*6)
    
    s=Syntax("testCases/target_perfectTest/lex/out.lex","none")
    tree = s.go()
    assertThat("main",tree.name)
    assertThat("int",tree.getChild(0).name)
    assertThat("x",tree.getChild(0).getChild(0).name)
    assertThat(":=",tree.getChild(1).name)
    assertThat("x",tree.getChild(1).getChild(0).name)
    assertThat("1",tree.getChild(1).getChild(1))
    

nroErrors = 0
testWithoutErrors1()
