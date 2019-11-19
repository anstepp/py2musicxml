from py2musicxml import Note

class Beat:

    def __init__(self) -> None:
        self.notes = []
        self.tuplet = False
        self.subdivisions = None
        self.multi_beat = False

    def make_beams(self) -> None:
        for note in self.notes[0:-1]:
            note.beam = True    

    def add_note(self, note: Note) -> None:
        self.notes.append(note)
