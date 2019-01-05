import random
from note import *

class grammar:
	
	def __init__(self, testVal, seed):
		random.seed(seed)
		"""Value for up down"""
		self.flipVal = testVal
		"""Replacement rules"""
		self.replacementThree = 5
		self.replacementTwo = -2

	def nextGen(self, string):
		newGeneration = list()
		for current in string:
			flip = random.random()
			if flip > self.flipVal:
				newGeneration.append(current)
				newGeneration.append(current)
			else:
				newGeneration.append(current)
		return newGeneration

	def makeSystem(self, start, generations):
		lastGen = start
		for i in range(generations):
			currentGen = self.nextGen(lastGen)
			lastGen = currentGen
		return currentGen