
'''
Author: Eduardo Medina <jemedina.96@gmail.com>
'''
class Utils:

	@staticmethod
	def getDataType(arg):
		if Utils.isFloat(arg):
			return 'real'
		elif Utils.isInt(arg):
			return 'int'
		elif arg == True or arg == False:
			return 'boolean'


	@staticmethod
	def isFloat(line):
		line = str(line)
		if '.' in line:
			try:
				line=float(line)
				return True
			except:
				return False
		else:
			return False

	@staticmethod
	def isInt(line):
		line = str(line)
		if not '.' in line:
			try:
				line=int(line)
				return True
			except:
				return False			
		else:
			return False
	@staticmethod
	def intToFloat(arg):
		return float(arg)


	@staticmethod
	def floatToInt(arg):
		return int(arg)