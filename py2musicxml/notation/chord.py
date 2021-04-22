import copy
from typing import Iterable, Tuple

from py2musicxml.notation import Note
import py2musicxml.log as logger

log = logger.get_logger()


"""TODO:
- Join up Chord and Pitch Class set for easy manipulation and 
identification.
- Redefine constructor for multiple dispatch or multiple arguments
where one can pass notes outside a list for easy use.
"""

class Chord:
    def __init__(self, note_list: Iterable[Note]) -> None:
        """Constructor for Chord object.

        Take a list of note objects and wraps them in a chord object.
        This wrapping does some under-the-hood work to have them work
        functionally together in the Python end of Py2MusicXML. It also
        adds necessary flags to write the xml.

        Args:
        --------

        note_list: List of Note objects

        Returns:
        ---------

        self: A Chord object

        """
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
        self.dur = self.notes[0].dur

        for note in self.notes[1:]:
            note.is_chord_member = True

    def _sort_notes(self, note_list: Iterable[Note]) -> Iterable[Note]:

        """Wrapper Function for Insertion sorting the notes by
        pitch."""

        for idx, note in enumerate(note_list):
            note_list = self._insert_notes(note_list, idx, note)

        return note_list

    def _insert_notes(
        self, note_list: Iterable[Note], idx: int, note: Note
    ) -> Iterable[Note]:
        """Insert helper function for insertion sort

        Args:
        ------

        note_list: Iterable[Note], list of note objects

        idx: int, current index

        note: Note, note to do insertion with

        """
        idx_shift = idx - 1
        while (idx_shift >= 0) and (note_list[idx_shift] > note):
            note_list.insert(idx_shift + 1, note_list.pop(idx_shift))
            idx_shift -= 1
        note_list.insert(idx_shift + 1, note_list.pop(note_list.index(note)))
        return note_list

    def _set_note_durs(self, duration) -> None:
        self.dur = duration
        for note in self.notes:
            note.dur = duration

    def split(self, diff) -> Tuple['__class__', '__class__']:
        old_chord = copy.deepcopy(self)
        new_chord = copy.deepcopy(self)

        old_chord._set_note_durs(self.dur - diff)
        new_chord._set_note_durs(diff)

        return old_chord, new_chord


