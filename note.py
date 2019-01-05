from noteRhythm import noteRhythm
from notePC import notePC
from math import ceil

class note(noteRhythm, notePC):
	def __init__(self, r, octave, pc):
		notePC.__init__(self, octave, pc)
		noteRhythm.__init__(self, dur=r)
		self.dur = r
		self.octave = octave
		self.pitch = pc
		#flags for ties
		self.tieStart = False
		self.tieContinue = False
		self.tieEnd = False
		#flags for tuplets
		self.tupletStart = False
		self.tupletContinue = False
		self.tupletEnd = False
		self.overflowTest()

	def overflowTest(self):
		if self.pc > 11:
			self.pc = self.pc - 12
			self.octave = self.octave + 1
		elif self.pc < 0:
			self.pc = self.pc + 12
			self.octave = self.octave - 1
		else:
			pass

	def makeOctavePC(self):
		octave = int(self.pitch)
		floatPC = self.pitch % 1
		pc = int(round(floatPC, 2) * 100)
		return octave, pc