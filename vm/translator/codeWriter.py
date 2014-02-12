"""
Addresses:
0-15: 			Virtual Registers (SP, LCL, ARG, THIS, THAT)
	0: SP
	1: LCL
	2: ARG
	3: THIS
	4: THAT
	5-12: TEMP
	13-15: GENERAL PURPOSE

16-255: 		Static
256-2047: 		Stack
2048-16383: 	Heap

POP:

POP top value in stack to ADDR value of SEGMENT type
decrease SP (stack pointer) by 1

PUSH:

PUSH new value to the top of stack with the value of SEGMENT ADDR
increase SP by 1
"""

class CodeWriter( object ):
	def __init__(self, outfile):
		super(CodeWriter, self).__init__()
		self.outfile = outfile
		self.hackLines = []
		self.compileFunctions = {
			'C_ARITHMETIC' : self.compileArithmetic,
			'C_PUSH' : self.compilePush,
			'C_POP' : self.compilePop
		}
		self.labels = {
			'local':'LCL',
			'argument':'ARG',
			'this':'THIS',
			'that':'THAT',
			'temp':'TEMP',
		}
		self.pointers = {
			'SP': 0,
			'LCL': 1,
			'ARG': 2,
			'THIS': 3,
			'THAT': 4,
			'TEMP': 5
		}
		print self.outfile

	def compileArithmetic(self,args):
		print 'compile arithmetic '

	def compilePush(self,args):
		segment = args[0]
		value = int(args[1])

		if segment == 'constant':
			self.hackLines.append('@' + `value`) #set A to the constant value
			self.hackLines.append('D=A') #put that in D
			self.hackLines.append('@0') #set A to SP address
			self.hackLines.append('A=M') #set A to SP
			self.hackLines.append('M=D') #set the address of SP to the value of D
			self.hackLines.append('@0') #increment SP
			self.hackLines.append('M=M+1')
		else:
			self.hackLines.append('@' + `self.pointers[self.labels[segment]]`) #set A to the segment base pointer
			self.hackLines.append('D=M') #get segment base address value and prep A
			self.hackLines.append('@' + `value`) #set A to offset
			self.hackLines.append('D=D+A') #compute address of RAM we want to push
			self.hackLines.append('A=D') #set A to the RAM address we just made
			self.hackLines.append('D=M') #set D to the value that that RAM address stores

			self.hackLines.append('@0') #set A to SP address
			self.hackLines.append('A=M') #set A to the SP
			self.hackLines.append('M=D') #save what is in D to where the SP points at at the moment
			self.hackLines.append('@0') #set A to address of SP
			self.hackLines.append('M=M+1') #increase SP by 1

	def compilePop(self,args):
		print 'compile pop'

	def printHackLines(self):
		for l in self.hackLines:
			print l

	def resolveCommand(self, commandType, args):
		self.compileFunctions[commandType](args);


