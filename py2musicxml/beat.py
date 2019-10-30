from py2musicxml import Note

class Beat:

    tuplet = False
    subdivisions = None

    def __init__(self):
        self.notes = list()

    def make_beams(self):
        for note in self.notes[0:-1]:
            note.beam = True    

    def add_note(self, note: Note):
        self.notes.append(note)
