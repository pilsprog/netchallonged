#!/usr/bin/python
""" not really a uml parser. It simply strips lines from stdin NOT containing def or class."""

#
#	@author: technocake
#	@desc: Simple line parser to extract classes and their functions from a python source file.
#	
#	Usage:	cat <source-file> | ./uml-lvl1-parser.py
#	Pipe a source file into the input of uml-lvl1-parser.py
#

import sys


source = sys.stdin

for line in source:
	if "class " in line:
		print ( line )
	if "def " in line:
		print ( "\t%s" % (line) )
