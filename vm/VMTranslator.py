#! /usr/bin/python

import sys
import os

from translator import parser
from translator import codeWriter

f = sys.argv[1]
try:
	filenames = os.listdir(f)
except OSError:
	filenames = [f]

writer = codeWriter.CodeWriter( f + '.asm' )

for fname in filenames:
	p = parser.Parser(f)

	while p.hasMoreCommands():
		p.advance()
		args = [p.arg1()]
		if p.arg2() :
			args.append(p.arg2())

		writer.resolveCommand(p.commandType(), args)

	writer.printHackLines()
		# print p.commandType()
