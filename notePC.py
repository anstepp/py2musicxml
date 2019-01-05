class notePC:
	def __init__(self, octave, pc):
		self.octave = octave
		self.pc = pc
		self.stepName, self.alter, self.accidental = self.getNoteName(0)

	"""turn into oct.pc format for rtcmix"""
	def makeCmix(self):
		decimal = self.pc / 100.0
		makeNote = self.octave + decimal
		return makeNote
		
	def getNoteName(self, startingPitch):
		flatKeys = [1, 3, 5, 8, 10]
		sharpKeys = [2, 4, 6, 7, 9, 11]
		if startingPitch is 0:		
			if self.pc == 0:
				return ["C", None, None]
			elif self.pc == 1:
				return ["C", "1", "sharp"]
			elif self.pc == 2:
				return ["D", None, None]
			elif self.pc == 3:
				return ["E", "-1", "flat"]
			elif self.pc == 4:
				return ["E", None, None]
			elif self.pc == 5:
				return ["F", None, None]
			elif self.pc == 6:
				return ["F", "1", "sharp"]
			elif self.pc == 7:
				return ["G", None, None]
			elif self.pc == 8:
				return ["A", "-1", "flat"]
			elif self.pc == 9:
				return ["A", None, None]
			elif self.pc == 10:
				return ["B", "-1", "flat"]
			elif self.pc == 11:
				return ["B", None, None]
			else:
				print("Note out of bounds - this could be a problem.", self.pc)
				return [None, None, None]
		if startingPitch in flatKeys:
			if self.pc == 0:
				return ["C", None, None]
			elif self.pc == 1:
				return ["D", "-1", "flat"]
			elif self.pc == 2:
				return ["D", None, None]
			elif self.pc == 3:
				return ["E", "-1", "flat"]
			elif self.pc == 4:
				return ["E", None, None]
			elif self.pc == 5:
				return ["F", None, None]
			elif self.pc == 6:
				return ["G", "-1", "flat"]
			elif self.pc == 7:
				return ["G", None, None]
			elif self.pc == 8:
				return ["A", "-1", "flat"]
			elif self.pc == 9:
				return ["A", None, None]
			elif self.pc == 10:
				return ["B", "-1", "flat"]
			elif self.pc == 11:
				return ["B", None, None]
			else:
				print("Note out of bounds - this could be a problem.")
				return [None, None, None]
		if startingPitch in sharpKeys:
			if self.pc == 0:
				return ["C", None, None]
			elif self.pc == 1:
				return ["C", "1", "sharp"]
			elif self.pc == 2:
				return ["D", None, None]
			elif self.pc == 3:
				return ["D", "1", "sharp"]
			elif self.pc == 4:
				return ["E", None, None]
			elif self.pc == 5:
				return ["F", None, None]
			elif self.pc == 6:
				return ["F", "1", "sharp"]
			elif self.pc == 7:
				return ["G", None, None]
			elif self.pc == 8:
				return ["G", "1", "sharp"]
			elif self.pc == 9:
				return ["A", None, None]
			elif self.pc == 10:
				return ["A", "1", "sharp"]
			elif self.pc == 11:
				return ["B", None, None]
			else:
				print("Note out of bounds - this could be a problem.")
				return [None, None, None]