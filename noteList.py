import pitchMath
import stepwise, stochasticGrammar
import bangleize
import note
import random

class noteList:
	def __init__(self, test, seed):
		self.test = test
		self.seed = seed
		self.B = bangleize.bangleize()

	def getList(self, type, startingOctave, startingNote, generations, startingPitch, rType, rhythm):
		startingList = [note.notePC(startingOctave,startingNote), ]
		if type is "SWG":
			SWG = stepwise.grammar(self.test, self.seed, startingPitch)
			pitches = SWG.makeSystem(startingList, generations)
		elif type is "SG":
			SG = stochasticGrammar.grammar(self.test, self.seed)
			pitches = SG.makeSystem(startingList, generations)
		elif type is "PF":
			pass	
		rhythmList = list()	
		if isinstance(rhythm, int):	
			passMe = [random.randint(1, rhythm) for x in range(0, 100000)]    
			for x in passMe:
				rhythmList.append(note.noteRhythm(dur=x))
			if rType is "ES":
				rhythms = self.B.eSpaced(rhythm[0], rhythm[1], rhythm[2])
			elif rType is "EU":
				rhythms = self.B.euclidize(rhythmList)
		elif isinstance(rhythm, list):
			for x in rhythm:
				rhythmList.append(note.noteRhythm(dur=x))
			if rType is "ES":
				rhythms = self.B.eSpaced(rhythm[0], rhythm[1], rhythm[2])
			elif rType is "EU":
				rhythms = self.B.euclidize(rhythmList)
		noteList = list()
		for r, p in zip(rhythms, pitches):
			x = note.note(r,p.octave,p.pc)
			x.stepName, x.alter, x.accidental = x.getNoteName(startingPitch)
			noteList.append(x)
		return noteList