#!/usr/bin/python
class Challenge:
	"""The generic challenge class. All classes should heritage from this one"""
	def name(self):
		"""name of challenge"""
		pass
	
	def desc(self):
		"""Description of challenge should return a string"""
		pass
	
	def example(self):
		"""Give an example of the challenge problem and an example solution (if applicable)"""
		pass
	
	def challenge(self):
		"""the actual challenge given to the nerd"""
	
	def passed(self,answer):
		"""Boolean function to check if the answer given to the challenge is correct or wrong."""
		pass
	
	def validAnswer(self):
		"""Used in example, and for testing purposes"""
		pass
	

	
	"""server for the challenge"""
	challengeServer = "pompel.komsys.org:1337"
	
	

if __name__ == "__main__":
	print("Dont run me, use me!")
