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
	
	def overflowTest(self, inNote):
		if inNote.pc > 11:
			fixedPC = inNote.pc - 12
			fixedNote = notePC(inNote.octave + 1, fixedPC)
			return fixedNote
		elif inNote.pc < 0:
			fixedPC = inNote.pc + 12
			fixedNote = notePC(inNote.octave - 1, fixedPC)
			return fixedNote
		else:
			return inNote

	def nextGen(self, string):
		newGeneration = list()
		for current in string:
			flip = random.random()
			if flip > self.flipVal:
				newGeneration.append(current)
				newGeneration.append(self.overflowTest(notePC(current.octave, current.pc + self.replacementThree)))
				newGeneration.append(current)
			else:
				newGeneration.append(current)
				newGeneration.append(self.overflowTest(notePC(current.octave, current.pc + self.replacementTwo)))
		return newGeneration

	def makeSystem(self, start, generations):
		lastGen = start
		for i in range(generations):
			currentGen = self.nextGen(lastGen)
			lastGen = currentGen
		return currentGen