from rtcmix import *
rtsetparams(44100,2)
load("MMODALBAR")
load("WAVETABLE")
load("STRUM2")
load("MCLAR")

import note
import bangleize
import stochasticGrammar, stepwise
import random

SG = stochasticGrammar.grammar(0.5, random.uniform(0, 1000))
B = bangleize.bangleize()
SWG = stepwise.stepwiseGrammar(0.5, random.uniform(0, 1000))

fourVoices = True
stepwise = True
"""
class playback:
	def __init__(self, factor, type, generations, seed):
		self.factor = factor
		self.type = type
		self.gens = generations
		#hack to make array of maketables for variety
		self.env = maketable("curve", 1000, 0,0,2, 100,1,2, 200,.9,2, 900,.9,2, 1000,0)
		self.B = bangleize.bangleize()
		self.SG = stochasticGrammar.grammar(seed)
		self.SWG = stepwise.stepwiseGrammar(seed)
	
	def makeThings(self, startOctave, startPitch):
		#---- pitch
		pitchStart1 = [note.notePC(startOctave,startPitch), ]
		pitches1 = self.SG.makeSystem(pitchStart1, self.generations)
		#---- rhythm
		rhythmList = list()
		passMe = [random.randint(1, 16) for x in range(0, 100000)]
		for x in passMe:
			rhythmList.append(note.noteRhythm(dur=x)
		rhythms = self.B.bangleize(rhythmList)
		#---- zip
		noteList = list()
		for r, p in zip(rhythms1, pitches1):
			noteList.append(note.note(r,p.makeCmix()))
		return noteList
			
	def playWaves(self, table):
		for item in table:
			duration = item.dur * self.factor
			pitch = item.pitch
			amp = random.uniform(9000, 10000)
			WAVETABLE(start, duration, amp * self.env, pitch, random.random())
			
	def playStrum(self, table):
		for item in table:
			duration = item.dur * self.factor
			amp = random.uniform(5000,7000)
			STRUM2(start, duration, amp, item.pitch, random.random(), duration, random.random())
	
	def playClar(self, table):
		for item in table:
			duration = item.dur * self.factor
			pitch = octpch(item.pitch)
			amp = random.uniform(4000,6000)
			MCLAR(start, duration, amp, pitch, random.random(), 0.125, random.random(), random.random())
	
	def playVibe(self, table):
		for item in table:
			duration = item.dur * self.factor
			amp = random.uniform(4000,6000)
			MMODALBAR(start, duration, amp, cpspch(item.pitch), 0.5, 0.5, 0, random.random())
			
	def playMar(self, table):
		for item in table:
			duration = item.dur * self.factor
			amp = random.uniform(4000, 6000)
			MMODALBAR(start, duration, amp, cpspch(item.pitch), 0.5, 0.5, 1, random.random())
"""			
			
