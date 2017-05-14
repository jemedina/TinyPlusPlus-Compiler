import sys
runtimePath = sys.argv[0][0:len(sys.argv[0])-len("tinypp.py")]
statesProperties = runtimePath+"lexer\config\states.properties"

class StateManager:

	def __init__(self):
		self.states = {}
		with open(statesProperties) as configFile:
			for lineConf in configFile:
				lineConf = lineConf.replace("\n","")
				register = lineConf.split("=")
				self.states[ register[0] ] = register[1]

	def setState(self,state):
		self.state = state

	def getState(self):
		try:
			stateToReturn = self.states[self.state]	
		except:
			stateToReturn = -1
		return stateToReturn

	def getStateByName(self,stateName):
		return self.states[stateName]

	def getStateName(self,index):
		for tempState in states:
		    if states[tempState] == index:
		        return tempState
		return -1

