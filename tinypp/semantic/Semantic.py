from semantic.HashTable import *
from semantic.Analyzer import * 
from semantic.DictionaryUtility import *
import json
import os
import ntpath
import platform


class Semantic:

	def __init__(self, path):
		#LOAD TREE
		jsonFile = self.openSyntaxTree(path)
		self.tree = DictionaryUtility.to_object(json.load(jsonFile))

		self.analyzer = Analyzer(self.tree)

		### TEST HASH TABLE ###
		hashTable = HashTable()
		hashTable.add('x',1,None,'int')
		hashTable.add('y',3,None,'int')
		hashTable.add('y',5,None,'int')
		hashTable.cliDisplayTable()
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
