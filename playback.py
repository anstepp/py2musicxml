from rtcmix import *
load("MMODALBAR")
load("WAVETABLE")
load("STRUM2")
load("MCLAR")

import note
import bangleize
import stochasticGrammar, stepwise
import random

class playback:
	def __init__(self, factor, type, inst, generations, upDown, seed):
		self.factor = factor
		self.type = type
		self.inst = inst
		self.gens = generations
		#hack to make array of maketables for variety
		self.env = maketable("curve", 1000, 0,0,2, 100,1,2, 200,.9,2, 900,.9,2, 1000,0)
		self.B = bangleize.bangleize()
		self.SG = stochasticGrammar.grammar(upDown, seed)
		self.SWG = stepwise.stepwiseGrammar(upDown, seed)
	
	def makeThings(self, startOctave, startPitch):
		#---- pitch
		if self.type == 0:
			pitchStart = [note.notePC(startOctave,startPitch), ]
			pitches = self.SG.makeSystem(pitchStart, self.gens)
		elif self.type == 1:
			pitchStart = [note.notePC(startOctave,startPitch), ]
			pitches = self.SWG.makeSystem(pitchStart, self.gens)
		#---- rhythm
		rhythmList = list()
		passMe = [random.randint(1, 16) for x in range(0, 100000)]
		for x in passMe:
			rhythmList.append(note.noteRhythm(dur=x))
		rhythms = self.B.bangleize(rhythmList)
		#---- zip
		noteList = list()
		for r, p in zip(rhythms, pitches):
			noteList.append(note.note(r,p.makeCmix()))
		return noteList
			
	def playWaves(self, table):
		start = 0
		for item in table:
			duration = item.dur * self.factor
			pitch = item.pitch
			amp = random.uniform(9000, 10000)
			WAVETABLE(start, duration, amp * self.env, pitch, random.random())
			start += duration
			
	def playStrum(self, table):
		start = 0
		for item in table:
			duration = item.dur * self.factor
			amp = random.uniform(5000,7000)
			STRUM2(start, duration, amp, item.pitch, random.random(), duration, random.random())
			start += duration
			
	def playClar(self, table):
		start = 0
		for item in table:
			duration = item.dur * self.factor
			pitch = cpspch(item.pitch)
			amp = random.uniform(6000,8000)
			MCLAR(start, duration, amp, pitch, random.random(), 0.125, random.random(), random.random())
			start += duration
			
	def playVibe(self, table):
		start = 0
		for item in table:
			duration = item.dur * self.factor
			amp = random.uniform(4000,6000)
			MMODALBAR(start, duration, amp, cpspch(item.pitch), 0.5, 0.5, 0, random.random())
			start += duration
			
	def playMar(self, table):
		start = 0
		for item in table:
			duration = item.dur * self.factor
			amp = random.uniform(4000, 6000)
			MMODALBAR(start, duration, amp, cpspch(item.pitch), 0.5, 0.5, 1, random.random())
			start += duration
			
	def play(self, oct, pc):
		passMe = self.makeThings(oct, pc)
		if self.inst == 1:
			self.playWaves(passMe)
		if self.inst == 2:
			self.playStrum(passMe)
		if self.inst == 3:
			self.playClar(passMe)
		if self.inst == 4:
			self.playVibe(passMe)
		if self.inst == 5:
			self.playMar(passMe)