if fourVoices:
	gens = 3
	factor = 8
	amp = 5000
	env = maketable("curve", 1000, 0,0,2, 100,1,2, 200,.9,2, 900,.9,2, 1000,0)
	pitchStart1 = [note.notePC(8,0), ]
	pitches1 = SG.makeSystem(pitchStart1, gens)

	rhythmList1 = list()
	passMe = [random.randint(1, 16) for x in range(0, 100000)]    
	for x in passMe:
		rhythmList1.append(note.noteRhythm(dur=x))
	rhythms1 = B.bangleize(rhythmList1)

	noteList1 = list()
	for r, p in zip(rhythms1, pitches1):
		noteList1.append(note.note(r,p.makeCmix()))
	start = 0
	for item in noteList1:
		duration = item.dur * factor
		MCLAR(start, duration, amp, cpspch(item.pitch), random.random(), 0.125, random.random(), random.random())
		start += duration	
	pitchStart2 = [stochasticGrammar.notePC(8,7), ]
	pitches2 = SG.makeSystem(pitchStart2, gens)

	rhythmList2 = list()
	passMe = [random.randint(1, 16) for x in range(0, 10000)]    
	for x in passMe:
		rhythmList2.append(note.noteRhythm(dur=x))
	rhythms2 = B.bangleize(rhythmList2)

	noteList2 = list()
	for r, p in zip(rhythms2, pitches2):
		noteList2.append(note.note(r,p.makeCmix()))
	start = 0
	for item in noteList2:
		duration = item.dur * factor
		MCLAR(start, duration, amp, cpspch(item.pitch), random.random(), 0.125, random.random(), random.random())
		start += duration

	pitchStart3 = [stochasticGrammar.notePC(9,0), ]
	pitches3 = SG.makeSystem(pitchStart3, gens)

	rhythmList3 = list()
	passMe = [random.randint(1, 16) for x in range(0, 10000)]    
	for x in passMe:
		rhythmList3.append(note.noteRhythm(dur=x))
	rhythms3 = B.bangleize(rhythmList3)

	noteList3 = list()
	for r, p in zip(rhythms3, pitches3):
		noteList3.append(note.note(r,p.makeCmix()))
	start = 0
	for item in noteList3:
		duration = item.dur * factor
		MCLAR(start, duration, amp, cpspch(item.pitch), random.random(), 0.125, random.random(), random.random())
		start += duration	

	pitchStart4 = [stochasticGrammar.notePC(7,10), ]
	pitches4 = SG.makeSystem(pitchStart3, 4)
	rhythmList4 = list()
	passMe = [random.randint(1, 16) for x in range(0, 10000)]    
	for x in passMe:
		rhythmList3.append(note.noteRhythm(dur=x))
	rhythms4 = B.bangleize(rhythmList3)
	
	noteList4 = list()
	for r, p in zip(rhythms4, pitches4):
		noteList3.append(note.note(r,p.makeCmix()))
	start = 0
	for item in noteList4:
		duration = item.dur * factor
		MCLAR(start, duration, amp, cpspch(item.pitch), random.random(), 0.125, random.random(), random.random())
		start += duration		

#--------------------------
if stepwise:
	gens = 8
	factor = 0.125
	amp = 5000
	startingList5 = [note.notePC(6,0), ]
	pitches5 = SWG.makeGrammar(startingList5, gens)

	rhythmList5 = list()
	passMe = [random.randint(1, 16) for x in range(0, 100000)]    
	for x in passMe:
		rhythmList5.append(bangleize.noteRhythm(dur=x))
	rhythms5 = B.bangleize(rhythmList5)

	noteList5 = list()
	for r, p in zip(rhythms5, pitches5):
		noteList5.append(note.note(r,p.makeCmix()))
	
	start = 0
	for item in noteList5:
		duration = item.dur * factor
		MMODALBAR(start, duration, amp, cpspch(item.pitch), 0.5, 0.5, 0, random.random())
		start += duration
	
	startingList6 = [note.notePC(6,7), ]
	pitches6 = SWG.makeGrammar(startingList6, gens)

	rhythmList6 = list()
	passMe = [random.randint(1, 16) for x in range(0, 100000)]    
	for x in passMe:
		rhythmList6.append(bangleize.noteRhythm(dur=x))
	rhythms6 = B.bangleize(rhythmList6)

	noteList6 = list()
	for r, p in zip(rhythms6, pitches6):
		noteList6.append(note.note(r,p.makeCmix()))
	
	start = 0
	print(len(noteList6))
	for item in noteList6:
		duration = item.dur * factor
		STRUM2(start, duration, amp, item.pitch, random.random(), duration, random.random())
		start += duration
	
	startingList7 = [note.notePC(6,4), ]
	pitches7 = SWG.makeGrammar(startingList7, gens)

	rhythmList7 = list()
	passMe = [random.randint(1, 16) for x in range(0, 100000)]    
	for x in passMe:
		rhythmList7.append(bangleize.noteRhythm(dur=x))
	rhythms7 = B.bangleize(rhythmList7)

	noteList7 = list()
	for r, p in zip(rhythms7, pitches7):
		noteList7.append(note.note(r,p.makeCmix()))
	
	start = 0
	print(len(noteList7))
	for item in noteList7:
		duration = item.dur * factor
		MMODALBAR(start, duration, amp, cpspch(item.pitch), 0.5, 0.5, 1, random.random())		
		start += duration