# This updates Brian House's bjorklund implementation to python3 and does a few other
# things to it to meet my needs.

import random
from note import *

class bangleize:
	def __init__(self):
		pass
		
	def bjorklund(self,  steps, pulses):
		steps = int(steps)
		pulses = int(pulses)
		if pulses > steps:
			rotate = pulses
			pulses = steps
			steps = rotate    
		pattern = []    
		counts = []
		remainders = []
		divisor = steps - pulses
		remainders.append(pulses)
		level = 0
		while True:
			counts.append(divisor / remainders[level])
			remainders.append(divisor % remainders[level])
			divisor = remainders[level]
			level = level + 1
			if remainders[level] <= 1:
				break
		counts.append(divisor)
	
		def build(level):
			if level == -1:
				pattern.append(0)
			elif level == -2:
				pattern.append(1)         
			else:
				for i in self.frange(0, counts[level], 1):
					build(level - 1)
				if remainders[level] != 0:
					build(level - 2)
	
		build(level)
		i = pattern.index(1)
		pattern = pattern[i:] + pattern[0:i]
		
		theList = list()
		count = 0
		for x in pattern:
			if x is 1 and count is not 0:
				theList.append(count)
				count = 1
			else:
				count += 1
		return theList		
		
	def frange(self, start, stop, step):
		i = start
		while i < stop:
			yield i
			i += step

	def eSpaced(self, theNoteList):
		last = None
		theList = list()
		for item in theNoteList:
			if last is not None:
				theList += self.bjorklund(last, item.duration)
			last = item.duration
		return theList
	
	def euclid(self, u, v):
		tempList = list()
		while v > 0:
			if u%v is not 0 and u//v is not 0:
				tempList.append(u//v)
			u, v = v, u % v	
		return tempList

	def euclidize(self, theNoteList):
		last = None
		theList = list()
		for item in theNoteList:
			if last is not None:
				theList += self.euclid(last, item.duration)
			last = item.duration
		return theList