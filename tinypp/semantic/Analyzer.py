from semantic.HashTable import *
from os import sys

class Analyzer:
    def __init__(self, tree):
        self.tree=tree
        self.tabla=HashTable()
        self.preorder(self.tree.sons[0])
        TreeUtils.cliDisplay(self.tree)
        self.tabla.cliDisplayTable()


    def preorder(self, node):
        for i in range(len(node.sons)):
            node.sons[i].type = node.name
            #Avoid variable redeclaration
            if self.tabla.hasKey(node.sons[i].name):
            	self.semanticError("Variable '"+node.sons[i].name+"' ya estaba declarada",line=node.sons[i].line)
            else:
            	self.tabla.add(node.sons[i].name,node.sons[i].line,None,node.name)
        if node.bro != None:
            self.preorder(node.bro)
    def semanticError(self,message,line=None):
    	errMsg = "Semantic Error [" + message +"]" + (" at line: "+line) if line != None else ""
    	print(errMsg,file=sys.stderr)
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
                                attrs = " (type="+root.type+")"
                            print(tabSpace+root.name + attrs)
			outFile.write(tabSpace+root.name)
			outFile.write("\n")
			for i in range(len(root.sons)):
				TreeUtils.cliDisplay(root.sons[i],tabSpace,hierarchy+1,lastSon=(i==len(root.sons)-1),outFile=outFile,std=std)
			if root.bro != None:
				TreeUtils.cliDisplay(root.bro,tabSpace,hierarchy,isBrotherNode=True,outFile=outFile,std=std)
