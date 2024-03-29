#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#	Network Math challenge - the very first challenge to ever enter the system.
#	In fact, originally the system was built in order to host THIS challenge, and that one only.
#	@author:	technocake
#	10.02.2012
#
import sys
import random
import time
import math
#to be able to load Challenge
sys.path.append("../");

from challenge import *

class mathChallenge(Challenge):
	"""The lvl 1 challenge """
	def name(self):
		return "Network Math Challenge"
	
	def desc(self):
		return """
			Challenge: Make a program that connects to %s using a tcp socket and does the following:

			1. sends your nickname.
			2. receives a math challenge.
			3. Sends the answer to that challeng in less then one second!
			
		""" % (Challenge.challengeServer,)
		
	def example(self):
		return """Example of math challenge: 729*632"""
	
	def challenge(self):
		""" Simple procedure to produce a random mathematical challenge"""
		A=1337
		B=13*3*7
		operators = ["+", "-", "*", "/"]
		#Selects random numbers and random operator
		a = int( round( random.random() * A ))
		b = int( round( random.random() * B ) )
		oi = int( round( random.random() * ( len( operators ) - 1 ) ) )
		#	Will yield something like: 13+37
		self.ChallengeGiven = "%d%s%d" % (a, operators[oi], b)
		return self.ChallengeGiven
		
	def passed(self, answer):
		return int(answer) == int( eval(self.ChallengeGiven) ) 
		
	def validAnswer(self):
		return int ( eval(self.ChallengeGiven))
		
	def timeLimit(self):
		return 1000

if __name__ == "__main__":
	""" Testing"""
	print ("Dont run me. use me")
	o = mathChallenge()
	#New testing method
	Challenge.test(o)
	
	quit()
	
	##below lines are not used anymore.
	
	(n,d,e,c,p,a) = (o.name(), o.desc(), o.example(), o.challenge(), o.passed(o.validAnswer()), o.validAnswer())
	
	print ("""
		Name: %s
		Desc: %s
		example: %s
		challenge: %s
		passed?: %s (answer: %s)
	
	""" % (n,d,e,c,p,a))