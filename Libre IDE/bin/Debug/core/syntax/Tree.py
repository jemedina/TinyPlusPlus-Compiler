from os import sys
class Node:
	def __init__(self,name=None):
		self.name = name
		self.sons = []
	def addChild(self,childNode):
		if childNode != None:
			self.sons.append(childNode)
	def getChild(self,index):
		if len(self.sons) > index:
			return self.sons[index]
		else:
			return None

class TreeUtils:
	@staticmethod
	def cliDisplay(root,tabSpace="",hierarchy=0):
		if(root != None):
			tabSpace=(hierarchy*"  ")+"├"+("─"*(1))
			print(tabSpace+root.name)
			for son in root.sons:
				TreeUtils.cliDisplay(son,tabSpace,hierarchy+1)

if __name__ == '__main__':
#I'm lazy in this moment to make an professional unit tests.. better this:
	if len(sys.argv) > 1 and sys.argv[1] == "-t":
		print("##### Test for Tree.py #####")
		root = Node("root")
		root.addChild(Node("Son 0"))
		root.addChild(Node("Son 1"))
		root.addChild(Node("Son 2"))
		son1 = root.getChild(1)
		son1.addChild(Node("Grandchild 0"))
		son1.addChild(Node("Grandchild 1"))
		root.getChild(2).addChild(Node("Grandchild 0"))
		son1.getChild(0).addChild(Node("Very child xd 0"))
		TreeUtils.cliDisplay(root)