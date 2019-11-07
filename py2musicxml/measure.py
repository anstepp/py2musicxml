from py2musicxml import Note, Beat, Rest

import copy
from typing import Union, Iterable


class Measure:
    index = None
    weight = None
    # divisions is self.subdivisions of the quarter note
    divisions = None
    # self.subdivisions is the musical
    subdivisions = 1
    #default to non-additive meter, this self corrects
    equal_divisions = True

    meter_dict = {2: "Duple", 3: "Triple", 4: "Quadruple"}
    meter_type = None
    meters = [2, 3, 4]
    meter = None
    is_empty = True

    def __init__(self, time_signature: tuple):
        self.notes = list()
        self.beats = list()
        self.meter_counts = list()
        self.time_signature = time_signature
        self.divide_measure()
        self.additive_beat_gen = self.count_generator()
        self.additive_beat_list = list((x for x in self.additive_beat_gen))

    def count_generator(self):
        count = 0
        for beat in self.measure_map:
            count += beat
            yield count

    def add_note(self, note: Note):
        self.notes.append(note)
        self.is_empty = False

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

    def divide_measure(self):
        if self.equal_divisions:
            if self.time_signature[1] % 3 is 0:
                how_many_beats = self.time_signature[0] / 3
                self.meter_type = "Compound"
                if how_many_beats in self.meters:
                    self.meter = self.meter_dict[how_many_beats]
                self.measure_map = [1 for x in range(how_many_beats)]
                count = 0
            elif self.time_signature[1] % 2 == 0:
                self.meter_type = "Simple"
                how_many_beats = self.time_signature[0]
                self.measure_map = [1 for x in range(how_many_beats)]
                if how_many_beats in self.meters:
                    self.meter = self.meter_dict[how_many_beats]
            else:
                equal_divisions = False
                self.meter = "Additive"
                self.measure_map = self.bjorklund()
        else:
            self.meter = "Additive"
            self.measure_map = self.bjorklund()

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
            remainderCount = [
                counter + 1 for x in remainderList if x is min(remainderList)
            ]
            remainder = len(remainderList)
        return returnList[0]

    def check_for_multiple_value(self, index: int, current_note: Note) -> bool:
        index = index
        current_beat = self.measure_map[index]
        if self.equal_divisions:
            if self.meter == "Duple":
                if current_note.dur == current_beat * 2:
                    new_beat = Beat()
                    new_beat.add_note(current_note)
                    self.beats.append(new_beat)
                    index += 1
                    return index
            if self.meter == "Triple":
                if (
                    current_note.dur == current_beat * 3
                    or current_note.dur == current_beat * 2
                ):
                    new_beat = Beat()
                    new_beat.add_note(current_note)
                    self.beats.append(new_beat)
                    index += 1
                    return index
            if self.meter == "Quadruple":
                if (
                    current_note.dur == current_beat * 4
                    or current_note.dur == current_beat * 2
                ):
                    new_beat = Beat()
                    new_beat.add_note(current_note)
                    self.beats.append(new_beat)
                    index += 1
                    return index
                elif current_note.dur == current_beat * 3 and index < 2:
                    new_beat = Beat()
                    new_beat.add_note(current_note)
                    self.beats.append(new_beat)
                    index += 1
                    return index
                else:
                    return index
            else:
                return index
        else:
            return index

    def get_extra_beats(self, overflow: int) -> int:
        overflow = overflow
        beat_count = 0
        for subdivisions in self.measure_map:
            overflow - subdivisions
            if overflow:
                beat_count += 1
        return beat_count

    def remove_extra_beats(self, count: int, index: int, dur: int) -> int:
        count = count + 1
        dur = dur
        end = index + count
        number_of_beat_subdivisions = 0
        for beat_duration in self.measure_map[count:end]:
            number_of_beat_subdivisions += beat_duration
        new_dur = dur - number_of_beat_subdivisions
        return new_dur

    def append_and_increment(self, measure: Beat, current_beat_count: int):
        current_beat_count = current_beat_count
        beat = measure
        self.beats.append(beat)
        # print(self.beats)
        current_beat_count += 1
        return Beat(), current_beat_count

    def subdivide_measure(self):
        current_beat = Beat()
        current_count = 0
        current_beat_count = 0
        current_list = self.notes
        for location, current_note in enumerate(current_list):
            current_count += current_note.dur
            subdivisions = self.measure_map[current_beat_count]
            print("current note dur {}, current count {} subdivisions {}".format(current_note.dur, current_count,subdivisions))
            current_beat_count = self.check_for_multiple_value(current_beat_count, current_note)
            current_count_floor = current_count // subdivisions
            current_count_mod = current_count % subdivisions
            # Completes a measure and has no extra measures
            if current_count_mod == 0 and current_count_floor == 1:
                print("zero, equal")
                if current_note.dur > subdivisions:
                    how_many_measures = current_count // subdivisions
                    what_goes_to_the_first_measure = (
                        current_note.dur - current_count // subdivisions
                    )
                    last_note_of_old_measure = copy.deepcopy(current_list[location])
                    last_note_of_old_measure.dur = what_goes_to_the_first_measure
                    last_note_of_old_measure.tie_start = True
                    current_beat.add_note(last_note_of_old_measure)
                    current_beat, subdivisions = self.append_and_increment(
                        current_beat, current_beat_count
                    )

                    while how_many_measures > 0:
                        whole_measure_note = copy.deepcopy(current_list[location])
                        whole_measure_note.dur = subdivisions
                        if how_many_measures > 1:
                            whole_measure_note.tie_start = True
                        else:
                            whole_measure_note.tie_end = True
                        current_beat.add_note(whole_measure_note)
                        current_beat, subdivisions = self.append_and_increment(
                            current_beat, current_beat_count
                        )
                        how_many_measures -= 1
                else:
                    altered_duration = copy.deepcopy(current_list[location])
                    current_beat.add_note(altered_duration)
                    current_beat, subdivisions = self.append_and_increment(
                        current_beat, current_beat_count
                    )
                current_count = 0

            # Completes a measure, and may have extra measures
            elif current_count_mod == 0 and current_count_floor > 1:
                print("zero, greater than")
                current_beat_count = self.check_for_multiple_value(current_beat_count ,current_note)
                how_many_beats = self.get_extra_beats(current_count_floor)
                what_goes_to_the_first_beat = self.remove_extra_beats(
                    current_beat_count, how_many_beats, current_note.dur
                )
                last_note_of_old_measure = copy.deepcopy(current_list[location])
                last_note_of_old_measure.dur = what_goes_to_the_first_beat
                last_note_of_old_measure.tie_start = True
                current_beat.add_note(last_note_of_old_measure)
                while how_many_beats > 0:
                    note_to_add = copy.deepcopy(current_list[location])
                    note_to_add.dur = subdivisions
                    note_to_add.measure_flag = True
                    current_beat.add_note(note_to_add)
                    current_beat, subdivisions = self.append_and_increment(
                        current_beat, current_beat_count
                    )
                    how_many_beats -= 1
                lastcurrent_count = current_count_mod
                current_count = 0

            # doesn't complete a measure, and doesn't have extra measures
            elif current_count_mod > 0 and current_count_floor == 1:
                print("greater than, zero")
                current_note = copy.deepcopy(current_list[location])
                overflow = current_count - subdivisions
                if overflow // subdivisions > 1:
                    newDur = subdivisions
                    current_note.dur = newDur
                    current_note.tie_start = True
                    current_beat.add_note(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = newDur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    current_beat.add_note(tied_note)
                else:
                    pre_tie = current_list[location].dur - overflow
                    current_note.dur = pre_tie
                    current_note.tie_start = True
                    current_beat.add_note(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = tied_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    current_beat.add_note(tied_note)
                    current_beat, subdivisions = self.append_and_increment(
                        current_beat, current_beat_count
                    )
                lastcurrent_count = current_count % subdivisions
                current_count = overflow

            # doesn't complete a measure, and has extra measures
            elif current_count_mod > 0 and current_count_floor > 1:
                print("greater than, greater than")
                current_note = copy.deepcopy(current_list[location])
                last_measure_count = subdivisions - lastcurrent_count
                overflow = current_count_mod
                if last_measure_count > 0:
                    how_many_measures = current_count // subdivisions - 1
                    what_goes_to_the_first_measure = (
                        subdivisions - lastcurrent_count
                    )
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                else:
                    how_many_measures = current_count // subdivisions
                    what_goes_to_the_first_measure = False
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                if what_goes_to_the_first_measure:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_first_measure
                    current_note.tie_start = True
                    current_beat.add_note(current_note)
                while how_many_measures > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = subdivisions
                    current_note.tie_start = True
                    # FIXME: This needs to not get switched on first note
                    current_beat.make_beams()
                    current_beat, subdivisions = self.append_and_increment(
                        current_beat, current_beat_count
                    )
                    if what_goes_to_the_last_measure > 0:
                        current_note.tie_end = True
                    current_note.tie_end = True
                    current_beat.add_note(current_note)
                    how_many_measures -= 1
                if what_goes_to_the_last_measure > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_last_measure
                    current_note.tie_end = True
                    current_beat.add_note(current_note)
                    current_beat.make_beams()
                    current_beat, subdivisions = self.append_and_increment(
                        current_beat, current_beat_count
                    )
                lastcurrent_count = current_count % subdivisions
                current_count = overflow % subdivisions

            # doesn't complete a measure, doesn't have extra measures
            elif current_count_mod > 0 and current_count_floor < 1:
                print("buisness as usual")
                altered_duration = copy.deepcopy(current_list[location])
                current_beat.add_note(altered_duration)
                lastcurrent_count = current_count_mod

            #fill measure with rests
            if current_count_mod != 0:
                for beat in self.measure_map[current_beat_count:]:
                    rest = Rest(beat)
                    self.beats.append(rest)
            #[beat.make_beams() for beat in self.beats]
