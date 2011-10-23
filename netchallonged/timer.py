import time
class Timer():
	""" A wrapper class for making the world simplest stopwatch / countdown"""
	def __init__(self, limit=-1):
		""" For use as a stop watch"""
		self.start = time.time()
		self.limit = limit
	
#	def __init__(self, limit):
#		""" For use as a countdown """
#		self()
		
	
	def stop(self):
		""" Stopping the whatch"""
		self.stop = time.time()
		self.timePassed = self.stop-self.start
	
	def calcTimePassed(self):
		self.timePassed = ( time.time() - self.start )
		
	def timeLeft(self):
		""" returns bool  <--  Limit passed? """
		self.calcTimePassed()
		return self.timePassed <= self.limit
		

if __name__ == "__main__":
	
	timer = Timer(2000)
	time.sleep(3)
	print (timer.timeLeft())