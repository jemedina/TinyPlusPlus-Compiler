from semantic.HashTable import *
from os import sys
import json
#Declaramos diccionario de palabras
STATEMENTS = [':=', 'if', 'repeat', 'while','cout','cin']
BOOL_OPERATORS = ['>', '<', '>=', '<=', '==', '!=']
MATH_OPERATORS = ['+', '-', '*', '/']
ERR = 'ERR'
KIND_REAL = 'real'
KIND_INT = 'int'
KIND_BOOL = 'boolean'
#Clase del analizador semantico
class Analyzer:
    #Constructor
    def __init__(self, tree):
        self.tree=tree
        self.tabla=HashTable()
        self.err = ""
        self.std = ""
        #Verificamos que existan los dos nodos principales
        if len(self.tree['sons']) > 1:
            self.preorder(self.tree['sons'][0])
            self.posorder(self.tree['sons'][1])
        else:
            if len(self.tree['sons']) == 1:
                if self.tree['sons'][0]['name'] in [KIND_REAL,KIND_BOOL,KIND_INT]:
                    self.preorder(self.tree['sons'][0])
                else:
                    self.posorder(self.tree['sons'][0])
                
        #self.tabla.cliDisplayTable()

    def mockTree(self):
        self.mock(self.tree)

    #Esta funcion sirve para añadir variables nulas a objetos que no las tienen
    def mock(self,root):
        if not 'type' in root:
            root['type'] = None
        if not 'val' in root:
            root['val'] = None
        if not 'line' in root:
            root['line'] = None
        for son in root['sons']:
            self.mock(son)
        if root['bro'] != None:
            self.mock(root['bro'])

    #Recorrer rama izquierda de las variables
    def preorder(self, node):
        for i in range(len(node['sons'])):
            node['sons'][i]['type'] = node['name']
            #Avoid variable redeclaration
            if self.tabla.hasKey(node['sons'][i]['name']):
            	self.semanticError("Variable '"+node['sons'][i]['name']+"' was already declared",line=node['sons'][i]['line'])
            else:
            	self.tabla.add(node['sons'][i]['name'],node['sons'][i]['line'],None,node['name'])
        if node['bro'] != None:
            self.preorder(node['bro'])

    def posorder(self, node):
        for son in node['sons']:
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
                    *Asignar node['val']ue = el resultado del operador logico
 
            Si es "+, -, *, /":
                Si los dos hijos son identificadores entonces:
                    *Verificar tipos iguales
                Si un hijo es identificador:
                    *Verificar que el no-identificador sea compatible con el tipo de dato
                Si los dos hijos son no-identificadores:
                    *Verificar que sean compatibles entre si
                    *Asignar node['val']ue = el resultado del operador aritmetico
        NOTA: Si se encuentra el uso de alguna variable no 
        definida dentreo de este recorrido, lanzar un error
        de variable no definida

        '''

        '''for son in node['sons']:
            if self.isStatement(son):
                self.posorder(son)
            else:
                self.assignAttrs(son)'''
        #Funcion de Decalraciones
        if self.isStatement(node):
            #ASIGNACIONES
            if node['name'] == ':=':#Preguntar si el nodo es un :=
                self.evalAssign(node['sons'][0], node['sons'][1])#Si fue := mandamos a llamar a la funcion evalAssign con sus dos hijos
            #MATH OPERADORES
            elif node['name'] in MATH_OPERATORS:#Preguntar si el nodo es un operador matematico
                #Si fue un operador matematico mandamos a llamar a la funcion evalMath con sus dos hijos, el operador que fue y la linea 
                mathVal = str(self.evalMath(node['sons'][0], node['sons'][1], node['name'], node['line']))
                #print(mathVal + node['sons'][0],file=sys.stderr)
                #Se asigna el valor del a la variable mathVal   
                node['val'] = mathVal
                #Vereficiar que la variable antes creada no sea un error si no para indicarlo
                if mathVal == ERR:
                    node['type'] = ERR
                #Si la variable es indicaremos que es real para la tabla has y si no es flotante solo indicaremos que es entera
                elif self.isFloat(mathVal):
                    node['type'] = KIND_REAL
                else:
                    node['type'] = KIND_INT
            #BOOL OPERADORES
            #Preguntar si el nodo es un operador booleano
            elif node['name'] in BOOL_OPERATORS:
                #Si fue un operador booleano mandamos a llamar a la funcion evalMath con sus dos hijos, el operador que fue y la linea
                boolVal = str(self.evalBool(node['sons'][0], node['sons'][1], node['name'], node['line']))
                #Asignamos el tipo al nodo
                node['type'] = KIND_BOOL
                #Creamos una variable con el valor del noddo
                node['val'] = boolVal
            #Si fue if,while o repeat mandamos a llamar a la funcion verifyBooleanExpresion ya sea con el primero o con el segundo hijo
            elif node['name'] in ['if', 'while']:
                self.verifyBooleanExpresion(node['sons'][0])
            elif node['name'] in ['repeat']:
                self.verifyBooleanExpresion(node['sons'][1])
        #Si no fue nada de lo anterior se llama a la funcion que verifique si es error o variable
        else:
            self.assignAttrs(node)

        #Rama completada, ir con el hermano
        if(node['bro'] != None):
            self.posorder(node['bro'])
    #Esta funcion solo verifica que el operador se encuentre en el diccionario de operadores booleanos si no para mandarlo como error
    def verifyBooleanExpresion(self, node):
        if node['type'] != KIND_BOOL:
            node['val'] = ERR
    #Esta funcion manda el mensaje de error dependiendo de donde se le llame y con el concepto del error
    def semanticError(self,message,line=None):
        errMsg = "Semantic Error [" + message +"]" + ((" at line: "+line) if line != None else "")
        self.err += errMsg+"\n"
        print(errMsg, file=sys.stderr)
    '''Esta funcion define que sea una declaracion que no sea vacia y se encuentre en los diccionarios de declaraciones, operadores booleanos 
    y matematicos'''
    def isStatement(self, node):
        return node['name'] != None and node['name'] != "" and \
            node['name'] in STATEMENTS or \
            node['name'] in BOOL_OPERATORS or \
            node['name'] in MATH_OPERATORS 
    def assignAttrs(self, node):
        #Si el nodo es error solo se indica el tipo del error y el valor para la tabla hash
        if node['name'] == 'error':
            node['type'] = 'syntax error'
            node['val'] = 'syntax error'
        #Si fue una letra 
        elif node['name'].isalpha():
            #Si ya se encuentra en la tabla hash 
            if self.tabla.hasKey(node['name']):
                #Agregamos la linea solamente
                self.tabla.addLine(node['name'], node['line'])
                var = self.tabla.getKey(node['name'])
                #Si tiene un valor diferente a none asignamos el tipo y el valor si no solo asignamos 0
                if var.getValue() != '<none>':
                    node['val'] = var.getValue()
                    node['type'] = var.type
                else:
                    node['type'] = var.type
                    node['val'] = '0'
            #Si no es encuentra en la tabla mandamos error de variable no declarada
            else:
                self.semanticError("Use of undefined variable '" + node['name'] + "'",line=node['line'])
                node['val'] = ERR
                node['type'] = ERR
        #Si el nodo es un flotante aguardamos su tipo como real y su valor
        elif self.isFloat(node['name']):
            node['type'] = 'real'
            node['val'] = node['name']
        #Si el nodo es un digito aguardamos su tipo como int y su valor
        elif node['name'].isdigit():
            node['type'] = 'int'
            node['val'] = node['name']
    #Funcion que define si el string es flotante 
    def isFloat(self, strs):
        try:
            return float(strs) and '.' in strs
        except ValueError:
            return False
    #Funcion que define las asignaciones        
    def evalAssign(self, node1, node2):
        #Si los tipos de los nodos son iguales
        if node1['type'] == node2['type']:
            #Se guarda el valor del node2 en el node1
            node1['val'] = node2['val']
            #Si se encuentra en la tabla hash se guaradar el valor nuevo
            if self.tabla.hasKey(node1['name']):
                self.tabla.setValue(node1['name'], node2['val'])
            #Si no se encuentra en la tabla hash se mada error
            else:
                self.semanticError("Use of undefined variable '" + node1['name'] + "'",line=node1['line'])
        #Si el node1 es int y el node2 es real
        elif node1['type'] == KIND_INT and node2['type'] == KIND_REAL:
            #Se crea una variable con el valor entero del node2 y se asigna al node1
            intVal = self.getInt(node2['val'])
            node1['val'] = intVal
            #Si se encuentra en la tabla hash se guaradar el valor nuevo y si no se manda el error
            if self.tabla.hasKey(node1['name']):
                self.tabla.setValue(node1['name'], intVal)
            else:
                self.semanticError("Use of undefined variable '" + node1['name'] + "'",line=node1['line'])
            #Si el node2 traia un valor de error se mandara el error semantico
            if intVal == ERR:
                self.semanticError("Can't cast <real> to <int>", line=node1['line'])
        #Se aplica la misma logica que lo anteriro solo que comparando real con int es decir todo lo que se guarde sera real
        elif node1['type'] == KIND_REAL and node2['type'] == KIND_INT:
            realVal = self.getReal(node2['val'])
            node1['val'] = realVal
            if self.tabla.hasKey(node1['name']):
                self.tabla.setValue(node1['name'], realVal)
            else:
                self.semanticError("Use of undefined variable '" + node1['name'] + "'",line=node1['line'])
        #Si se quiere compara un operador con un int
        elif node1['type'] == KIND_BOOL and node2['type'] == KIND_INT:
            #Se obtiene el valor numerico booleano es decir 1 o 0 
            boolVal = self.getBoolean(node2['val'])
            #Si el valor es diferente de 0 o 1 mandamos error si no es asi se asigna el valor en la tabla
            if boolVal != '0' and boolVal != '1':
                self.semanticError("Unable to cast <int> to <boolean>",line=node1['line'])
                node1['val'] = ERR
            else:
                node1['val'] = boolVal
                self.tabla.setValue(node1['name'], boolVal)
        #Si no fue nada de lo anterior se ,amdara como un error
        else:
            node1['val'] = ERR
            if self.tabla.hasKey(node1['name']):
                self.tabla.setValue(node1['name'], ERR)
                self.semanticError('<'+ node1['type'] + "> is not compatible with <" + node2['type']+">",line=node1['line'])
            #else:
            #    self.semanticError("Use of undefined variable '" + node1['name'] + "'",line=node1['line'])

    #Funcion de evaluaciones matematicas
    def evalMath(self, node1, node2, op, opline):
        #Verificamos que los nodos sean diferentes de un booleano y diferentes de un error
        if node1['type'] != KIND_BOOL and node2['type'] != KIND_BOOL:
            if node1['val'] != ERR and node2['val'] != ERR:
                #Guardamos el string del valor
                strA = str(node1['val'])
                strB = str(node2['val'])
                #Asignamos los tipos de los nodos si es real o int
                a = float(self.getReal(strA)) if self.isFloat(strA) else int(self.getInt(strA))
                b = float(self.getReal(strB)) if self.isFloat(strB) else int(self.getInt(strB))
                #Se realizan las operaciones dependiendo del operador
                if op == '+':
                    if node1['type'] == KIND_INT and node2['type'] == KIND_INT:
                        return self.parseInt(a+b)
                    else:
                        return a+b
                elif op == '-':
                    if node1['type'] == KIND_INT and node2['type'] == KIND_INT:
                        return self.parseInt(a-b)
                    else:
                        return a-b
                elif op == '*':
                    if node1['type'] == KIND_INT and node2['type'] == KIND_INT:
                        return self.parseInt(a*b)
                    else:
                        return a*b
                elif op == '/':
                    #Se valida que no se pueda dividir entre 0
                    if b == 0:
                        self.semanticError("Can't divide by zero!", line=opline)
                        return ERR
                    if node1['type'] == KIND_INT and node2['type'] == KIND_INT:
                        return self.parseInt(a/b)
                    else:
                        return a/b
        #Se mandan los errores a los primeros 2 if's respectivamente
            else:
                return ERR
        else:
            self.semanticError("Unable to operate with booleans", line=opline)
            return ERR
    #Funcion de evaluaciones booleanas
    def evalBool(self, node1, node2, op, opline):
        #Verificamos que el operador sea un operador booleano y que los nodos sean de tipo booleano 
        if op != '==' and op != '!=' and (node1['type'] == KIND_BOOL or node2['type'] == KIND_BOOL):
            self.semanticError("The operator '"+op+"' can't be used with booleans",line=opline)
            return ERR
        #Si el operador es un "==" o "!=" se verifica que ninguno de los nodos sea error y si no es haci se hace la comparacion respectiva al operador
        elif op == '==':
            if node1['val'] == ERR or node2['val'] == ERR:
                return ERR
            else:
                return '1' if node1['val'] == node2['val'] else '0'
        elif op == '!=':
            if node1['val'] == ERR or node2['val'] == ERR:
                return ERR
            else:
                return '1' if node1['val'] != node2['val'] else '0'
        else: #<, >, <=, >= para numeros:
            #Para los operadores <,>,<=,>= primero se guardan los valores de los nodos asi como su tipo rela o int
            strA = str(node1['val'])
            strB = str(node2['val'])
            if strA==ERR or strB ==ERR:
                return ERR
            a = float(self.getReal(strA)) if self.isFloat(strA) else int(self.getInt(strA))
            b = float(self.getReal(strB)) if self.isFloat(strB) else int(self.getInt(strB))
            #Se verifica que ninguno de los nodos tenga el valor de error y si no es asi se realiza la comparacion dependiendo del operador 
            if op == '>':
                if node1['val'] == ERR or node2['val'] == ERR:
                    return ERR
                else:
                    return '1' if a > b else '0'
            elif op == '<':
                if node1['val'] == ERR or node2['val'] == ERR:
                    return ERR
                else:
                    return '1' if a < b else '0'
            elif op == '>=':
                if node1['val'] == ERR or node2['val'] == ERR:
                    return ERR
                else:    
                    return '1' if a >= b else '0'
            elif op == '<=':
                if node1['val'] == ERR or node2['val'] == ERR:
                    return ERR
                else: 
                    return '1' if a <= b else '0'
    #Funcion que regresa el valor int de un string
    def getInt(self, value):
        strVal = str(value)
        if '.' in strVal:
            return ERR
        else:
            return strVal
    #Funcion que regresa la parte entera de un flotante
    def parseInt(self, value):
        strVal = str(value)
        if '.' in strVal:
            return strVal.split(".")[0]
        else:
            return strVal
    #Funcion que regresa el valor real de un string
    def getReal(self, value):
        strVal = str(value)
        if '.' in strVal:
            return strVal
        else:
            return strVal+".0"
    #Funcion que regresa el valor booleano de un string
    def getBoolean(self, value):
        strVal = str(value)
        if not strVal in ['1', '0']:
            return ERR
        else:
            return strVal
#Metodo para pintar el arbol en consola
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
                            if 'type' in root:
                                attrs = " (type="+root['type']
                            if 'val' in root:
                                attrs += ", val="+str(root['val'])
                            attrs = (attrs + ")") if attrs != '' else ''
                            print(tabSpace+root['name'] + attrs)
			outFile.write(tabSpace+root['name'])
			outFile.write("\n")
			for i in range(len(root['sons'])):
				TreeUtils.cliDisplay(root['sons'][i],tabSpace,hierarchy+1,lastSon=(i==len(root['sons'])-1),outFile=outFile,std=std)
			if root['bro'] != None:
				TreeUtils.cliDisplay(root['bro'],tabSpace,hierarchy,isBrotherNode=True,outFile=outFile,std=std)
