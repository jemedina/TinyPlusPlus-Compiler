from semantic.HashTable import *
from os import sys

STATEMENTS = [':=', 'if', 'repeat', 'while','cout','cin']
BOOL_OPERATORS = ['>', '<', '>=', '<=', '==', '!=']
MATH_OPERATORS = ['+', '-', '*', '/']
ERR = 'ERR'
KIND_REAL = 'real'
KIND_INT = 'int'
KIND_BOOL = 'boolean'
class Analyzer:
    def __init__(self, tree):
        self.tree=tree
        self.tabla=HashTable()
        self.preorder(self.tree.sons[0])
        self.posorder(self.tree.sons[1])
        TreeUtils.cliDisplay(self.tree)
        self.tabla.cliDisplayTable()


    def preorder(self, node):
        for i in range(len(node.sons)):
            node.sons[i].type = node.name
            #Avoid variable redeclaration
            if self.tabla.hasKey(node.sons[i].name):
            	self.semanticError("Variable '"+node.sons[i].name+"' was already declared",line=node.sons[i].line)
            else:
            	self.tabla.add(node.sons[i].name,node.sons[i].line,None,node.name)
        if node.bro != None:
            self.preorder(node.bro)

    def posorder(self, node):
        for son in node.sons:
            self.posorder(son)
        #Leer el nombre del nodo
        ''' Dependiendo del nombre del nodo puede pasar lo siguiente:
            Si es "==, !=, <=, >=, < ó >": 
                Si los dos hijos son identificadores entonces:
                    *Verificar tipos iguales
                Si un hijo es identificador:
                    *Verificar que el no-identificador sea compatible con el tipo de dato
                Si los dos hijos son no-identificadores:
                    *Verificar que sean compatibles entre si
                    *Asignar node.value = el resultado del operador logico
 
            Si es "+, -, *, /":
                Si los dos hijos son identificadores entonces:
                    *Verificar tipos iguales
                Si un hijo es identificador:
                    *Verificar que el no-identificador sea compatible con el tipo de dato
                Si los dos hijos son no-identificadores:
                    *Verificar que sean compatibles entre si
                    *Asignar node.value = el resultado del operador aritmetico
        NOTA: Si se encuentra el uso de alguna variable no 
        definida dentreo de este recorrido, lanzar un error
        de variable no definida

        '''

        '''for son in node.sons:
            if self.isStatement(son):
                self.posorder(son)
            else:
                self.assignAttrs(son)'''

        if self.isStatement(node):
            #ASIGNACIONES
            if node.name == ':=':
                self.evalAssign(node.sons[0], node.sons[1])
            #MATH OPERADORES
            elif node.name in MATH_OPERATORS:
                mathVal = str(self.evalMath(node.sons[0], node.sons[1], node.name, node.line))
                node.val = mathVal
                if mathVal == ERR:
                    node.type = ERR
                elif self.isFloat(mathVal):
                    node.type = KIND_REAL
                else:
                    node.type = KIND_INT
            #BOOL OPERADORES
            elif node.name in BOOL_OPERATORS:
                boolVal = str(self.evalBool(node.sons[0], node.sons[1], node.name, node.line))
                node.type = KIND_BOOL
                node.val = boolVal
            elif node.name in ['if', 'while']:
                self.verifyBooleanExpresion(node.sons[0])
            elif node.name in ['repeat']:
                self.verifyBooleanExpresion(node.sons[1])
        else:
            self.assignAttrs(node)

        #Rama completada, ir con el hermano
        if(node.bro != None):
            self.posorder(node.bro)

    def verifyBooleanExpresion(self, node):
        if node.type != KIND_BOOL:
            node.val = ERR

    def semanticError(self,message,line=None):
    	errMsg = "Semantic Error [" + message +"]" + ((" at line: "+line) if line != None else "")
    	print(errMsg, file=sys.stderr)

    def isStatement(self, node):
        return node.name != None and node.name != "" and \
            node.name in STATEMENTS or \
            node.name in BOOL_OPERATORS or \
            node.name in MATH_OPERATORS

    def assignAttrs(self, node):
        if node.name == 'error':
            node.type = 'syntax error'
            node.val = 'syntax error'
        elif node.name.isalpha():
            if self.tabla.hasKey(node.name):
                self.tabla.addLine(node.name, node.line)
                var = self.tabla.getKey(node.name)
                if var.getValue() != '<none>':
                    node.val = var.getValue()
                    node.type = var.type
                else:
                    node.type = var.type
                    node.val = '0'
            else:
                self.semanticError("Use of undefined variable '" + node.name + "'",line=node.line)
                node.val = ERR
                node.type = ERR

        elif self.isFloat(node.name):
            node.type = 'real'
            node.val = node.name
        elif node.name.isdigit():
            node.type = 'int'
            node.val = node.name

    def isFloat(self, strs):
        try:
            return float(strs) and '.' in strs
        except ValueError:
            return False

    def evalAssign(self, node1, node2):
        if node1.type == node2.type:
            node1.val = node2.val
            self.tabla.setValue(node1.name, node2.val)
        elif node1.type == KIND_INT and node2.type == KIND_REAL:
            intVal = self.getInt(node2.val)
            node1.val = intVal
            self.tabla.setValue(node1.name, intVal)
            if intVal == ERR:
                self.semanticError("Can't cast <real> to <int>", line=node1.line)
        elif node1.type == KIND_REAL and node2.type == KIND_INT:
            realVal = self.getReal(node2.val)
            node1.val = realVal
            self.tabla.setValue(node1.name, realVal)
        elif node1.type == KIND_BOOL and node2.type == KIND_INT:
            boolVal = self.getBoolean(node2.val)
            if boolVal != '0' and boolVal != '1':
                self.semanticError("Unable to cast <int> to <boolean>",line=node1.line)
                node1.val = ERR
            else:
                node1.val = boolVal
                self.tabla.setValue(node1.name, boolVal)
        else:
            node1.val = ERR
            self.tabla.setValue(node1.name, ERR)
            self.semanticError('<'+ node1.type + "> is not compatible with <" + node2.type+">",line=node1.line)
    
    def evalMath(self, node1, node2, op, opline):
        if node1.type != KIND_BOOL and node2.type != KIND_BOOL:
            if node1.val != ERR and node2.val != ERR:
                strA = str(node1.val)
                strB = str(node2.val)
                a = float(self.getReal(strA)) if self.isFloat(strA) else int(self.getInt(strA))
                b = float(self.getReal(strB)) if self.isFloat(strB) else int(self.getInt(strB))

                if op == '+':
                    return a+b
                elif op == '-':
                    return a-b
                elif op == '*':
                    return a*b
                elif op == '/':
                    if b == 0:
                        self.semanticError("Can't divide by zero!", line=opline)
                        return ERR
                    return a/b
                else:
                    return ERR
            else:
                return ERR
        else:
            self.semanticError("Unable to operate with booleans", line=opline)
            return ERR

    def evalBool(self, node1, node2, op, opline):
        if op != '==' and op != '!=' and (node1.type == KIND_BOOL or node2.type == KIND_BOOL):
            self.semanticError("The operator '"+op+"' can't be used with booleans",line=opline)
            return ERR
        elif op == '==':
            return '1' if node1.val == node2.val else '0'
        elif op == '!=':
            return '1' if node1.val != node2.val else '0'
        else: #<, >, <=, >= para numeros:
            strA = str(node1.val)
            strB = str(node2.val)
            a = float(self.getReal(strA)) if self.isFloat(strA) else int(self.getInt(strA))
            b = float(self.getReal(strB)) if self.isFloat(strB) else int(self.getInt(strB))
            if op == '>':
                return '1' if a > b else '0'
            elif op == '<':
                return '1' if a < b else '0'
            elif op == '>=':
                return '1' if a >= b else '0'
            elif op == '<=':
                return '1' if a <= b else '0'
    def getInt(self, value):
        strVal = str(value)
        if '.' in strVal:
            return ERR
        else:
            return strVal

    def getReal(self, value):
        strVal = str(value)
        if '.' in strVal:
            return strVal
        else:
            return strVal+".0"

    def getBoolean(self, value):
        strVal = str(value)
        if not strVal in ['1', '0']:
            return ERR
        else:
            return strVal

