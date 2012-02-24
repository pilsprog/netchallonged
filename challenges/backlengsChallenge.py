#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#	Backlengs challenge  --> flip your letters :)  abba <--> abba and ba <--> ab ;)
#
#	@author:	technocake
#	17.02.2012
#
import sys
import random
import time
import math
#to be able to load Challenge
sys.path.append("../");
import backlengs

from challenge import *


class backlengsChallenge(Challenge):
	"""The backlengs challenge"""

	def __init__(self):
		"""just loading jokes  :)"""
		self.jokes =  open (self.challengeDir + "/yomama.list").readlines()
		
	def name(self):
		return "Backlengs Challenge"
	
	def desc(self):
		return """
			Challenge: Make a program that connects to %s using a tcp socket and does the following:

			1. sends your nickname.
			2. receives a random yo-mama joke, and then flips it backwords. So yo-mama is fat --> taf si amam.oy .
			3. Sends the answer to that challenge in less then %d second!
			
		""" % (Challenge.challengeServer, self.timeLimit()/1000.00)
		
	def example(self):
		return """Example of %s challenge: \n%s\n<-->\n%s <-->"""%(self.name(), self.challenge(),self.validAnswer())
	
	def challenge(self):
		""" Gets a random yomama joke from a big list. """
		
		joke = self.jokes[ int( round (random.random()*len(self.jokes) ))-1 ].strip()
		self.ChallengeGiven = joke
		return self.ChallengeGiven
		
	def passed(self, answer):
		return answer == self.validAnswer()
		
	def validAnswer(self):
		return backlengs.backlengs(self.ChallengeGiven)
		
	def timeLimit(self):
		return 1000

if __name__ == "__main__":
	""" Testing"""
	print ("Testing the backlengsChallenge")
	import pdb #debug  see http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/
	pdb.set_trace()
	
	backlengsChallenge.challengeDir="."
	o = backlengsChallenge()

	#New testing method
	Challenge.test(o)
