import logging

from typing import Iterable

from py2musicxml.notation import Note

beat_logger = logging.getLogger('Beat').setLevel(logging.INFO)



class Beat:
    def __init__(self, subdivisions: int) -> None:
        """init a Beat"""
        self.notes = []
        self.tuplet = False
        self.subdivisions = subdivisions
        self.multi_beat = False
        self.actual_notes = 0

    def _make_beams(self) -> None:
        """Create Beam flags for consituient notes"""
        for location, note in enumerate(self.notes):
            if location == 0:
                note.beam_start = True
            else:
                note.beam_continue = True

    def add_note(self, note: Note) -> None:
        logging.debug(f"Appending note: {note}")
        self.notes.append(note)
        self._make_beams()

    def extend_beat(self, notes: Iterable[Note]) -> None:
        """Input a list of notes to add to the beat"""
        self.notes.extend(notes)
        self._make_beams()

    #     self._tuplet_test()

    # def _tuplet_test(self):
    #     value = []
    #     for note in self.notes:
    #         value.append(note.dur)
    #     print(value)
    #     value_set = set(value)
    #     if self.subdivisions % 3 == 0:
