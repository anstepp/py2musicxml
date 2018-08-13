from noteRhythm import noteRhythm
from notePC import notePC
from math import ceil

# the life of a note

# in a tuplet, we change the subdivision of the beat
# groups of 3 in the space of 2
# grouping of notes other than the subdivision of the meter
	# it has to change in the subdivsion, feel of music changes
	# how is this unit of time divided, and then subdivided

	# when beat is divided by 2, subdivisions are in groups of 2 - simple time
	# by 3, compound
	# 4 is outgrowth of 2, can be reduced into 2
	# 


	# pc - pitch class


class note(noteRhythm, notePC):
	duration = None
	octave = None
	pitch = None

	# flags for ties
	tieStart = False
	tieContinue = False
	tieEnd = False
	
	# flags for tuplets
	tupletStart = False
	tupletContinue = False
	tupletEnd = False

	def __init__(self, duration, octave, pitch):
		
		notePC.__init__(self, octave, pitch)
		
		noteRhythm.__init__(self, dur=duration)
		
		self.duration = duration
		self.octave = octave
		self.pitch = pitch
		

	def makeOctavePC(self):
		octave = int(self.pitch)
		floatPC = self.pitch % 1
		pc = int(round(floatPC, 2) * 100)
		return octave, pc