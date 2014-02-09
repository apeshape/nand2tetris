import io
import sys

#ass = io.open('MaxL.asm', encoding='ascii')
#if(!sys.argv[1]){
#	sys.exit('Usage: assembler.py filename destname');
#}
ass = io.open(sys.argv[1], encoding='ascii')
out = open(sys.argv[2] + '.hack','w')

lines = ass.read().split('\n')

computations = {
				'0'		: '101010',
				'1'		: '111111',
				'-1'	: '111010',
				'D'		: '001100',
				'A'		: '110000',
				'M'		: '110000',
				'!D'	: '001101',
				'!A'	: '110001',
				'!M'	: '110001',
				'-D'	: '001111',
				'-A'	: '110011',
				'-M'	: '110011',
				'D+1'	: '011111',
				'A+1'	: '110111',
				'M+1'	: '110111',
				'D-1'	: '001110',
				'A-1'	: '110010',
				'M-1'	: '110010',
				'D+A'	: '000010',
				'D+M'	: '000010',
				'D-A'	: '010011',
				'D-M'	: '010011',
				'A-D'	: '000111',
				'M-D'	: '000111',
				'D&A'	: '000000',
				'D&M'	: '000000',
				'D|A'	: '010101',
				'D|M'	: '010101'
				}
destinations = {
				'M'		: '001',
				'D'		: '010',
				'MD'	: '011',
				'A'		: '100',
				'AM'	: '101',
				'AD'	: '110',
				'AMD'	: '111'
				}
jumps = {
				'JGT'	: '001',
				'JEQ'	: '010',
				'JGE'	: '011',
				'JLT'	: '100',
				'JNE'	: '101',
				'JLE'	: '110',
				'JMP'	: '111'
				}
instructions = [];

numLines = 0
output = ''

def padbin(val):
	padlen = 16 - len(val)
	padding = ''
	if ( padlen > 0):
		for i in range(padlen):
			padding = padding + '0'

	return padding + val

def getJump(jump):
	if(jump == ''):
		return '000'
	if(jump in jumps):
		return jumps[jump]
	return False

def getDest(dest):
	if(dest == ''):
		return '000'
	if(dest in destinations):
		return destinations[dest]
	return False

def getComp(comp):
	abit = '0'
	if(comp in computations):
		if('M' in comp):
			abit = '1'
		return abit + computations[comp]
	return False

def composeBinary(dest, comp, jump):
	destBits = getDest(dest)
	compBits = getComp(comp)
	jumpBits = getJump(jump)

	if(destBits and compBits and jumpBits):
		return '111' + compBits + destBits + jumpBits
	return False


for line in lines:
	instruction = ''
	instruction_type = 'a'

	dest = ''
	comp = ''
	jump = ''

	if line.startswith('//'):
		continue

	if line.startswith('@'):
		val = int(line[1:])
		instruction = bin(val)[2:]
		instruction = padbin(instruction)

		instructions.append(instruction)
		numLines = numLines + 1
		continue


	if ('=' in line):
		instruction_type = 'c'
		parts = line.split('=')
		dest = parts[0]
		comp = parts[1]
	elif(line in computations):
		instruction_type = 'c'
		dest = None
		comp = line

	if(';' in line):
		if(comp != ''):
			parts = comp.split(';')
		else:
			parts = line.split(';')
		comp = parts[0]
		jump = parts[1]
		print jump
	instruction = composeBinary(dest, comp, jump)
	if(instruction):
		instructions.append(instruction)
	#else:
		#print 'Invalid command at line: ' + str(numLines + 1)



	numLines = numLines + 1

print "num lines: " + str(numLines)
hack = '\n'.join(instructions);
out.writelines(hack)



