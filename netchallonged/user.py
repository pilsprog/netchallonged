#!/usr/bin/python

class User:
	"""User for storing progress"""
	def __init__(self, nick):
		"""Initing on nickname"""
		self.nick = nick
		self.lvl = 0
		self.score = 0
		
		
if __name__ == "__main__":
	u = User("technocake")
	u.lvl+=1
	print(u.nick, u.lvl, u.score)
	

		
		
	