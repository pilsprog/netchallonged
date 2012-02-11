#!/usr/bin/env python
import sys
import socket
import random
import time
import threading
import math

#Custom timer :P
import timer
import scores
from user import * #Holding scores and lvl and nick

from prompt import *

try:
	import SocketServer
except:
	import socketserver as SocketServer

#Appending the challenge dir to the module loading path :)
challengeDir = "challenges"
sys.path.append(challengeDir) 


#CONFIGZ
#http://docs.python.org/library/socketserver.html


HOST, PORT = '', 1337

#
#
#	Code::Phun Network challonge. 
#
#

scores = scores.Scores()

def load(challenge):
	""" Dynamically loading modules. Returns the module loaded"""
	return __import__(challenge, fromlist=[])
	
def getChallonge():
	""" Simple procedure to produce a random mathematical challenge"""
	A=1337
	B=13*3*7
	operators = ["+", "-", "*", "/"]
	#Selects random numbers and random operator
	a = int( round( random.random() * A ))
	b = int( round( random.random() * B ) )
	oi = int( round( random.random() * ( len( operators ) - 1 ) ) )
	#	Will yield something like: 13+37
	return "%d%s%d" % (a, operators[oi], b)

	


class NerdHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		cur_thread = threading.currentThread()
		print ("%s Joined. Will he or she manage? The clock is ticking." %(self.client_address[0]))
		try:
			#Limit of 1 sec
			t = timer.Timer(1)
			# Getting the nickname the nerd is using 
			nickname=self.ReadSomething()
		
			# Making a challenge for him /her
			
			challenge = getChallonge()
			# We need to know the answer to see if the nerd did it..
			answer = int( eval(challenge) )
			
			self.SaySomething(challenge + "\n")
			# 32bit integer max 
			nerdAttempt = int ( self.ReadSomething() )
			
			#Did he make the challenge?
			passed = answer == nerdAttempt
			
			
			
			#Telling him/her:
			reply = "Correct!\n" if passed and t.timeLeft() else "Wrong or not solved in time :)!\n"
			self.SaySomething(reply)
		
			
		
			# http://effbot.org/zone/thread-synchronization.htm
			#Grading him
			
			scores.addResult("%s [%s]" %(nickname, self.client_address[0]), passed)
			
			print ( "The nerd gave an attempt to answer the challonge. \n \
			\t Challenge: \t %s \n \
			. He thought it to be:  %d \n \
			It should be: %d\n \
			, and he is  %s !!!!" % 
				(challenge, nerdAttempt, answer, reply) )
				
		except Exception as e:
			print ( "Man quit! %s" %(e,))
		finally:
			print ( "%s Nerd Gones " % self.client_address[0] )
	
	def SaySomething(self, something):
		""" Method for writing to the socket. 
		Python 3 compability issue handling :) Str is no longar  string or something"""
		self.wfile.write(something.encode('UTF-8'))
	
	def ReadSomething(self):
		""" Method to read from the socket.
		The comp...  well, it decodes utf-8."""
		return self.rfile.readline(int( math.pow(2,30) )).decode('UTF-8').strip()


class ThreadedNetChallonged(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	challenges = {}
	users = {}
	def addChallenge(self, challenge, lvl):
		""" For globally adding a new challenge to the server. lvl overwriting is done by adding a new challenge with an old lvl"""
		with self.lock:
			self.challenges[lvl] = challenge
		
	def getChallenge(self, lvl):
		""" Returns a Challenge object linked with a current lvl"""
		with self.lock:
			return self.challenges[lvl]

	def addUser(self, nickname):
		""" Checks if the user is new, then creates it. If we have the user from before, this method does nothing."""
		with self.userlock:
			#a.setdefault(k[, x]) does this... wher a is the self.users dictionary.
			if not nickname in self.users:
				self.users[nickname] == User(nickname)
	
	def getUser(self, nickname):
		"""Returns a User object wit nick: nickname"""
		with self.userlock:
			return self.users[nickname]
	
	#To make the operations on add / get users / challenges atomic.
	lock = threading.RLock()
	userlock = threading.RLock()
	
	
# Below are the control and running of the server.
# It is an interactive prompt that controls it.

if __name__ == "__main__":
	server = ThreadedNetChallonged((HOST, PORT), NerdHandler)

	def shutUp():
		print ("Shuting down.. eh, up")
		server.shutdown()
		exit()

	print ( "The Challonge is alive" )
	serveraddr, serverport = server.server_address
	try:
		serverThread = threading.Thread(target=server.serve_forever)
		serverThread.setDaemon(True)
		serverThread.start()
		while 1:
			cmd = prompt("Code::Phun->NetChallongeD>> ")
			if "quit" in cmd:
				shutUp()
				
				
			if "help" in cmd:
				args = cmd.split(" ")
				
				#Lists all cmds
				if len(args) == 1:
					for k in ["load", "scores", "quit", "help"]:
						print (k)
					print ("Usage help [<command>]  \n if no command given, it lists all commands")
					continue
				
				if "load" in args[1]:
					print("Usage: load <challenge-name> <lvl>")
				
				
			elif "load" in cmd:
				""" Loads a new challenge module """
				if 1:
					(name, lvl) = cmd.split(" ")[1:3]
					print ("Loading %s at lvl %s" %(name, lvl))
					
					mod = load(name)
					exec ("task = mod.%s()" %(name, )) #dirty hack?
					
					print (task.desc())
					
					print ("loaded")
					
				#except:
				#	print("Usage: load <challenge-name> <lvl>")
					
					
			elif "scores" in cmd:
				print ( scores.getScores() )
	except KeyboardInterrupt:
		print ( "Shuting down, erh up... ")
	finally:
		server.shutdown()