class TreeUtils:
	@staticmethod
	def cliDisplay(root,tabSpace="",hierarchy=0,isBrotherNode=False,lastSon=False,outFile=None,pathOfSouce=None,std=True):
		if outFile == None:
			outFile = open("tree.syn","+w",encoding='utf-8')
		if(root != None):
			if lastSon:
				tabSpace=(hierarchy*"│")+"└"
			else:
				if isBrotherNode:
					tabSpace=(hierarchy*"│")+"├"
				else:
					tabSpace=(hierarchy*"│")+"└"
			if std:
                            attrs=''
                            if hasattr(root,'type'):
                                attrs = " (type="+root.type
                            if hasattr(root,'val'):
                                attrs += ", val="+str(root.val)
                            attrs = (attrs + ")") if attrs != '' else ''
                            print(tabSpace+root.name + attrs)
			outFile.write(tabSpace+root.name)
			outFile.write("\n")
			for i in range(len(root.sons)):
				TreeUtils.cliDisplay(root.sons[i],tabSpace,hierarchy+1,lastSon=(i==len(root.sons)-1),outFile=outFile,std=std)
			if root.bro != None:
				TreeUtils.cliDisplay(root.bro,tabSpace,hierarchy,isBrotherNode=True,outFile=outFile,std=std)
