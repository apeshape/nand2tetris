import io

arithmetics = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']

class Parser( object ):
	def __init__(self, arg):
		super(Parser, self).__init__()
		self.input = io.open( arg )
		self.lines = self.washInput(self.input.read().split('\n'))
		self.lineCount = len(self.lines)
		self.currentCommand = ''
		self.currentCommandParts = []
		self.atCommand = 0

	def washInput(self, lines):
		res = []
		for line in lines:
			if line.startswith('//') or line.startswith('\n') or line == '':
				continue
			res.append(line)
		return res

	def getInput(self):
		return self.input

	def hasMoreCommands(self):
		return self.atCommand <= self.lineCount - 1

	def advance(self):
		self.currentCommand = self.lines[self.atCommand]
		self.currentCommandParts = self.currentCommand.split(' ')
		self.atCommand = self.atCommand + 1

	def commandType(self):
		c = self.currentCommandParts[0]
		if c in arithmetics:
			return 'C_ARITHMETIC'
		if c == 'push': return 'C_PUSH'
		if c == 'pop': return 'C_POP'

	def arg1(self):
		if self.commandType() == 'C_ARITHMETIC':
			return self.currentCommandParts[0]
		return self.currentCommandParts[1]

	def arg2(self):
		if self.commandType() in ( 'C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL' ):
			return self.currentCommandParts[2]



