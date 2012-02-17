#!/usr/bin/python
#lvl 2
import sys

try:
	HOST = sys.argv[1]
except:
	HOST = 'pompel.komsys.org' 
	

def backlengs(ord):
	if len(ord) <= 1:
		return ord
	return ord[-1] + backlengs(ord[1:-1]) + ord[0]


from socket import *
print ("connecting")
s = socket()
s.connect((HOST, 1337))
s.send("technocake\n") 
print("sent nick")
ch = s.recv(1024).strip()
print ("got challenge %s " %(ch,))
ch2 = ch.decode('utf-8')


s.send(backlengs(ch)+"\n")
for i in range(len(ch)): print("%s:%s"% (ord(ch[i]), ord(ch2[i])))
pased = s.recv(1024)
        
print (pased)   
