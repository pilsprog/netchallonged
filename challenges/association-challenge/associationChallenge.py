#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#	Association rules learning challenge  
#       Figure out the association rules hidden in the data.
#       There should be 3 items that are likly to appear together
#
#	@author:    ljos
# 

import sys
import subprocess

#to be able to load Challenge
sys.path.append("../");

from challenge import *


class associationChallenge(Challenge):
    """The association rules learning challenge"""

    def __init__(self):
        """Starting clojure code which generates the data
        and makes the answer"""
        p = subprocess.Popen('lein run', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.answer = p.stdout.readline().strip()
        self.ChallengeGiven = p.read() 
        
        
        
    def name(self):
        return "Association Challenge"
	
    def desc(self):
        return """
			Challenge: Make a program that learns the association rules hidden in the data. There should 3 items that are a lot more likely to appear together then the rest of them.

			1. Send your nickname.
			2. Recieve 10000 transactions or data-lines
			3. Send the answer back. You have 30 min before a new data set will be generated.
                        
                        The transaction are in the format: (butter pork flour) and are each on their own line.
                        The answer should be sent as a list f.ex.: (jam flour potatoes)
		"""
    
    def example(self):
        return ""
    
    def challenge(self):
        """ Retrieves the data  """
        return self.ChallengeGiven
    
    def passed(self, answer):
        return answer.strip() == self.answer;
    
    def validAnswer(self):
        return """"f.ex.: (cheese soda tomatoes)"""
    
    def timeLimit(self):
        return 1000*60*30
    
    if __name__ == "__main__":
        """ Testing"""
        print ("Testing the associationChallenge")
        import pdb #debug  see http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/
        pdb.set_trace()
        
        backlengsChallenge.challengeDir="."
        o = associationChallenge()
        
	#New testing method
        Challenge.test(o)
        
