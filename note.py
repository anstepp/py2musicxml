from noteRhythm import noteRhythm
from notePC import notePC
from math import ceil

class note(noteRhythm, notePC):
	def __init__(self, r, oct, pc):
		notePC.__init__(self, oct, pc)
		noteRhythm.__init__(self, dur=r)
		self.dur = r
		self.octave = oct
		self.pitch = pc
		#flags for ties
		self.tieStart = False
		self.tieContinue = False
		self.tieEnd = False
		#flags for tuplets
		self.tupletStart = False
		self.tupletContinue = False
		self.tupletEnd = False

	def makeOctavePC(self):
		octave = int(self.pitch)
		floatPC = self.pitch % 1
		pc = int(round(floatPC, 2) * 100)
		return octave, pc