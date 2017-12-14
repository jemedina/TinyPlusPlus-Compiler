from semantic.HashTable import *
from semantic.Analyzer import * 
from semantic.DictionaryUtility import *
import json
import os
import ntpath
import platform

class Semantic:

	def __init__(self, path, isCli, noOutputs=True):
		#LOAD TREE
		jsonFile = self.openSyntaxTree(path)
		#self.tree = DictionaryUtility.to_object(json.load(jsonFile))
		self.tree = json.load(jsonFile)
		self.analyzer = Analyzer(self.tree)
		if isCli and noOutputs == False:
			TreeUtils.cliDisplay(self.analyzer.tree)
		
		self.analyzer.mockTree()
		if not isCli and noOutputs == False:
			print(json.dumps(self.analyzer.tree, indent=2, sort_keys=False))

		#self.analyzer.tabla.cliDisplayTable()

		#SAVE FILE STATEMENTS:
		pathOfSouce = path
		fileOpen = True
		canonicalFileName = ntpath.basename(pathOfSouce)
		withoutExtention = canonicalFileName[0:canonicalFileName.find(".")]
		synDirectory = "target_"+withoutExtention+"\\sem\\"
		basepath = ntpath.abspath(pathOfSouce)[0:len(ntpath.abspath(pathOfSouce))-len(canonicalFileName)]
		if  platform.system() != 'Linux':
			try: 
				os.makedirs(basepath+synDirectory)
			except OSError:
				pass
			errFile = open(basepath+synDirectory+"err.sem","+w")
			outFile = open(basepath+synDirectory+"out.sem","+w",encoding='utf-8')
			tablaFile = open(basepath+synDirectory+"tabla.sem","+w",encoding='utf-8')
			jsonFile = open(basepath+synDirectory+"out.json","+w",encoding='utf-8')
		else:
			synDirectory = "target_"+withoutExtention+"/sem/"
			try: 
				os.makedirs(synDirectory)
			except OSError:
				pass
			errFile = open(synDirectory+"err.sem","+w")
			outFile = open(synDirectory+"out.sem","+w",encoding='utf-8')
			tablaFile = open(basepath+synDirectory+"tabla.sem","+w",encoding='utf-8')
			jsonFile = open(synDirectory+"out.json","+w",encoding='utf-8')
		self.hasErrors = self.analyzer.hasErrors
		print(json.dumps(self.analyzer.tree, indent=2, sort_keys=False),file=jsonFile)
		print(self.analyzer.err,file=errFile)
		self.analyzer.tabla.fileDisplayTable(tablaFile)

	def getHashTable(self):
		return self.analyzer.tabla

	def getSemanticTree(self):
		return self.tree



	def getTree(self):
		return self.tree

	def openSyntaxTree(self, pathOfSouce):
		canonicalFileName = ntpath.basename(pathOfSouce)
		withoutExtention = canonicalFileName[0:canonicalFileName.find(".")]
		synDirectory = "target_"+withoutExtention+"\\syn\\"
		basepath = ntpath.abspath(pathOfSouce)[0:len(ntpath.abspath(pathOfSouce))-len(canonicalFileName)]
		if  platform.system() != 'Linux':
			try: 
				jsonFile = open(basepath+synDirectory+"out.json","r",encoding='utf-8')
				return jsonFile
			except OSError:
				pass
		else:
			synDirectory = "target_"+withoutExtention+"/syn/"
			try: 
				jsonFile = open(synDirectory+"out.json","r",encoding='utf-8')
				return jsonFile
			except OSError:
				pass
		return None
