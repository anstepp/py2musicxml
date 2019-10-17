import copy
import fractions

from functools import reduce
from lxml import etree
from noteGrouping.py import group_notes

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

    def get_list(self, **kwargs):

        self.measure_factor = (
            kwargs.get("factor") if kwargs.get("factor") else DEFAULT_MEASURE_FACTOR
        )

        self.measure_beats = (
            kwargs.get("beats") if kwargs.get("beats") else DEFAULT_MEASURE_BEATS
        )

        note_sort_method = kwargs.get("how") if kwargs.get("how") else "Default"

        self._clean_list(note_sort_method)

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

    def get_uniques(self, input_list: Iterable[NoteList]):
        uniques = []
        for item in input_list:
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
        measure_list = group_notes(self.current_list, self.subdivisions)
        
        unique_durations = self.get_uniques(middle_list)
        print("durs", unique_durations)
        lcm_of_durations = reduce(self.lcm, unique_durations)
        print("lcm", lcm_of_durations)
        #self.subdivisions = self.measure_factor * lcm_of_durations
        print("self.subdivisions", self.subdivisions)
        # in the future, this will do scaling, etc.
        return_list = middle_list
        return return_list

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

    def get_change_pitch(self, group: Iterable[NoteList]):
        for item, value in group[1:-1]:
            if item > group[value - 1] and item < group[value + 1]:
                return True
            elif item < group[value - 1] and item > group[value + 1]:
                return True

    def get_change_group(self, group: Iterable[NoteList]):
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
                # print("current_count", current_count)
                if current_count == self.subdivisions:
                    if location != len(current_list) - 1:
                        self.current_list[location + 1].measure_flag = True
                    altered_duration = copy.deepcopy(self.current_list[location])
                    altered_duration.dur = altered_duration.dur / current_multiplier
                    return_list.append(altered_duration)
                    current_count = 0
                elif current_count > self.subdivisions:
                    current_note = copy.deepcopy(self.current_list[location])
                    # print("logic for ties", current_count, self.subdivisions)
                    overflow = current_count - self.subdivisions
                    # print("overflow", overflow)
                    pre_tie = self.current_list[location].dur - overflow
                    # print("pre-tie", pre_tie)
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

    def metric_finder(self, subgroup: Iterable[NoteList]):
        pass
