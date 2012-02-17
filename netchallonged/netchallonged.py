#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket
import random
import time
import threading
import math
import copy 
import os
import pdb
from cPickle import *

#Custom timer :P
import timer
import scores
import challenge
from user import * #Holding scores and lvl and nick

from prompt import *

try:
	import SocketServer
except:
	import socketserver as SocketServer

#Appending the challenge dir to the module loading path :)
challengeDir = "challenges"
sys.path.append(challengeDir) 
DEBUG = 1

#CONFIGZ
#http://docs.python.org/library/socketserver.html


HOST, PORT = '', 1337

#
#
#	Code::Phun Network challonge. 
#
#

scores = scores.Scores()

def load(chl):
	""" Dynamically loading modules. Returns the module loaded"""
	byteCodeFile = challenge.Challenge.challengeDir + "/" + chl + ".pyc"
	if (os.path.exists(byteCodeFile)):
		print ( "python bytecode exists. Deleting it " )
		try:
			os.remove(byteCodeFile)
		except:
			print ("Could not delete file. please delete manually for a refreshed challenge")
			print ("file: %s" % (byteCodeFile,))
	return __import__(chl, fromlist=[])
	


	


class NerdHandler(SocketServer.StreamRequestHandler):
	"""
		The class invoked when dealing with a nerd.
		
		Each client connecting will get a separate thread running handling them. (this class)
		It is here the communication happens between the server and client. It will ask the server main thread for
		the current challenge active for the user. (@see ThreadedNetChallonged.getChallenge() )Then serve it. 
	
	"""
	def handle(self):
		cur_thread = threading.currentThread()
		print ("%s Joined. Will he or she manage? The clock is ticking." %(self.client_address[0]))
		try:
		
			#Limit of 1 sec
			
			# Getting the nickname the nerd is using 
			nickname=self.ReadSomething()
			print ("******************************** Nerd: %s " % (nickname,))
			lvl = server.addUser(str(nickname))
			# Making a challenge for him /her
 			challengeHandler = server.getChallenge(str(lvl))
			print (challengeHandler.desc())
			
			
			challenge = challengeHandler.challenge()
			
			
			self.SaySomething(challenge)

			
			#Ticking down
			t = timer.Timer(challengeHandler.timeLimit())
			
			nerdAttempt = str(self.ReadSomething())
			
			#Did he make the challenge?
			passed = challengeHandler.passed(nerdAttempt)
			if passed:
				#todo make this a method instead
				server.levelUpUser(str(nickname))

			
			
			#Telling him/her:
			reply = "Correct!\n" if passed and t.timeLeft() else "Wrong or not solved in time :)!\n"
			self.SaySomething(reply)
		
			
			answer = str(challengeHandler.validAnswer())
			
			# http://effbot.org/zone/thread-synchronization.htm
			#Grading him
			
			scores.addResult("%s [%s]" %(nickname, self.client_address[0]), passed)
			
			print ( "The nerd gave an attempt to answer the challonge. \n \
			\t Challenge: \t %s \n \
			. He thought it to be:  %s \n \
			It should be: %s\n \
			, and he is  %s !!!!" % 
				(challenge, nerdAttempt, answer, reply) )
	
		except Exception as e:
			print ( "Man quit! %s" %(e,))
		finally:
			print ( "%s Nerd Gones " % self.client_address[0] )
	
	def SaySomething(self, something):
		""" Method for writing to the socket. 
		Python 3 compability issue handling :) Str is no longar  string or something"""
		self.wfile.write((something).encode('UTF-8')+'\n')
	
	def ReadSomething(self):
		""" Method to read from the socket.
		The comp...  well, it decodes utf-8."""
		return self.rfile.readline(int( math.pow(2,30) )).decode('UTF-8').strip()
		



