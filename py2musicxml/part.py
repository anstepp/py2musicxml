import copy
import fractions

from functools import reduce
from lxml import etree
from typing import Iterable, List, Tuple
from py2musicxml import Measure, Note, Beat

TimeSignature = List[Tuple[int, int]]

DEFAULT_MEASURE_BEATS = 4
DEFAULT_MEASURE_FACTOR = 1


class Part:
    measure_factor, measure_beats = None, None
    subdivisions, wngob = None, None
    time_signature_index, current_beat_count, current_count = None, None, None
    additive_beat_count = None

    def __init__(self, input_list: Iterable[Note], time_signature: TimeSignature):
        self.measure_list, self.current_list, self.final_list = list(), list(), list()
        self.current_list = input_list
        self.time_signature = time_signature
        self.measure_beats = self.time_signature[0][0]
        self.wngob = self.time_signature[0][1]
        self.get_part(1)

    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def get_part(self, measure_factor: int):

        self.measure_factor = measure_factor
        self.group_list_to_measures()
        #[measure.subdivide_measure() for measure in self.measure_list]

    def get_uniques(self):
        uniques = []
        for item in current_list:
            if item.dur not in uniques:
                uniques.append(item.dur)
            else:
                pass
        return uniques

    def assign_measure_weight(self):
        for note in self.current_list:
            if note.measure_flag is False:
                pass
            else:
                if note.location is 1:
                    weight = 1000
                else:
                    if get_change_pitch(self.current_list[note:note]):
                        note.weight += 1
                    if note.duration > subdivisions:
                        note.weight += 1

    def compare_weight(self):
        pass

    # def get_change_pitch(self, range: window):
    #     for item, value in group[1:-1]:
    #         if item > group[value - 1] and item < group[value + 1]:
    #             return True
    #         elif item < group[value - 1] and item > group[value + 1]:
    #             return True

    def get_change_group(self,):
        pass

    def get_implied_meter(self):
        location_map = []
        pitch_locations = self.get_change_pitch()
        meter_locations = self.get_change_group()
        highest_level = [
            pitch
            for pitch, meter in zip(pitch_locations, meter_locations)
            if pitch == meter
        ]
        last_location = 0
        # perhaps wrap this in a smaller function and make it recurisve? Is there a non-recusrive way to make this work?
        for location in highest_level:
            subgroup = self.current_list[last_location:location]
            groups_2_and_3 = self.metric_finder(
                subgroup
            )  # or should I use the .get_change_pitch() and .get_change_group()
            location_map.append(groups_2_and_3)
            location = last_location
        implied_list = self.group_by_map(location_map)
        return implied_list

    """Call this function to advance to the next measure.
    This should only be called when a measure is full, that is,
    current_beat_count is full, or the subdivisions are full.
    """
    def append_and_increment(self) -> None:
        for note in self.current_measure.notes:
            print(
                "measure added, new current_measure",
                self.measure_list,
                self.measure_list[0].notes,
                note.dur,
            )
        self.measure_list.append(self.current_measure)
        self.advance_time_signature_index()
        self.current_measure = Measure(self.time_signature[self.time_signature_index])

    def advance_time_signature_index(self) -> None:
        self.time_signature_index = (self.time_signature_index + 1) % len(self.time_signature)

    def advance_current_beat_count(self) -> None:
        """If the measure is full of beats, we need to append the measure
        and advance to a new measure. Otherwise, just advance the current
        count"""
        if self.current_beat_count == len(self.current_measure.measure_map):
            self.current_beat_count = 0
            self.append_and_increment()
        else:
            self.current_beat_count += 1
            self.additive_beat_count.next()

    def make_multi_beat_note(self) -> None:
        multi_beat_note = Beat()
        multi_beat_note.notes.append(self.current_note)
        self.current_measure.beats.append(multi_beat_note)
        self.append_and_increment()

    def get_internal_measures(self) -> None:
        accumulated_beats = 0
        # Test for all subdivisions being equal
        if self.current_measure.equal_divisions:
            while self.current_count > accumulated_beats:
                remaining_measure_duration = 0
                if self.current_measure.meter is "Duple":
                    if self.current_count == remaining_measure_duration:
                        self.make_multi_beat_note()
                        self.current_beat_count = 0
                if self.current_measure.meter is "Triple":
                    if self.current_count == remaining_measure_duration:
                        self.make_multi_beat_note()
                        self.current_beat_count = 0
                if self.current_measure is "Quadruple":
                    if self.current_count == remaining_measure_duration:
                        self.make_multi_beat_note()
                        self.current_beat_count = 0
                beat_to_add = self.current_measure.measure_map[self.current_beat_count]
                """In the case that the current_beat_count is advanced beyond the
                number of beats in the measure, advance the beat count. accumulated_beats
                and self.current_beat_count continue without change, however. This
                represents a full measure, appended inside advance_current_beat_count,
                and self.current_measure becomes a new measure."""
                if self.current_beat_count > len(self.current_measure.measure_map):
                    accumulated_beats += beat_to_add
                    self.advance_current_beat_count()
                    print(self.current_beat_count, self.current_count, accumulated_beats)
                else:
                    accumulated_beats += beat_to_add
                    self.advance_current_beat_count
        else:
            """Eventually, this will deal with additive meters.
            For now, skip, and fail on a test by testing:
            self.current_measure.equal_divisions = True"""
            pass

        self.current_measure = Measure(self.time_signature[self.time_signature_index])


    def group_list_to_measures(self):
        measure_list = list()
        self.current_measure = Measure(self.time_signature[0])
        current_list = self.current_list
        self.current_measure_count = 0
        self.time_signature_index = 0
        self.current_beat_count = 0
        self.current_count = 0
        self.additive_beat_count = self.current_measure.count_generator()
        for location, item in enumerate(current_list):
            maximum_measure_duration = 0
            for division in self.current_measure.measure_map:
                maximum_measure_duration += division
            subdivisions = self.current_measure.measure_map[self.current_beat_count]
            self.current_count += item.dur
            current_count_floor = self.current_count // subdivisions
            current_count_mod = self.current_count % subdivisions
            # print('current measure: {}, current measure notes: {}'.format(current_measure, current_measure.notes))

            if current_count_mod == 0 and current_count_floor == 1:
                print("zero, equal")

                if item.dur > maximum_measure_duration:
                    self.get_internal_measures()
                    self.current_measure = self.append_and_increment()
                    print(self.current_measure)
                    while how_many_measures > 0:
                        whole_measure_note = copy.deepcopy(current_list[location])
                        whole_measure_note.dur = subdivisions
                        if how_many_measures > 1:
                            whole_measure_note.tie_start = True
                        else:
                            whole_measure_note.tie_end = True
                        self.current_measure.add_note(whole_measure_note)
                        self.current_measure = self.append_and_increment()
                        how_many_measures -= 1
                else:
                    altered_duration = copy.deepcopy(current_list[location])
                    self.current_measure.add_note(altered_duration)
                    self.current_measure = self.append_and_increment()
                    print(self.current_measure)
                self.current_count = 0

            elif current_count_mod == 0 and current_count_floor > 1:
                print("zero, greater than")

                self.get_internal_measures()
                lastcurrent_count = current_count_mod
                self.current_count = 0


            elif current_count_mod > 0 and current_count_floor == 1:
                print("greater than, zero")
                current_note = copy.deepcopy(current_list[location])
                overflow = self.current_count - subdivisions
                if overflow // subdivisions > 1:
                    newDur = subdivisions
                    current_note.dur = newDur
                    current_note.tie_start = True
                    self.current_measure.add_note(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = newDur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    self.current_measure.add_note(tied_note)
                else:
                    pre_tie = current_list[location].dur - overflow
                    current_note.dur = pre_tie
                    current_note.tie_start = True
                    self.current_measure.add_note(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = tied_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    self.current_measure.add_note(tied_note)
                    self.append_and_increment()
                    print(current_measure)
                lastcurrent_count = self.current_count % subdivisions
                self.current_count = overflow
            elif current_count_mod > 0 and current_count_floor > 1:
                print("greater than, greater than")
                current_note = copy.deepcopy(current_list[location])
                last_measure_count = subdivisions - lastcurrent_count
                overflow = current_count_mod
                if last_measure_count > 0:
                    how_many_measures = self.current_count // subdivisions - 1
                    what_goes_to_the_first_measure = subdivisions - lastcurrent_count
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                else:
                    how_many_measures = self.current_count // subdivisions
                    what_goes_to_the_first_measure = False
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = subdivisions * how_many_measures
                if what_goes_to_the_first_measure:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_first_measure
                    current_note.tie_start = True
                    self.current_measure.add_note(current_note)
                while how_many_measures > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = subdivisions
                    current_note.tie_start = True
                    # FIXME: This needs to not get switched on first note
                    current_note.measure_flag = True
                    self.append_and_increment()
                    print(self.current_measure)
                    if what_goes_to_the_last_measure > 0:
                        current_note.tie_end = True
                    current_note.tie_end = True
                    self.current_measure.add_note(current_note)
                    how_many_measures -= 1
                if what_goes_to_the_last_measure > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_last_measure
                    current_note.tie_end = True
                    current_note.measure_flag = True
                    self.current_measure.add_note(current_note)
                    self.append_and_increment()
                    print(current_measure)
                lastcurrent_count = current_count % subdivisions
                self.current_count = overflow % subdivisions
            elif current_count_mod > 0 and current_count_floor < 1:
                print("buisness as usual")
                altered_duration = copy.deepcopy(current_list[location])
                self.current_measure.add_note(altered_duration)
                lastcurrent_count = current_count_mod
