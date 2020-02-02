from .note import Note


class Beat:
    def __init__(self, subdivisions: int) -> None:
        self.notes = []
        self.tuplet = False
        self.subdivisions = subdivisions
        self.multi_beat = False
        self.actual_notes = 0

    def _make_beams(self) -> None:
        for location, note in enumerate(self.notes):
            if location == 0:
                note.beam_start = True
            else:
                note.beam_continue = True

    def add_note(self, note: Note) -> None:
        self.notes.append(note)
        self._make_beams()

    #     self._tuplet_test()

    # def _tuplet_test(self):
    #     value = []
    #     for note in self.notes:
    #         value.append(note.dur)
    #     print(value)
    #     value_set = set(value)
    #     if self.subdivisions % 3 == 0:
