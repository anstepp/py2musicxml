from typing import Iterable

from py2musicxml.notation import Note

import py2musicxml.log as logger

log = logger.get_logger()

class Chord:

    def __init__(self, note_list: Iterable[Note]) -> None:
        if all(isinstance(note, Note) for note in note_list):
            if all(note.dur == note_list[0].dur for note in note_list):
                unsorted_notes = note_list
            else:
                raise ValueError("All durations in Chord() must be equal")
        else:
            raise ValueError("Arguments to Chord() must be Notes")

        for idx, note in enumerate(note_list):
            log.debug(f"Note list, idx: {idx}, note {note}")

        self.notes = self._sort_notes(note_list)

        for note in self.notes[1:]:
            note.is_chord_member = True

    def _sort_notes(self, note_list: Iterable[Note]) -> Iterable[Note]:

        for idx, note in enumerate(note_list):
            note_list = self._insert_notes(note_list, idx, note)

        return note_list

    def _insert_notes(self, note_list: Iterable[Note], idx: int, note: Note) -> Iterable[Note]:
        idx_shift = idx - 1
        while (idx_shift >= 0) and (note_list[idx_shift] > note):
            note_list.insert(idx_shift + 1, note_list.pop(idx_shift))
            idx_shift -= 1
        note_list.insert(idx_shift + 1, note_list.pop(note_list.index(note)))
        return note_list


