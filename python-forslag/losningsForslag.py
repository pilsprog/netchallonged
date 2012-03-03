#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
losningsForslag.py

Created by Robin Garen Aaberg on 2011-10-24.
"""

import sys
import codecs
import os
import socket


def main():
	s = socket.socket()
	s.connect(('localhost', 1337))


	print ("Kobler til serveren")
	s.send("Marte og Robin\n")
	mattestykket = s.recv(1024).decode('UTF-8').strip()
	
	print (u'Prøver aa finne en løsning på mattestykket')
	#Må vi finne en måte å løse det på!

	svaret = eval(mattestykket)

	s.send(str(svaret).encode('UTF-8')+"\n")
	print (u"Klarte vi det då?")
	klarteViDet = s.recv(1024).decode('UTF-8').strip()
	
	print (klarteViDet)
	
	s.close()

if __name__ == '__main__':
	main()

