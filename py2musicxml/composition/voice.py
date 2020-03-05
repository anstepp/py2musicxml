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
        self.note_list = []

    def _transpose(self, input_list: Iterable[Union[Note, Rest]], interval: int) -> None:

        temp_list = []

        for note in input_list:
            if isinstance(note, Note):
                temp_list.append(Note(note.dur, note.octave, note.pc + 2))
            else:
                append(note)

        return temp_list

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

    def make_part(self, time_signature: Time_Signature) -> Part:
        checked_list = self._check_range(self.note_list)
        part = Part(checked_list, time_signature)
        return [part]

    def _check_range(self, note_list: Iterable[Union[Note, Rest]]):
        temp_list = []
        for note in note_list:
            if isinstance(note, Note):
                if note.octave == self.range[0][0]:
                    if note.pc >= self.range[0][1]:
                        temp_list.append(note)
                    else:
                        temp_note = Note(note.dur, self.range[0][0], note.pc)
                        temp_list.append(temp_note)
                elif note.octave < self.range[0][0]:
                    temp_note = Note(note.dur, self.range[0][0], note.pc)
                    temp_list.append(temp_note)
                elif note.octave == self.range[1][0]:
                    if note.pc <= self.range[1][1]:
                        temp_list.append(note)
                    else:
                        temp_note = Note(note.dur, self.range[1][0], note.pc)
                        temp_list.append(temp_note)
                elif note.octave > self.range[1][0]:
                    temp_note = Note(note.dur, self.range[1][0], note.pc)
                    temp_list.append(temp_note)                   
                else:
                    temp_list.append(note)
            else:
                temp_list.append(note)
        return temp_list

    def make_staccato(self, slice_range=None) -> None:
        if slice_range:
            for note in self.note_list:
                if isinstance(note, Note):
                    temp_list.append(Note(0.25, note.octave, note.pc))
                    temp_list.append(Rest(note.dur - 0.25))
        else:
            temp_list = []
            for note in self.note_list:
                if isinstance(note, Note):
                    temp_list.append(Note(0.25, note.octave, note.pc))
                    temp_list.append(Rest(note.dur - 0.25))
        self.note_list = temp_list

    def clear_list(self):
        self.pitches = []
        self.durations = []
        self.note_list = []

    def set_note_list(self, input_list: Iterable[Union[Note, Rest]]) -> None:
        self.note_list = input_list

    def constrain_range(self, temp_range: Range):
        for note in self.note_list:
            if isinstance(note, Note):
                if note.octave < temp_range[0][0] and note.pc < temp_range[0][1]:
                    print("out of range, correcting up")
                    note = Note(note.dur, temp_range[0][0], note.pc)
                elif note.octave > temp_range[1][0] and note.pc > temp_range[1][1]:
                    print("out of range, correcting down")
                    note.octave = Note(note.dur, temp_range[1][0], note.pc)

class Flute(Voice):
    def __init__(self):
        super(Flute, self).__init__()
        self.range = [(4, 0), (7, 2)]


class Clarinet(Voice):
    def __init__(self):
        super(Clarinet, self).__init__()
        self.range = [(3, 4), (6, 9)]
        self.chalumeau = [(3, 4), (4, 4)]


    def make_part(self, time_signature: Time_Signature) -> Part:
        checked_list = self._check_range(self.note_list)
        transposed_list = self._transpose(checked_list, 2)
        part = Part(transposed_list, time_signature)
        return [part]

    def constrain_to_chalumeau(self) -> None:
        for note in self.note_list[slice_range[0] : slice_range[1]]:
            if isinstance(note, Note):
                if note.octave < self.chalumeau[0][0] and note.pc < self.chalumeau[0][1]:
                    print("out of range, correcting up")
                    note = Note(note.dur, self.chalumeau[0][0], note.pc)
                elif note.octave > self.chalumeau[1][0] and note.pc > self.chalumeau[1][1]:
                    print("out of range, correcting down")
                    note = Note(note.dur, self.chalumeau[1][0], note.pc)


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


class Piano(Voice):
    def __init__(self):
        super(Piano, self).__init__()
        self.range = [(0, 9), (8, 0)]

    def make_part(self, time_signature: Time_Signature) -> Iterable[Part]:

        """divide notelist into two lists, divided by middle c"""

        note_list_bottom = []
        note_list_top = []

        for note in self.note_list:
            if isinstance(note, Note):
                if note.octave >= 4:
                    note_list_top.append(note)
                    note_list_bottom.append(Rest(note.dur))

                elif note.octave < 4:
                    note_list_bottom.append(note)
                    note_list_top.append(Rest(note.dur))

                else:
                    print('!!!!!!!!ERROR!!!!!!!!!!!')

            elif isinstance(note, Rest):
                note_list_top.append(note)
                note_list_bottom.append(note)

            else:
                print("!!!!!!!ERROR!!!!!!!!!")

        self.bottom = Part(note_list_bottom, time_signature)
        self.top = Part(note_list_top, time_signature)

        """keep parts in score order"""
        self.part = [self.top, self.bottom]
        return self.part     
