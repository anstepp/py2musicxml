from py2musicxml import Note
from py2musicxml import Beat

import copy
from typing import Union, Iterable

class Measure():
    index = None
    beats = []
    weight = None
    #divisions is self.subdivisions of the quarter note
    divisions = None 
    #self.subdivisions is the musical
    subdivisions = 1
    time_signature = tuple()
    notes = list()
    equal_divisions = True

    def __init__(self, time_signature: tuple):
        self.time_signature = time_signature

    def add_note(self, note: Note):
        beat = Beat()
        beat.add_note(note)
        self.beats.append(beat)

    def gcd(self, a: Union[int, float], b: Union[int, float]):
        if type(a) and type(b) is int:
            while b:
                a, b = b, a % b
            return a
        else:
            # convert float to fraction by approximating denominator then gcd
            return fractions.gcd(
                fractions.Fraction(a).limit_denominator(),
                fractions.Fraction(b).limit_denominator(),
            )

    def lcm(self, a: int, b: int):
        return a * b // self.gcd(a, b)

    def get_divisions(self):
        self.divisions = reduce(self.lcm, self.notes.dur)

    def divide_measure(self):
        if self.equal_divisions:
            if self.time_signature[1] % 3 is 0:
                how_many_beats = self.time_signature[0] / 3
                measure_map = [1 for x in range(how_many_beats)]
            elif self.time_signature[1] % 2 == 0:
                how_many_beats = self.time_signature[0]
                measure_map = [1 for x in range(how_many_beats)]
            else:
                """the user has asked for even spacing in a
                situation where the music can't be. Use the
                bjorklund algorithm to divide the beats up"""
                measure_map = bjorklund()
        return measure_map

    def bjorklund(self):
        unspacedList = unspacedList
        returnList = []
        remainder = len(unspacedList)

        for x in range(0, size):
            if x < attacks:
                returnList.append([1])
            else:
                returnList.append([0])
        minimumLength = 0
        listCounter = 0
        tempList = returnList
        while remainder > 1:
            listCounter = 0
            if minimumLength is 0:
                for currentSeries in returnList:
                    if currentSeries[0] is 0 and listCounter < attacks:
                        tempList[listCounter] += currentSeries
                        tempList[tempList.index(currentSeries)] = []
                        listCounter += 1
            else:
                for item in returnList:
                    if len(item) is minimumLength:
                        if len(item) is minimumLength:
                            tempList[listCounter] += item
                            tempList[tempList.index(item)] = []
                            listCounter += 1
            tempList = [x for x in tempList if x != []]
            returnList = tempList
            listCounter = 0
            remainderList = [len(x) for x in returnList]
            minimumLength = min(remainderList)
            counter = 0
            remainderCount = [counter + 1 for x in remainderList if x is min(remainderList)]
            remainder = len(remainderList)
        return returnList[0]

    def subdivide_measure(self):
        for note in self.notes:
            new_beat = Beat()
            self.beats.append(new_beat.add_note(note))
        # measure_map = self.divide_measure()
        # self.beats = list()
        # current_beat = Beat()
        # current_count = 0
        # current_beat_count = 0
        # subdivisions = measure_map[current_beat_count]
        # current_list = self.notes
        # for location, item in enumerate(current_list):
        #     current_count += item.dur
        #     current_count_floor = current_count // subdivisions
        #     current_count_mod = current_count % subdivisions
        #     if current_count_mod == 0 and current_count_floor == 1:
        #         #print("zero, equal")
        #         if location != len(current_list) - 1:
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #         if item.dur > subdivisions:
        #             how_many_measures = current_count // subdivisions
        #             what_goes_to_the_first_measure = (
        #                 item.dur - current_count // subdivisions
        #             )
        #             last_note_of_old_measure = copy.deepcopy(current_list[location])
        #             last_note_of_old_measure.dur = what_goes_to_the_first_measure
        #             last_note_of_old_measure.tie_start = True
        #             current_beat.add_note(last_note_of_old_measure)
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #             while how_many_measures > 0:
        #                 whole_measure_note = copy.deepcopy(current_list[location])
        #                 whole_measure_note.dur = subdivisions
        #                 if how_many_measures > 1:
        #                     whole_measure_note.tie_start = True
        #                 else:
        #                     whole_measure_note.tie_end = True
        #                 current_beat.add_note(whole_measure_note)
        #                 self.beats.append(current_beat)
        #                 current_beat = Beat()
        #                 subdivisions = measure_map[current_beat_count]
        #                 how_many_measures -= 1
        #         else:
        #             altered_duration = copy.deepcopy(current_list[location])
        #             current_beat.add_note(altered_duration)
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #         current_count = 0
        #     elif current_count_mod == 0 and current_count_floor > 1:
        #         #print("zero, greater than")
        #         how_many_measures = current_count // subdivisions
        #         if location != len(current_list) - 1:
        #             current_list[location + 1].measure_flag = True
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #         how_many_measures = current_count // subdivisions - 1
        #         what_goes_to_the_first_measure = (
        #             item.dur - subdivisions * how_many_measures
        #         )
        #         last_note_of_old_measure = copy.deepcopy(current_list[location])
        #         last_note_of_old_measure.dur = what_goes_to_the_first_measure
        #         last_note_of_old_measure.tie_start = True
        #         current_beat.add_note(last_note_of_old_measure)
        #         while how_many_measures > 0:
        #             note_to_add = copy.deepcopy(current_list[location])
        #             note_to_add.dur = subdivisions
        #             note_to_add.measure_flag = True
        #             current_beat.add_note(note_to_add)
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #             how_many_measures -= 1
        #         lastcurrent_count = current_count_mod
        #         current_count = 0
        #     elif current_count_mod > 0 and current_count_floor == 1:
        #         #print("greater than, zero")
        #         current_note = copy.deepcopy(current_list[location])
        #         overflow = current_count - subdivisions
        #         if overflow // subdivisions > 1:
        #             newDur = subdivisions
        #             current_note.dur = newDur
        #             current_note.tie_start = True
        #             current_beat.add_note(current_note)
        #             tied_note = copy.deepcopy(current_list[location])
        #             tied_dur = overflow % subdivisions
        #             tied_note.dur = newDur
        #             tied_note.tie_end = True
        #             tied_note.measure_flag = True
        #             current_beat.add_note(tied_note)
        #         else:
        #             pre_tie = current_list[location].dur - overflow
        #             current_note.dur = pre_tie
        #             current_note.tie_start = True
        #             current_beat.add_note(current_note)
        #             tied_note = copy.deepcopy(current_list[location])
        #             tied_dur = overflow % subdivisions
        #             tied_note.dur = tied_dur
        #             tied_note.tie_end = True
        #             tied_note.measure_flag = True
        #             current_beat.add_note(tied_note)
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #         lastcurrent_count = current_count % subdivisions
        #         current_count = overflow
        #     elif current_count_mod > 0 and current_count_floor > 1:
        #         #print("greater than, greater than")
        #         current_note = copy.deepcopy(current_list[location])
        #         last_measure_count = subdivisions - lastcurrent_count
        #         overflow = current_count_mod
        #         if last_measure_count > 0:
        #             how_many_measures = current_count // subdivisions - 1
        #             what_goes_to_the_first_measure = subdivisions - lastcurrent_count
        #             what_goes_to_the_last_measure = overflow
        #             extra_measure_beats = subdivisions * how_many_measures
        #         else:
        #             how_many_measures = current_count // subdivisions
        #             what_goes_to_the_first_measure = False
        #             what_goes_to_the_last_measure = overflow
        #             extra_measure_beats = subdivisions * how_many_measures
        #         if what_goes_to_the_first_measure:
        #             current_note = copy.deepcopy(current_list[location])
        #             current_note.dur = what_goes_to_the_first_measure
        #             current_note.tie_start = True
        #             current_beat.add_note(current_note)
        #         while how_many_measures > 0:
        #             current_note = copy.deepcopy(current_list[location])
        #             current_note.dur = subdivisions
        #             current_note.tie_start = True
        #             # FIXME: This needs to not get switched on first note
        #             current_note.measure_flag = True
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #             if what_goes_to_the_last_measure > 0:
        #                 current_note.tie_end = True
        #             current_note.tie_end = True
        #             current_beat.add_note(current_note)
        #             how_many_measures -= 1
        #         if what_goes_to_the_last_measure > 0:
        #             current_note = copy.deepcopy(current_list[location])
        #             current_note.dur = what_goes_to_the_last_measure
        #             current_note.tie_end = True
        #             current_note.measure_flag = True
        #             current_beat.add_note(current_note)
        #             self.beats.append(current_beat)
        #             current_beat = Beat()
        #             subdivisions = measure_map[current_beat_count]
        #         lastcurrent_count = current_count % subdivisions
        #         current_count = overflow % subdivisions
        #     elif current_count_mod > 0 and current_count_floor < 1:
        #         #print("buisness as usual")
        #         altered_duration = copy.deepcopy(current_list[location])
        #         current_beat.add_note(altered_duration)
        #         lastcurrent_count = current_count_mod
        # return self.beats