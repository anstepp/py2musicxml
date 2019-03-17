from .note import Note
from .notelist import NoteList
from .utils import fix_pitch_overflow


class Pitch:
    octave, pitch_class = None, None

    def __init__(self, octave, pitch_class):
        self.octave, self.pitch_class = fix_pitch_overflow(octave, pitch_class)


class Duration:
    duration = None

    def __init__(self, duration):
        self.duration = duration


# this method can be overloaded with multipledispatch
def make_NoteList(duration_sequence, pitch_sequence):
    notes = [
        Note(d.duration, p.octave, p.pitch_class)
        for d, p in zip(duration_sequence, pitch_sequence)
    ]

    return NoteList(notes)
