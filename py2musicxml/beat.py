from py2musicxml import Note

class Beat:

    notes = list()
    tuplet = False
    subdivisions = None

    def __init__(self):
        pass

    def _make_beams(self):
        for note in self.notes[0:-1]:
            note.beam = True    

    def add_note(self, note: Note):
        self.notes.append(note)
        self._make_beams()
