#!/usr/bin/python
import sys
def backlengs(ord):
	if len(ord) <= 1:
		return ord
	return ord[-1] + backlengs(ord[1:-1]) + ord[0]
if __name__ == "__main__":
	print (backlengs("hei"))
	while 1:
		ord = sys.stdin.readline()[:-1]
		sys.stdout.write( ord + " <-> " +backlengs(ord) + "\n")
