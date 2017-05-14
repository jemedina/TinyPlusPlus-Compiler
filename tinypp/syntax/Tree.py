from os import sys
class Node:
	def __init__(self,name=None):
		self.name = name
		self.sons = []
		self.bro = None
	def addChild(self,childNode):
		if childNode != None:
			self.sons.append(childNode)
	def getChild(self,index):
		if len(self.sons) > index:
			return self.sons[index]
		else:
			return None
	def addBro(self,broNode):
		self.bro = broNode
	def appendBro(self,broNode):
		if self.bro == None:
			self.bro = broNode
		else:
			tmp = self.bro
			while tmp.bro != None:
				tmp = tmp.bro
			tmp.bro = broNode
class TreeUtils:
	@staticmethod
	def cliDisplay(root,tabSpace="",hierarchy=0,isBrotherNode=False,lastSon=False):
		if(root != None):
			if lastSon:
				tabSpace=(hierarchy*"│")+"└"
			else:
				if isBrotherNode:
					tabSpace=(hierarchy*"│")+"├"
				else:
					tabSpace=(hierarchy*"│")+"└"
			print(tabSpace+root.name)
			for i in range(len(root.sons)):
				TreeUtils.cliDisplay(root.sons[i],tabSpace,hierarchy+1,lastSon=(i==len(root.sons)-1))
			if root.bro != None:
				TreeUtils.cliDisplay(root.bro,tabSpace,hierarchy,isBrotherNode=True)
