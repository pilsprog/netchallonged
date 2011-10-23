#!/usr/bin/env python
import sys
import socket
import random
import time
import threading
import math
#Custom timer :P
import timer

try:
	import SocketServer
except:
	import socketserver as SocketServer

from prompt import *
#CONFIGZ
#http://docs.python.org/library/socketserver.html


HOST, PORT = '', 1337

#
#
#	Code::Phun Network challonge. 
#
#

def getChallonge():
	""" Simple procedure to produce a random mathematical challenge"""
	A=1337
	B=13*3*7
	operators = ["+", "-", "*", "/"]
	#Selects random numbers and random operator
	ai = int( round( random.random() * A ))
	bi = int( round( random.random() * B ) )
	oi = int( round( random.random() * ( len( operators ) - 1 ) ) )
	#	Will yield something like: 13+37
	return "%d%s%d" % (ai, operators[oi], bi)

	


class NerdHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		cur_thread = threading.currentThread()
		print ("%s Joined. Will he or she manage? The clock is ticking." %(self.client_address[0]))
		try:
			#Limit of 1 sec
			t = timer.Timer(1)
			# Getting the language the nerd is using 
			language=self.rfile.readline().strip()
		
			# Making a challenge for him /her
			challenge = getChallonge()
			# We need to know the answer to see if the nerd did it..
			answer = int( eval(challenge) )
			
			self.SaySomething(challenge + "\n")
			# 32bit integer max 
			nerdAttempt = int ( self.rfile.readline( int( math.pow(2,30) ) ).strip() )
			
			#Did he make the challenge?
			passed = answer == nerdAttempt
			
			#Telling him/her:
			reply = "Correct!\n" if passed and t.timeLeft() else "Wrong!\n"
			self.SaySomething(reply)
		
			# http://effbot.org/zone/thread-synchronization.htm
		
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
		""" Python 3 compability issue handling :) Str is no longar  string or something"""
		self.wfile.write(bytes(something, 'UTF-8'))

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
			if "quit" in prompt("Code::Phun->NetChallongeD>> "):
				shutUp()
	except KeyboardInterrupt:
		print ( "Shuting down, erh up... ")
	finally:
		server.shutdown()
