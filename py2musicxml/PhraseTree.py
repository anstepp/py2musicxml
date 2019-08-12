import Tree

class PhraseTree(Tree):

	def __init__(self, notelist):
		val = 0
		nodelist = [val += x for note.dur in notelist if self.tieTest(note)]

	def tieTest(self, note):
		if note.TieContinue is False and note.TieEnd is False:
			return True
		else:
			return False

