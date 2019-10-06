from note import Note

class Beat:

    notes = []
    tuplet = False

    def __init__(self):
        self.make_beams()

    def make_beams(self):
        for note in notes[1:-1]:
            note.beam = True    

    # do I need a warn not to use beat.notes.append()?
    # Should it be overloaded?
    def add_note(self, note):
        notes.append(note)
        self.make_beams()
