#!/usr/bin/python

class User:
	"""User for storing progress"""
	def __init__(self, nick):
		"""Initing on nickname"""
		self.nick = nick
		self.lvl = 0
		self.scores = []
		
	def addScore(self, lvl, score):
		nextLvl = lvl + 1
		if self.lvl < nextLvl:
			self.scores += [[] for _ in range(nextLvl - self.lvl)]
		self.lvl = max(nextLvl, self.lvl)
		self.scores[lvl].append(score)

if __name__ == "__main__":
	u = User("technocake")
	u.addScore(0, 0)
	print(u.nick, u.lvl, u.scores)
