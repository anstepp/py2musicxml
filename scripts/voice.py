from py2musicxml import Note, Rest, Part

from typing import List, Tuple, Iterable, Union

Time_Signature = List[Tuple[int, int]]
Range = List[Tuple[int,int]]
Slice = Tuple[int,int]

class Voice:

    def __init__(self):
        self.pitches = []
        self.durations = []
        self.note_list = []
        self.range = Range

    def extend_pitches(self, input_list: list) -> None:
        self.pitches.extend(input_list)

    def extend_durations(self, input_list: list) -> None:
        self.durations.extend(input_list)

    def make_note_list(self, octave: int) -> None:
        self.note_list = [Note(dur, octave, pc) for dur, pc in zip(self.durations, self.pitches)]

    def extend_note_list(self, input_list: Iterable[Union[Note, Rest]]) -> None:
        self.note_list.extend(input_list)

    def insert_rest(self, duration: int, index: int) -> None:
        self.note_list.insert(index, Rest(duration))

    def make_part(self, time_signature: Time_Signature) -> Part:
        return Part(self.note_list, time_signature)

    def check_range(self):
        for note in self.note_list:
            if note.octave < self.range[0][0] and note.pc < self.range[0][1]:
                note = Note(note.dur, range[0][0], note.pc)
            elif note.octave > self.range[1][0] and note.pc > self.range[1][1]:
                note.octave = Note(note.dur, range[1][0], note.pc)

    def make_staccato(self, slice_range: Slice) -> None:
        for index, note in enumerate(self.note_list[slice_range[0]:slice_range[1]]):
            if type(note) is not Rest:
                self.note_list[index * 2] = Note(note.dur * 0.25, note.octave, note.pc)
                self.note_list.insert(index * 2 + 1, Rest(note.dur * 0.75))

class Flute(Voice):

    def __init__(self):
        super(Flute, self).__init__()
        self.range = [(4,0), (7,2)]


class Clarinet(Voice):

    def __init__(self):
        super(Clarinet, self).__init__()
        self.range = [(3,2), (6,9)]
        self.chalumeau = [(3,2), (4,4)]

    def constrain_to_chalumeau(self, slice_range: Slice) -> None:
        for note in self.note_list[slice_range[0]:slice_range[1]]:
            if note.octave < self.chalumeau[0][0] and note.pc < self.chalumeau[0][1]:
                note = Note(note.dur, range[0][0], note.pc)
            elif note.octave > self.chalumeau[1][0] and note.pc > self.chalumeau[1][1]:
                note = Note(note.dur, range[1][0], note.pc)

class Bassoon(Voice):

    def __init__(self):
        super(Bassoon, self).__init__()
        self.range = [(1, 10), (5,3)]
