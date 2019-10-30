import copy
import fractions

from functools import reduce
from lxml import etree
from typing import Iterable

DEFAULT_MEASURE_BEATS = 4
DEFAULT_MEASURE_FACTOR = 1


class NoteList:
    measure_factor, measure_beats = None, None
    initial_list, current_list, final_list = None, None, None

    def __init__(self, input_list: list):
        self.current_list = input_list
        self.subdivisions = None
    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def get_part(self, **kwargs):

        self.measure_factor = (
            kwargs.get("factor") if kwargs.get("factor") else DEFAULT_MEASURE_FACTOR
        )

        self.measure_beats = (
            kwargs.get("beats") if kwargs.get("beats") else DEFAULT_MEASURE_BEATS
        )

        note_sort_method = kwargs.get("how") if kwargs.get("how") else "Default"

        self._clean_list(note_sort_method)

        return self.final_list

    def _clean_list(self, how: str):
        if how is "Implied":
            self.final_list = self.groupByImpliedMeter()
        if how is "Map":
            self.final_list = self.group_by_map()
        # default to 4/4
        if how is "Default":
            self.final_list = self.group_list()
        else:
            self.final_list = self.group_list()

    def get_uniques(self):
        uniques = []
        for item in current_list:
            if item.dur not in uniques:
                uniques.append(item.dur)
            else:
                pass
        return uniques

    def group_list(self):
        current_count = 0
        # current count of number of self.subdivisions including the new note (item)
        last_current_count = 0
        middle_list = []
        return_list = []
        self.subdivisions = self.measure_beats * self.measure_factor

        #new function to group by input from the noteGroup function in another file
        measure_list = self.group_list_to_measures(self.subdivisions)
        return measure_list

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
        current_list = self.current_list
        current_count = 0
        middle_list = list()
        for location, item in enumerate(current_list):
            current_count += item.dur
            current_count_floor = current_count // subdivisions
            current_count_mod = current_count % subdivisions
            if current_count_mod == 0 and current_count_floor == 1:
                if item.dur > subdivisions:
                    how_many_measures = current_count // subdivisions
                    what_goes_to_the_first_measure = (
                        item.dur - current_count // subdivisions
                    )
                    last_note_of_old_measure = copy.deepcopy(current_list[location])
                    last_note_of_old_measure.dur = what_goes_to_the_first_measure
                    last_note_of_old_measure.tie_start = True
                    middle_list.append(last_note_of_old_measure)
                    while how_many_measures > 0:
                        whole_measure_note = copy.deepcopy(current_list[location])
                        whole_measure_note.dur = subdivisions
                        if how_many_measures > 1:
                            whole_measure_note.tie_start = True
                        else:
                            whole_measure_note.tie_end = True
                        middle_list.append(whole_measure_note)
                        how_many_measures -= 1
                else:
                    altered_duration = copy.deepcopy(current_list[location])
                    middle_list.append(altered_duration)
                current_count = 0
                if location != len(current_list) - 1:
                    current_list[location + 1].measure_flag = True
            elif current_count_mod == 0 and current_count_floor > 1:
                how_many_measures = current_count // subdivisions
                if location != len(current_list) - 1:
                    current_list[location + 1].measure_flag = True
                how_many_measures = current_count // subdivisions - 1
                what_goes_to_the_first_measure = (
                    item.dur - subdivisions * how_many_measures
                )
                last_note_of_old_measure = copy.deepcopy(current_list[location])
                last_note_of_old_measure.dur = what_goes_to_the_first_measure
                last_note_of_old_measure.tie_start = True
                middle_list.append(last_note_of_old_measure)
                while how_many_measures > 0:
                    note_to_add = copy.deepcopy(current_list[location])
                    note_to_add.dur = subdivisions
                    note_to_add.measure_flag = True
                    middle_list.append(note_to_add)
                    how_many_measures -= 1
                last_current_count = current_count_mod
                current_count = 0
            elif current_count_mod > 0 and current_count_floor == 1:
                current_note = copy.deepcopy(current_list[location])
                overflow = current_count - subdivisions
                if overflow // subdivisions > 1:
                    new_dur = subdivisions
                    current_note.dur = new_dur
                    current_note.tie_start = True
                    middle_list.append(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = new_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    middle_list.append(tied_note)
                else:
                    pre_tie = current_list[location].dur - overflow
                    new_dur = pre_tie
                    current_note.dur = new_dur
                    current_note.tie_start = True
                    middle_list.append(current_note)
                    tied_note = copy.deepcopy(current_list[location])
                    tied_dur = overflow % subdivisions
                    tied_note.dur = tied_dur
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    middle_list.append(tied_note)
                last_current_count = current_count % subdivisions
                current_count = overflow
            elif current_count_mod > 0 and current_count_floor > 1:
                current_note = copy.deepcopy(current_list[location])
                last_measure_count = subdivisions - last_current_count
                overflow = current_count_mod
                if last_measure_count > 0:
                    how_many_measures = current_count // subdivisions - 1
                    what_goes_to_the_first_measure = subdivisions - last_current_count
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
                    middle_list.append(current_note)
                while how_many_measures > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = subdivisions
                    current_note.tie_start = True
                    # FIXME: This needs to not get switched on first note
                    current_note.measure_flag = True
                    if what_goes_to_the_last_measure > 0:
                        current_note.tie_end = True
                    current_note.tie_end = True
                    middle_list.append(current_note)
                    how_many_measures -= 1
                if what_goes_to_the_last_measure > 0:
                    current_note = copy.deepcopy(current_list[location])
                    current_note.dur = what_goes_to_the_last_measure
                    current_note.tie_end = True
                    current_note.measure_flag = True
                    middle_list.append(current_note)
                last_current_count = current_count % subdivisions
                current_count = overflow % subdivisions
            elif current_count_mod > 0 and current_count_floor < 1:
                altered_duration = copy.deepcopy(current_list[location])
                middle_list.append(altered_duration)
                last_current_count = current_count_mod
            return current_list

    """this method is designed to take an input map to allow
    for various time signatures being user defined, or to 
    have different proportions per measure.
    It may not work yet."""

    def group_by_map(self, input_map: list):
        map_to_group = input_map
        for map_value in map_to_group:
            current_beats = map_value[0]
            current_multiplier = map_value[1]
            self.subdivisions = current_beats * current_multiplier
            for location, item in enumerate(self.current_list):
                current_count += item.dur
                # # print("current_count", current_count)
                if current_count == self.subdivisions:
                    if location != len(current_list) - 1:
                        self.current_list[location + 1].measure_flag = True
                    altered_duration = copy.deepcopy(self.current_list[location])
                    altered_duration.dur = altered_duration.dur / current_multiplier
                    return_list.append(altered_duration)
                    current_count = 0
                elif current_count > self.subdivisions:
                    current_note = copy.deepcopy(self.current_list[location])
                    # # print("logic for ties", current_count, self.subdivisions)
                    overflow = current_count - self.subdivisions
                    # # print("overflow", overflow)
                    pre_tie = self.current_list[location].dur - overflow
                    # # print("pre-tie", pre_tie)
                    current_note.dur = pre_tie / current_multiplier
                    current_note.tie_start = True
                    return_list.append(current_note)
                    # there should probably be a "no accidental" flag, too
                    tied_note = copy.deepcopy(self.current_list[location])
                    tied_note.dur = overflow / measure_factor
                    tied_note.tie_end = True
                    tied_note.measure_flag = True
                    return_list.append(tied_note)
                    current_count = overflow
                else:
                    altered_duration = copy.deepcopy(self.current_list[location])
                    altered_duration.dur = altered_duration.dur / current_multiplier
                    return_list.append(altered_duration)
        return return_list
