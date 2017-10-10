class HashTableRow:
	def __init__(self, line=-1, value=None, memory=None, type=None):
		self.lines = [line]
		self.value = value
		self.memory = memory
		self.type = type
	def __str__(self):
		return "│{:<15}│{:<15}│{:<15}│{:<10}│".format(self.getLines(),self.getValue(),self.memory,self.type)

	def getLines(self):
		linesStr = ""
		for line in self.lines:
			linesStr += str(line) +", "
		
		linesStr = linesStr[:len(linesStr)-2]
		return linesStr
	
	def getValue(self):
		return '<none>' if self.value == None else self.value
	
class HashTable:
	def __init__(self):
		self.table = {}
		self.memoryIndex = 0

	def add(self,id,line,value,type):
		if(id in self.table):
			self.table[id].lines.append(line)			
			return True
		else:
			self.table[id] = HashTableRow(line,value,self.memoryIndex,type)
			self.memoryIndex += 1
			return False
	def addLine(self,id,line):
		if(id in self.table):
			self.table[id].lines.append(line)
			
	def hasKey(self, id):
		return id in self.table

	def getKey(self, id):
		return self.table[id]

	def cliDisplayTable(self):
		print("┼"+("─"*8)+"┼"+("─"*15)+"┼"+("─"*15)+"┼"+("─"*15)+"┼"+("─"*10)+"┼")
		print("│{:<8}│{:<15}│{:<15}│{:<15}│{:<10}│".format('ID','Lines','Value','Mem','Type'))
		
		print("┼"+("─"*8)+"┼"+("─"*15)+"┼"+("─"*15)+"┼"+("─"*15)+"┼"+("─"*10)+"┼")
		for item in self.table.items():
			#print("{:<8} {:<15} {:<10}".format(k, label, num))
			print("│{:<8}".format(item[0]) + str(item[1]))
			print("┼"+("─"*8)+"┼"+("─"*15)+"┼"+("─"*15)+"┼"+("─"*15)+"┼"+("─"*10)+"┼")
		