import pitchMath
import stepwise, stochasticGrammar
import bangleize
import note
import random

class noteList:
<<<<<<< HEAD
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
=======
	def __init__(self, updownfactor, grammarseed):
		self.updownfactor = updownfactor # decimal from 0 to 1, percentage
							# higher percentange, each repetition of the grammar more likely to go down
							# dictates movement of each repetition of grammar - up or down
		self.grammarseed = grammarseed # seed for the grammar
		self.B = bangleize.bangleize()

	def getList(self, grammarType, startingOctave, startingNote, generations, startingPitch, rType, rhythm):
		startingList = [note.notePC(startingOctave,startingNote), ]
		
		# swg - stepwise grammer (stochastic stepwise grammar)
		# functions on scale degrees instead of pitches

		grammar = None

		if grammarType is "SWG":
			grammar = stepwise.grammar(self.updownfactor, self.grammarseed, startingPitch)
		elif grammarType is "SG":
			grammar = stochasticGrammar.grammar(self.updownfactor, self.grammarseed)
		else:
			raise Exception('Your grammar is unacceptable.')

		pitches = grammar.makeSystem(startingList, generations)


>>>>>>> 01c53147638d5f1eb4f7342e3d44bfe98c556e9c
		rhythmList = list()	
		if isinstance(rhythm, int):	
			passMe = [random.randint(1, rhythm) for x in range(0, 100000)]    
			for x in passMe:
				rhythmList.append(note.noteRhythm(dur=x))
			if rType is "ES":
				rhythms = self.B.eSpaced(rhythmList)
			elif rType is "EU":
				rhythms = self.B.euclidize(rhythmList)
		elif isinstance(rhythm, list):
			for x in rhythm:
				rhythmList.append(note.noteRhythm(dur=x))
			if rType is "ES":
				rhythms = self.B.eSpaced(rhythmList)
			elif rType is "EU":
				rhythms = self.B.euclidize(rhythmList)
		noteList = list()
		for r, p in zip(rhythms, pitches):
			x = note.note(r,p.octave,p.pc)
			x.stepName, x.alter, x.accidental = x.getNoteName(startingPitch)
			noteList.append(x)
		return noteList