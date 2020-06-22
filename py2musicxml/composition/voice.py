"""
Voice is a file that contains classes that represent voices and instruments.

To use one of the voices, you import:

from py2musicxml.composition import [chosen_voice]

The score then has access to creating an instrument:

first_trumpet = Trumpet()

Which you can then call methods that are either generic
or instrument specific. These methods allow for various
prototyping/score production functionality.

All instruments have the following methods. The necessary
arguments are given as well:

To extend pitch values:
Voice.extend_pitches(List[int])

To extend duration values:
Voice.extend_durations(List[int])

To convert pitch and duration values to Note objects:
Voice.make_note_list(int)

To add Note objects to the list of Note objects:
Voice.extend_note_list(List[Note, Rest])

To insert a Rest object of a given duration in the Note object list:
Voice.insert_rest(int: duration, int: index)

To insert a Note object or list of Note objects in the Note object list:
Voice.insert_note_list(List[Note, Rest], int: index)

Convert list of Note objects to a Part object:
Voice.make_part(Time_Signature)

Check range of the instrument:
Voice.check_range()

To clear out the note list:
Voice.clear_list()
"""

from py2musicxml.notation import Note, Rest, Part

from typing import List, Tuple, Iterable, Union

Time_Signature = List[Tuple[int, int]]
Range = List[Tuple[int, int]]
Slice = Tuple[int, int]


class Voice:
    def __init__(self):
        self.pitches = []
        self.durations = []

        self.range = Range

        """Have both a note_list and a part associated with the instrument.
        In the case we have to operate a method belonging to an instrument
        after the measure/beat subdivision algorithm, or if the instrument
        is multiple parts (i.e. piano)"""
        self.part = None
        self.note_list = []

    def extend_pitches(self, input_list: list) -> None:
        self.pitches.extend(input_list)

    def extend_durations(self, input_list: list) -> None:
        self.durations.extend(input_list)

    def make_note_list(self, octave: int) -> None:
        self.note_list = [
            Note(dur, octave, pc) for dur, pc in zip(self.durations, self.pitches)
        ]

    def extend_note_list(self, input_list: Iterable[Union[Note, Rest]]) -> None:
        self.note_list.extend(input_list)

    def insert_rest(self, duration: int, index: int) -> None:
        self.note_list.insert(index, Rest(duration))

    def insert_note_list(self, input_list: Iterable[Union[Note, Rest]], index: int) -> None:
        first_chunk = self.note_list[0:index]
        last_chunk = self.note_list[index:]
        self.note_list = first_chunk + input_list + last_chunk

    def make_part(self, time_signature: Time_Signature) -> Part:
        self.part = Part(self.note_list, time_signature)
        return self.part

    def check_range(self):
        for note in self.note_list:
            if note.octave < self.range[0][0] and note.pc < self.range[0][1]:
                note = Note(note.dur, range[0][0], note.pc)
            elif note.octave > self.range[1][0] and note.pc > self.range[1][1]:
                note.octave = Note(note.dur, range[1][0], note.pc)

    def make_staccato(self, slice_range: Slice) -> None:
        for index, note in enumerate(self.note_list[slice_range[0] : slice_range[1]]):
            if type(note) is not Rest:
                self.note_list[index * 2] = Note(0.25, note.octave, note.pc)
                if index != slice_range[1]:

                    self.note_list.insert(index * 2 + 1, Rest(note.dur - 0.25))

    def clear_list(self):
        self.pitches = []
        self.durations = []
        self.note_list = []


class Flute(Voice):
    def __init__(self):
        super(Flute, self).__init__()
        self.range = [(4, 0), (7, 2)]


class Clarinet(Voice):
    def __init__(self):
        super(Clarinet, self).__init__()
        self.range = [(3, 2), (6, 9)]
        self.chalumeau = [(3, 2), (4, 4)]

    def constrain_to_chalumeau(self, slice_range: Slice) -> None:
        for note in self.note_list[slice_range[0] : slice_range[1]]:
            if note.octave < self.chalumeau[0][0] and note.pc < self.chalumeau[0][1]:
                note = Note(note.dur, range[0][0], note.pc)
            elif note.octave > self.chalumeau[1][0] and note.pc > self.chalumeau[1][1]:
                note = Note(note.dur, range[1][0], note.pc)


class Bassoon(Voice):
    def __init__(self):
        super(Bassoon, self).__init__()
        self.range = [(1, 10), (5, 3)]


class Strings(Voice):
    def __init__(self):
        super(Strings, self).__init__()
        self.open_strings = None

    def bariolage(self, range_to_affect: Slice) -> None:
        pass


class Violin(Strings):
    def __init__(self):
        super(Violin, self).__init__()
        self.range = [(3, 7), (8, 11)]
        self.open_strings = [(3, 7), (4, 2), (4, 9), (5, 4)]


class Cello(Strings):
    def __init__(self):
        super(Cello, self).__init__()
        self.range = [(1, 0), (6, 4)]
        self.open_strings = [(1, 0), (1, 7), (2, 2), (2, 9)]
