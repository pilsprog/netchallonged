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
from prompt import *

try:
	import SocketServer
except:
	import socketserver as SocketServer


#CONFIGZ
#http://docs.python.org/library/socketserver.html


HOST, PORT = '', 1337

#
#
#	Code::Phun Network challonge. 
#
#

scores = scores.Scores()


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
			# Getting the language the nerd is using 
			language=self.ReadSomething()
		
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
			
			scores.addResult("%s [%s]" %(language, self.client_address[0]), passed)
			
			print ( "The nerd gave an attempt to answer the challonge. \n \
			\t Challenge: \t %s \n \
			. He thought it to be:  %d \n \
			It should be: %d\n \
			, and he is  %s !!!!" % 
				(challenge, nerdAttempt, answer, reply) )
				
		except Exception as e:
			print ( "Man quit! %s" %(e,))
		finally:
			print ( "%s Nerd Lost:/ " % self.client_address[0] )
	
	def SaySomething(self, something):
		""" Method for writing to the socket. 
		Python 3 compability issue handling :) Str is no longar  string or something"""
		self.wfile.write(something.encode('UTF-8'))
	
	def ReadSomething(self):
		""" Method to read from the socket.
		The comp...  well, it decodes utf-8."""
		return self.rfile.readline(int( math.pow(2,30) )).decode('UTF-8').strip()


class ThreadedNetChallonged(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

	
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
			elif "scores" in cmd:
				print ( scores.getScores() )
	except KeyboardInterrupt:
		print ( "Shuting down, erh up... ")
	finally:
		server.shutdown()
