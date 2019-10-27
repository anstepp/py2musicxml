import copy
import fractions

from functools import reduce
from lxml import etree
from typing import Iterable, List, Tuple
from py2musicxml import Measure, Note

TimeSignature = List[Tuple[int, int]]

DEFAULT_MEASURE_BEATS = 4
DEFAULT_MEASURE_FACTOR = 1


class Part:
    measure_factor, measure_beats = None, None
    initial_list, current_list, final_list = None, None, None
    time_signature = []
    subdivisions, wngob = None, None

    def __init__(self, input_list: Iterable[Note], time_signature: TimeSignature):
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

        subdivisions = self.measure_beats * measure_factor

        self.final_list = self.group_list_to_measures(subdivisions)

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
        highest_level = [pitch for pitch, meter in zip(pitch_locations, meter_locations) if pitch == meter]
        last_location = 0
        #perhaps wrap this in a smaller function and make it recurisve? Is there a non-recusrive way to make this work?
        for location in highest_level:
            subgroup = self.current_list[last_location:location]
            groups_2_and_3 = self.metric_finder(subgroup) #or should I use the .get_change_pitch() and .get_change_group()
            location_map.append(groups_2_and_3)
            location = last_location
        implied_list = self.group_by_map(location_map)
        return implied_list

    def group_list_to_measures(self, subdivisions: int):
        subdivisions = subdivisions
        print(subdivisions)
        measure_list = list()
        current_measure = Measure(self.time_signature[0])
        current_count = 0
        current_list = self.current_list
        print(current_list)
        for location, item in enumerate(current_list):
            current_count += item.dur
            print(location, item, current_count)
            current_count_floor = current_count // subdivisions
            current_count_mod = current_count % subdivisions
            if current_count_mod == 0 and current_count_floor == 1:
                #print("zero, equal")
                if location != len(current_list) - 1:
                    current_list[location + 1].measure_flag = True
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                if item.dur > subdivisions:
                    how_many_measures = current_count // subdivisions
                    what_goes_to_the_first_measure = (
                        item.dur - current_count // subdivisions
                    )
                    last_note_of_old_measure = copy.deepcopy(current_list[location])
                    last_note_of_old_measure.dur = what_goes_to_the_first_measure
                    last_note_of_old_measure.tie_start = True
                    current_measure.add_note(last_note_of_old_measure)
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                    while how_many_measures > 0:
                        whole_measure_note = copy.deepcopy(current_list[location])
                        whole_measure_note.dur = subdivisions
                        if how_many_measures > 1:
                            whole_measure_note.tie_start = True
                        else:
                            whole_measure_note.tie_end = True
                        current_measure.add_note(whole_measure_note)
                        current_measure.subdivide_measure()
                        measure_list.append(current_measure)
                        current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                        how_many_measures -= 1
                else:
                    altered_duration = copy.deepcopy(current_list[location])
                    current_measure.add_note(altered_duration)
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                current_count = 0
            elif current_count_mod == 0 and current_count_floor > 1:
                #print("zero, greater than")
                how_many_measures = current_count // subdivisions
                if location != len(current_list) - 1:
                    current_list[location + 1].measure_flag = True
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                how_many_measures = current_count // subdivisions - 1
                what_goes_to_the_first_measure = (
                    item.dur - subdivisions * how_many_measures
                )
                last_note_of_old_measure = copy.deepcopy(current_list[location])
                last_note_of_old_measure.dur = what_goes_to_the_first_measure
                last_note_of_old_measure.tie_start = True
                current_measure.add_note(last_note_of_old_measure)
                while how_many_measures > 0:
                    note_to_add = copy.deepcopy(current_list[location])
                    note_to_add.dur = subdivisions
                    note_to_add.measure_flag = True
                    current_measure.add_note(note_to_add)
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                    how_many_measures -= 1
                lastcurrent_count = current_count_mod
                current_count = 0
            elif current_count_mod > 0 and current_count_floor == 1:
                #print("greater than, zero")
                current_note = copy.deepcopy(current_list[location])
                overflow = current_count - subdivisions
                if overflow // subdivisions > 1:
                    newDur = subdivisions
                    current_note.dur = newDur
                    current_note.tie_start = True
                    current_measure.add_note(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = newDur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    current_measure.add_note(tied_note)
                else:
                    pre_tie = current_list[location].dur - overflow
                    current_note.dur = pre_tie
                    current_note.tie_start = True
                    current_measure.add_note(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = tied_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    current_measure.add_note(tied_note)
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                lastcurrent_count = current_count % subdivisions
                current_count = overflow
            elif current_count_mod > 0 and current_count_floor > 1:
                #print("greater than, greater than")
                current_note = copy.deepcopy(current_list[location])
                last_measure_count = subdivisions - lastcurrent_count
                overflow = current_count_mod
                if last_measure_count > 0:
                    how_many_measures = current_count // subdivisions - 1
                    what_goes_to_the_first_measure = subdivisions - lastcurrent_count
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
                    current_measure.add_note(current_note)
                while how_many_measures > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = subdivisions
                    current_note.tie_start = True
                    # FIXME: This needs to not get switched on first note
                    current_note.measure_flag = True
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                    if what_goes_to_the_last_measure > 0:
                        current_note.tie_end = True
                    current_note.tie_end = True
                    current_measure.add_note(current_note)
                    how_many_measures -= 1
                if what_goes_to_the_last_measure > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_last_measure
                    current_note.tie_end = True
                    current_note.measure_flag = True
                    current_measure.add_note(current_note)
                    current_measure.subdivide_measure()
                    measure_list.append(current_measure)
                    current_measure = Measure(self.time_signature[(len(measure_list)+1)%len(self.time_signature)])
                lastcurrent_count = current_count % subdivisions
                current_count = overflow % subdivisions
            elif current_count_mod > 0 and current_count_floor < 1:
                #print("buisness as usual")
                altered_duration = copy.deepcopy(current_list[location])
                current_measure.add_note(altered_duration)
                lastcurrent_count = current_count_mod
        return measure_list