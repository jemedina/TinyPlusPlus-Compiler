class Node:
	def __init__(self):
		self.left = None
		self.right = None
		self.value = None
	def __init__(self,val):
		self.left = None
		self.right = None
		self.value = val
	

class Tree:
	def __init__(self):
		self.root = None
	
	def add(self,newValue):
		if self.root == None:
			self.root = Node(newValue)
		else:
			parent = tmp = self.root
			while tmp != None:
				parent = tmp
				if tmp.value > newValue:
					tmp = tmp.left
				else:
					tmp = tmp.right
			if parent.value > newValue:
				parent.left = Node(newValue)
			else:
				parent.right = Node(newValue)

	def prefix(self,node):
		if(node != None):
			self.prefix(node.left)
			self.prefix(node.right)
			print(node.value)

	def displayPrefix(self):
		self.prefix(self.root)


t = Tree()
t.add(5)
t.add(2)
t.add(6)
t.add(0)
t.add(1)
t.displayPrefix()