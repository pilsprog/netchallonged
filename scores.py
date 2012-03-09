#!/usr/bin/env python
# encoding: utf-8
"""
scores.py

Created by Robin Garen Aaberg on 2011-10-24.
"""

import sys
import os
from threading import Lock

class Scores:
	"""
	Scores is the datastructure holding the scores for the challonge
	inter-threadedly!
	"""
	scores = {}
	wins = 0
	losses = 0
	
	lock = Lock()

	def addResult(self, id, result):
		"""(id[ip], result[bool]) --> scores"""
		try:
			self.lock.acquire()
			
			self.scores[id] = result
			self.wins += 1 if result else 0
			self.losses += 1 if not result else 0
		except Exception as e:
			print ( e )
		finally:
			self.lock.release()
			
	def getScores(self):
		"""docstring for getScores"""
		try:
			self.lock.acquire()
			niftyString = "Wins: %s - Loss: %s" % (self.wins, self.losses)
		finally:
			self.lock.release()
		return niftyString

def main():
	s = Scores()
	s.addResult('193.158.393.2', True)
	print( s.getScores() )

if __name__ == '__main__':
	main()

