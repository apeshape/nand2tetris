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
	def __init__( self, outfile ):
		super(CodeWriter, self).__init__()
		self.outfile = open('vmlabb.asm','w')
		self.hackLines = []
		self.uniqueLabelCount = 0
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
			'temp':'R5',
			'pointer':'THIS'
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

	def uniqueLabel( self ):
		label = 'L$' + `self.uniqueLabelCount`
		self.uniqueLabelCount = self.uniqueLabelCount + 1
		return label

	def writeLn( self, op ):
		self.hackLines.append(op)
		self.outfile.write(op + '\n')

	def unary( self, arType ):
		self.writeLn('@SP')
		self.writeLn('AM=M-1')

		if arType == 'neg':
			self.writeLn('D=-M')
		if arType == 'not':
			self.writeLn('D=!M')

		self.writeLn('M=D')
		self.writeLn('@SP')
		self.writeLn('M=M+1')

	def cmp( self, arType ):
		ifTrue = self.uniqueLabel()
		ifFalse = self.uniqueLabel()
		endIf = self.uniqueLabel()

		#pop 1st value and save in R13
		self.writeLn('@SP') # prep A with SP
		self.writeLn('AM=M-1') # set A to *SP
		self.writeLn('D=M') # store the value that SP points to
		self.writeLn('@R13')
		self.writeLn('M=D') # store value in R13

		#pop 2nd value and put in D
		self.writeLn('@SP')
		self.writeLn('AM=M-1')
		self.writeLn('D=M')

		#get 1st value from R13 and put in A
		self.writeLn('@R13')
		self.writeLn('A=M')

		self.writeLn('D=D-A')

		if arType == 'eq':
			self.writeLn('@' + ifTrue)
			self.writeLn('D;JEQ')
			self.writeLn('@' + ifFalse)
			self.writeLn('D;JNE')
		if arType == 'gt':
			self.writeLn('@' + ifTrue)
			self.writeLn('D;JGT')
			self.writeLn('@' + ifFalse)
			self.writeLn('D;JLE')
		if arType == 'lt':
			self.writeLn('@' + ifTrue)
			self.writeLn('D;JLT')
			self.writeLn('@' + ifFalse)
			self.writeLn('D;JGE')


		self.writeLn('(' + ifTrue + ')')
		self.writeLn('@SP')
		self.writeLn('A=M')
		self.writeLn('M=-1')
		self.writeLn('@SP')
		self.writeLn('M=M+1')
		self.writeLn('@' + endIf)
		self.writeLn('0;JMP')
		self.writeLn('(' + ifFalse + ')')
		self.writeLn('@SP')
		self.writeLn('A=M')
		self.writeLn('M=0')
		self.writeLn('@SP')
		self.writeLn('M=M+1')
		self.writeLn('('+endIf+')')


	def add( self, arType ):
		#pop X and store in R13
		self.writeLn('@SP') # prep A with SP
		self.writeLn('AM=M-1') # set A to *SP
		self.writeLn('D=M') # store the value that SP points to
		self.writeLn('@R13')
		self.writeLn('M=D')

		#pop Y and store in D
		self.writeLn('@SP') # prep A with SP
		self.writeLn('AM=M-1') # set A to *SP
		self.writeLn('D=M') # store the value that SP points to

		#get X from R13
		self.writeLn('@R13')
		self.writeLn('A=M')
		if arType == 'sub':
			self.writeLn('D=D-A')
		else:
			self.writeLn('D=D+A')
		self.writeLn('@SP')
		self.writeLn('AM=M')
		self.writeLn('M=D')
		self.writeLn('@SP')
		self.writeLn('M=M+1')

	def andOr( self, arType ):
		#pop 1st value and save in R13
		self.writeLn('@SP') # prep A with SP
		self.writeLn('AM=M-1') # set A to *SP
		self.writeLn('D=M') # store the value that SP points to
		self.writeLn('@R13')
		self.writeLn('M=D') # store value in R13

		#pop 2nd value and put in D
		self.writeLn('@SP')
		self.writeLn('AM=M-1')
		self.writeLn('D=M')

		#get 1st value from R13 and put in A
		self.writeLn('@R13')
		self.writeLn('A=M')

		if arType == 'or':
			self.writeLn('D=D|A')
		if arType == 'and':
			self.writeLn('D=D&A')

		self.writeLn('@SP')
		self.writeLn('A=M')
		self.writeLn('M=D')
		self.writeLn('@SP')
		self.writeLn('M=M+1')



	def compileArithmetic( self, args ):
		arType = args[0]
		if arType == 'add' or arType == 'sub':
			self.add( arType )
		if arType in ['eq', 'gt', 'lt']:
			self.cmp( arType )
		if arType in ['neg', 'not']:
			self.unary( arType )
		if arType in ['and', 'or']:
			self.andOr( arType )

	def compilePush( self, args ):
		segment = args[0]
		value = int(args[1])

		if segment == 'constant':
			self.writeLn('@' + `value`) #set A to the constant value
			self.writeLn('D=A') #put that in D
			self.writeLn('@SP') #set A to SP address
			self.writeLn('A=M') #set A to SP
			self.writeLn('M=D') #set the address of SP to the value of D
			self.writeLn('@SP') #increment SP
			self.writeLn('M=M+1')
		else:
			self.writeLn('@' + self.labels[segment]) #set A to the segment base pointer
			self.writeLn('D=M') #get segment base address value and prep A
			self.writeLn('@' + `value`) #set A to offset
			self.writeLn('D=D+A') #compute address of RAM we want to push
			self.writeLn('A=D') #set A to the RAM address we just made
			self.writeLn('D=M') #set D to the value that that RAM address stores

			self.writeLn('@SP') #set A to SP address
			self.writeLn('A=M') #set A to the SP
			self.writeLn('M=D') #save what is in D to where the SP points at at the moment
			self.writeLn('@SP') #set A to address of SP
			self.writeLn('M=M+1') #increase SP by 1

	def compilePop( self, args ):
		segment = args[0]
		offset = int(args[1])

		#Get top value from stack
		self.writeLn('@SP') # prep A with SP
		self.writeLn('AM=M-1') # set A to *SP
		self.writeLn('D=M') # store the value that SP points to

		#save value to TMP
		self.writeLn('@13')
		self.writeLn('M=D')

		#get location to where we want to POP
		self.writeLn('@' + self.labels[segment])
		if(segment == 'temp'):
			self.writeLn('D=A')
		else:
			self.writeLn('D=M') #Store segment pointer in D
		self.writeLn('@' + `offset`)
		self.writeLn('D=D+A')

		#Swap values with TMP
		self.writeLn('@R14')
		self.writeLn('M=D')

		self.writeLn('@13')
		self.writeLn('D=M')

		self.writeLn('@14')
		self.writeLn('A=M')

		self.writeLn('M=D')

	def printHackLines( self ):
		for l in self.hackLines:
			print l

	def resolveCommand( self, commandType, args ):
		self.compileFunctions[commandType](args);


