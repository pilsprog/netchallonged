#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#	noChallenge - dummy challenge called when user has reached the final level
#	@author:	eoma
#	17.02.2012
#
import sys
import random
import time
import math
#to be able to load Challenge
sys.path.append("../");

from challenge import *

class noChallenge(Challenge):
	#calledByValidAnswer = False

	"""The unrecognized lvl challenge """
	def name(self):
		return "Unrecognized Level Challenge"
	
	def desc(self):
		return """
			Challenge: This challenge either means no challenges are loaded or
			you've mastered all the challenges. ;)
		"""
		
	def example(self):
		return """No relevant challenge"""
	
	def challenge(self):
		return "You've reached the current latest level. There will be more in the future. No need to compute something :) (Just submit empty/whatever string)"
		
	def passed(self, answer):
		if self.calledByValidAnswer:
			self.calledByValidAnswer = False
			return True
		else:
			return False
		
	def validAnswer(self):
		self.calledByValidAnswer = True
		return False
		
	def timeLimit(self):
		return 1000

if __name__ == "__main__":
	""" Testing"""
	#import pdb #debug  see http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/
	#pdb.set_trace()

	print ("Dont run me. use me")
	o = noChallenge()
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
