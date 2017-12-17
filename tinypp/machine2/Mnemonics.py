'''
Author: Eduardo Medina <jemedina.96@gmail.com>
'''
class Mnemonics:
	HALT = "HALT"
	IN = "IN"
	INR = "INR"
	INB = "INB"
	OUT = "OUT"
	OUTLN = "OUTLN"
	ADD = "ADD"
	SUB = "SUB"
	MUL = "MUL"
	DIV = "DIV"
	LD = "LD"
	ST = "ST"
	LDA = "LDA"
	LDC = "LDC"
	JLT = "JLT"
	JLE = "JLE"
	JGT = "JGT"
	JGE = "JGE"
	JEQ = "JEQ"
	JNE = "JNE"
	DEFINE = "DEFINE"

	#Esta constante es para validar que estamos usando mnemonicos validos
	ALL_MNEMONICS = ["INR","OUTLN","INB","DEFINE","HALT","IN","OUT","ADD","SUB","MUL","DIV","LD","ST","LDA","LDC","JLT","JLE","JGT","JGE","JEQ","JNE"]