import pitchMath
import stepwise, stochasticGrammar
import bangleize
import note
import random
import copy

class noteList:	

	def __init__(self, updownfactor, grammarseed):
		self.updownfactor = updownfactor # decimal from 0 to 1, percentage
							# higher percentange, each repetition of the grammar more likely to go down
							# dictates movement of each repetition of grammar - up or down
		self.grammarseed = grammarseed # seed for the grammar
		self.B = bangleize.bangleize()


	#this works, but I don't know if it's wise to actually adjust the list while it's being read
	#maybe some research
	#also, sometimes finale misreads by a 64th note. Not sure about that.
	def groupList(self, theList):
		currentList = theList
		#for now, assume 4/4 at a factor of 1
		measureFactor = 1
		measureBeats = 4
		currentCount = 0
		for location, item in enumerate(currentList):
			currentCount += item.dur
			if currentCount > measureBeats * measureFactor:
				#print("making copies")
				overflow = currentCount % measureBeats
				currentList[location].dur = currentList[location].dur - overflow
				currentList[location].tieStart = True
				tiedNote = copy.copy(currentList[location])
				tiedNote.dur = overflow
				tiedNote.tieEnd = True
				currentList.insert(location + 1, tiedNote)
				currentCount = 0
			else:
				#print("no change")
				pass
		return currentList

	def getList(self, grammarType, startingOctave, startingNote, generations, startingPitch, rType, rhythm):
		startingList = [note.notePC(startingOctave,startingNote), ]
		
		# swg - stepwise grammar (stochastic stepwise grammar)
		# functions on scale degrees instead of pitches

		grammar = None

		if grammarType is "SWG":
			grammar = stepwise.grammar(self.updownfactor, self.grammarseed, startingPitch)
		elif grammarType is "SG":
			grammar = stochasticGrammar.grammar(self.updownfactor, self.grammarseed)
		else:
			raise Exception('Your grammar is unacceptable.')

		pitches = grammar.makeSystem(startingList, generations)

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
		print("before", noteList)
		noteList = self.groupList(noteList)	
		print("after", noteList)
		return noteList