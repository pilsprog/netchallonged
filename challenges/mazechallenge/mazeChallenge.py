#!/usr/bin/python
#coding: utf-8
#
#
#	Maze Challenge
#
#	Written by: technocake, FireNeslo, eoma, zeddi, steinbitglis
#	idea: steinbitglis
#
#	Generation based on zeddis (insert name here FireNeslo)
#	
#	changelog:
#	technocake 250212	Made the skeleton for the maze Challenge.
#
######################################

import sys, random, pdb

sys.path.append("../../") #to find challenge.py


class mazeChallenge(  ):
	obstacle='#'

	def generateMaze(self, width, height):
		""" Generates a WxH grid filling it with obstacles """
		self.map = [[self.obstacle]*height for x in xrange(width)]
		self.w, self.h = width, height
	

	def represent(self):
		"""	Gives a textual representation of the maze in its current state	 """
		out = ""
		for y in range(self.h):
			for x in range(self.w):	
				out +=self.map[x][y] 
			out +="\n" 
		return out


	def move(self, p, dir):
		p1 = (p[0] + dir[0] , p[1] + dir[1])
		return [p1[0] if p1[0] < self.w  and p1[0] >= 0 else p[0], p1[1] if p1[1] < self.h and p1[1] >= 0 else p[1]]

	def eat(self, p):
		self.map[ p[0] ][ p[1] ] = ' '

	def snake(self, p0, p1):
		""" Simulates a snake eating itself in a random path from point 0 to point 1 """
		#Direction vectors
		dirs = {	'up'	: [0, -1], 
					'down'	: [0, 1], 
					'right'	: [1, 0], 
					'left'	: [-1, 0]
				}
		delta_x, delta_y = p1[0]-p0[0], p1[1]-p0[1]
		u = [delta_x/abs(delta_x), delta_y/abs(delta_y)] #unit vectors.
		dirs = [[0, u[0]], [u[1], 0]] #direction vector set. Only concisting of the two vectors pointing to the point p1

		p=p0
		while (p != p1):	
			dir = dirs[random.randrange(len(dirs))]
			p=self.move(p, dir)
			self.eat(p)





if __name__ == "__main__":
	
	maze = mazeChallenge()
	maze.generateMaze(50,24)
	maze.snake([0,0], [49,23])
	print(maze.represent())