class ThreadedNetChallonged(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	
	def addChallenge(self, challenge, lvl):
		""" For globally adding a new challenge to the server. lvl overwriting is done by adding a new challenge with an old lvl"""
		try:
			with self.lock:
				self.challenges[lvl] = challenge
		except Exception as e: print (e, "failed")
		
	def getChallenge(self, lvl):
		""" Returns a Challenge object linked with a current lvl"""
		#todo implement a mechanism for when there are no challenges left. 
		try: 
			with self.lock:
				return self.challenges[lvl]
		except Exception as e: print (e, "failed")

	def addUser(self, nickname):
		""" Checks if the user is new, then creates it. If we have the user from before, this method does nothing.
			Returns lvl of the user.
		"""
		try:
			with self.userlock:
				#a.setdefault(k[, x]) does this... wher a is the self.users dictionary.
				if not nickname in self.users:
					self.users[nickname] = User(nickname)
				return self.users[nickname].lvl
		except Exception as e: print (e, "failed")
		
		
		
	def levelUpUser(self, nickname):
		"""	 Leveling up  a user. If the last level is reached, it will still update level, but there will be no challenges to let it further exceed.
			 getChallonge should take account for handling lvls which does not yet change
		 """
		try:
			with self.userlock:
				#a.setdefault(k[, x]) does this... wher a is the self.users dictionary.
				if not nickname in self.users:
					self.users[nickname] = User(nickname)
				self.users[nickname].lvl+=1
		except Exception as e: print (e, "failed")
	
	
	def getUser(self, nickname):
		"""Returns a User object wit nick: nickname"""
		try:
			with self.userlock:
				return self.users[nickname]
		except Exception as e: print (e, "failed")
			
	def listUsers(self):
		"""	Returns a copy of the current userlists  """
		try:
			with self.userlock:
				return copy.copy(self.users)
		except Exception as e: print (e, "failed")
		
	def listChallenges(self):
		"""	Returns a copy of the current userlists  """
		try:
			with self.lock:
				return copy.copy(self.challenges)
		except Exception as e:
			print ("List challenges erroer %s " %(e,))
				
	def saveServerState(self):
		"""	Function to save the state of the server. 
			Users and their levels
			Challenges and their levels
			Scores [not implemented]
		"""
		try:
			with self.stateLock:
				with self.userLock:
					with self.lock:
						#Saving user state
						userFile = open("user.state", "w")
						Pickle.dump(self.users, userFile)
						#Saving Challenge state
						challengeFile = open("challenge.state", "w")
						Pickle.dump(self.challenges, challengeFile)
						#Saving score state
						scoreFile = open("score.state", "w")
						#todo: implement. Move scores under the threaded server object.
						#pickle.dump(self.scores, scoreFile)
						
		except Exception as e:
			print ("Failed to save states.. %s " %(e,))
		finally:
			userFile.close()
			scoreFile.close()
			challengeFile.close()

				
	
	
	def saveServerState(self):
		"""	Function to load a earlier state of the server. 
			Users and their levels
			Challenges and their levels
			Scores [not implemented]
		"""
		try:
			with self.stateLock:
				with self.userlock:
					with self.lock:
						#loading user state
						userFile = open("user.state", "r")
						self.users = pickle.load(userFile)
						#loading challenge state
						challengeFile = open("challenge.state", "r")
						self.challenges = pickle.load(challengeFile)
						#loading score state
						#todo: implement
						scoreFile = open("score.state", "r")
						
						
		except Exception as e:
			print ("Failed to save states.. %s " %(e,))	
		finally:
			userFile.close()
			scoreFile.close()
			challengeFile.close()	
			
	#State objects :)
	challenges = {}
	users = {}
	
	#To make the operations on add / get users / challenges atomic.
	lock = threading.RLock() #challengelock
	userlock = threading.RLock()
	stateLock = threading.RLock()
	
	
	
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
					for k in ["load", "scores", "quit", "help", "users"]:
						print (k)
					print ("Usage help [<command>]  \n if no command given, it lists all commands")
					continue
				
				if "load" in args[1]:
					print("Usage: load <challenge-name> <lvl>")
				
				
			elif "load" in cmd:
				
				#
				#		LOAD SERVER STATE
				#	
				
				if "state" in cmd:
					""" Overwriting the load challenge command to act for load state from state files"""
					print ("Loading server states")
					try:
						server.loadServerState()
					except Exception as e:
						print (" Failed to load states: %s " %(e,))

					continue #skipping over the next steps
				
				#
				#		LOAD Challenge
				#
				
				""" Loads a new challenge module """
				try:
					(name, lvl) = cmd.split(" ")[1:3]
					print ("Loading %s at lvl %s" %(name, lvl))
					
					mod = load(name)
					exec ("challengeObj = mod.%s()" %(name, )) #dirty hack?
					
					#Testing the loaded module
					if not challenge.Challenge.test(challengeObj):
						print ("Not loaded")
						continue
					
					#loading it into the server
					server.addChallenge(challengeObj, lvl)
					
					print ("loaded")
					
				except Exception as e:
					print ("Exception %s" %(e))
					print("Usage: load <challenge-name> <lvl>")
					
					
			elif "scores" in cmd:
				print ( scores.getScores() )
			
			# 
			#		Save Server States
			#	
				
			elif "save" in cmd:
				if "state" in cmd:
					print ("Saving states")
					try:
						server.saveServerState()
					except Exception as e:
						print( "Failed to save server state %s " % (e,))
					#Skipping the next sub comands		
					continue

					
				
			
			elif "users" in cmd:
				print("%s")
				for k,v in server.listUsers().items():
					print ("User: %s has gone to lvl: %s" % (k, v.lvl))
					
			elif "challenges" in cmd:
				print (" Listing challenges ")
				for k,v in server.listChallenges().items():
					print ("Lvl: %s \t Challenge:  %s \n\tExample: %s \n\n" % (k, v.name(), v.example()))
					
	except KeyboardInterrupt:
		print ( "Shuting down, erh up... ")
	finally:
		server.shutdown()
