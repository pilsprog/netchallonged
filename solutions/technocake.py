#!/usr/bin/python
from socket import *

s = socket()
s.connect(("pompel.komsys.org", 1337))
s.send("technocake\n")
ch = s.recv(1024)
s.send(str(eval(ch))+"\n")
pased = s.recv(1024)

print (pased)

