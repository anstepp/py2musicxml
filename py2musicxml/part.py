import copy
import fractions

from functools import reduce
from lxml import etree
from typing import Iterable, List, Tuple
from py2musicxml import Measure, Note, Beat, Rest
from collections import namedtuple

TimeSignature = List[Tuple[int, int]]

DEFAULT_MEASURE_BEATS = 4
DEFAULT_MEASURE_FACTOR = 1


class Part:
    def __init__(self, input_list: Iterable[Note], time_signature: TimeSignature):
        self.measure_factor, self.measure_beats = None, None
        self.subdivisions, self.max_subdivisions = None, None
        self.time_signature_index, self.current_beat_count, self.current_count = (
            None,
            None,
            None,
        )
        self.additive_beat_count = None
        self.current_count_mod, self.current_count_floor = None, None
        self.measure_list, self.current_list, self.final_list = list(), list(), list()
        self.current_list = input_list
        self.time_signature = time_signature
        self.measure_beats = self.time_signature[0][0]
        self.wngob = self.time_signature[0][1]
        self.current_count = 0
        self.get_part(1)

    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def get_part(self, measure_factor: int):

        self.measure_factor = measure_factor
        self.group_list_to_measures()
        # [measure.subdivide_measure() for measure in self.measure_list]

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

    def append_and_increment_measure(self) -> None:
        self.current_measure.add_beat(self.current_beat)
        self.measure_list.append(self.current_measure)
        self.advance_time_signature_index()
        self.current_measure = Measure(self.time_signature[self.time_signature_index])
        self.current_beat = Beat()
        self.additive_beat_count = self.current_measure.count_generator()
        self.set_current_count_adjacencies()
        self.max_subdivisions = self.current_measure.additive_beat_max
        self.current_beat_count = 0
        self.subdivisions = self.current_measure.additive_beat_list[
            self.current_beat_count
        ]

    def advance_time_signature_index(self) -> None:
        self.time_signature_index = (self.time_signature_index + 1) % len(
            self.time_signature
        )

    def advance_current_beat_count(self, advance: int) -> None:
        """If the measure is full of beats, we need to append the measure
        and advance to a new measure. Otherwise, just advance the current
        count"""
        self.current_beat_count += advance
        if self.current_beat_count >= len(self.current_measure.measure_map) - 1:
            self.append_and_increment_measure()
            self.current_beat_count = 0
            self.current_beat = Beat()
        else:
            self.current_measure.add_beat(self.current_beat)
            self.subdivisions = self.current_measure.additive_beat_list[
                self.current_beat_count
            ]
            self.current_beat = Beat()

    def make_whole_measure_note(self, size: int, advance: int) -> None:
        self.current_beat = Beat()
        note_to_add = copy.deepcopy(self.current_note)
        note_to_add.dur = size
        self.current_beat.add_note(note_to_add)
        self.append_and_increment_measure()

    def make_multi_beat_rest(self, rest: Rest, advance: int) -> None:
        multi_beat = Beat()
        multi_beat.add_note(rest)
        self.current_measure.add_beat(multi_beat)
        for index in range(advance):
            self.advance_current_beat_count()

    def get_internal_measures(self) -> None:
        # print("current_beat_count", self.current_beat_count)
        # Get any remiander of the note that belongs in the last measure
        if self.current_beat_count > 0:
            # print("current_beat_count > 1")
            overflow = self.current_measure_mod
            old_measure_dur = self.max_subdivisions - self.current_count
            if old_measure_dur:
                old_measure_note = copy.deepcopy(self.current_note)
                old_measure_note.dur = old_measure_dur
                self.current_beat.add_note(old_measure_note)
                self.append_and_increment_measure()
                # print("appended old measure")

        # Test for all subdivisions being equal

        if self.current_measure.equal_divisions:
            how_many_measures = self.current_measure_floor
            if self.current_beat_count is 0:
                while how_many_measures > 0:
                    # print('current_count_mod: {}'.format(self.current_count_mod))
                    # print('current_measure_mod: {}'.format(self.current_measure_mod))

                    # print("how many measures", how_many_measures)
                    """This uses the type of measure to write a whole measure.
                    Eventually, we need to take cases of dotted notes that cross
                    one level of subdivisions, as well as half notes in 3 and 4/4"""
                    if self.current_measure.meter is "Duple":
                        if self.current_count >= 2:
                            self.make_whole_measure_note(2, 2)
                            self.current_count -= 2
                            self.set_current_count_adjacencies()
                            how_many_measures = self.current_measure_floor
                    elif self.current_measure.meter is "Triple":
                        # print("I'm in triple, current_count {}".format(self.current_count))
                        if self.current_count >= 3:
                            # print('and currentcount is gte 3')
                            self.make_whole_measure_note(3, 3)
                            self.current_count -= 3
                            # print("current_count:", self.current_count)
                            how_many_measures -= 1
                            # print(
                            #     "Current count:",
                            #     self.current_count,
                            #     "hm measures:",
                            #     how_many_measures,
                            # )

                    elif self.current_measure is "Quadruple":
                        if self.current_count >= 4:
                            self.make_whole_measure_note(4, 4)
                            self.current_count -= 4
                            self.set_current_count_adjacencies()
                            how_many_measures = self.current_measure_floor

                # print("BEFORE REMIANDER")
                # print('self.current_measure_mod: {}'.format(self.current_measure_mod))

                if self.current_measure_mod > 0:
                    # print("REMIANDER")
                    # print("self.current_count: {}".format(self.current_count))
                    remiander_note = copy.deepcopy(self.current_note)
                    remiander_note.dur = self.current_count
                    self.current_beat.add_note(remiander_note)
                    self.advance_current_beat_count(self.current_count)
                    self.current_count = remiander_note.dur
                else:
                    pass
        else:
            """Eventually, this will deal with additive meters.
            For now, skip, and fail on a test by testing:
            assert self.current_measure.equal_divisions = True"""
            pass
        return self.current_count

    def set_current_count_adjacencies(self) -> int:
        self.current_count_floor = self.current_count // self.subdivisions
        self.current_count_mod = self.current_count % self.subdivisions
        self.current_measure_floor = self.current_count // self.max_subdivisions
        self.current_measure_mod = self.current_count % self.max_subdivisions

        return self.current_measure_floor
        # print("adjacencies set", self.current_count_floor, self.current_count_mod, self.current_measure_floor, self.current_measure_mod)

    def wrap_up(self) -> None:
        last_measure = self.measure_list[-1]
        duration_passed = 0
        for beat in last_measure.beats:
            for note in beat.notes:
                duration_passed += note.dur
                # print(duration_passed)
        counter = -1
        while counter > (len(last_measure.additive_beat_list) * -1):
            if duration_passed < last_measure.additive_beat_list[counter]:
                pass
                # print("Duration {}, Beat Count {}".format(duration_passed, last_measure.additive_beat_list[counter]))
            else:
                counter -= 1

    def group_list_to_measures(self) -> None:

        current_information_tuple = namedtuple(
            "current_information_tuple",
            ['current_measure',
            'current_beat',
            'current_measure_count',
            'time_signature_index',
            'current_beat_count',
            'subdivisions',
            'current_note',
            'current_count']
        )

        self.current_measure = Measure(self.time_signature[0])
        self.current_beat = Beat()

        self.current_measure_count = 0
        self.time_signature_index = 0
        self.current_beat_count = 0

        self.measure_beat_list = self.current_measure.additive_beat_list
        self.subdivisions = self.measure_beat_list[self.current_beat_count]
        self.max_subdivisions = self.current_measure.additive_beat_max

        for location, note in enumerate(self.current_list):
            self.current_note = note
            self.current_count += self.current_note.dur
            # print("new note current count", self.current_count)
            current_count = self.set_current_count_adjacencies()
            # print("note {}, current_count {}, current_measure_floor {} current_measure_mod {}".format(
            #    note, self.current_count, self.current_measure_floor, self.current_measure_mod))
            # in this case, we need to advance the measure count
            if self.current_measure_floor >= 1:
                # use this to clean up the measures that exist
                self.get_internal_measures()
                """This has advanced the measure, and the measure may be incomplete.
                If the next note advances beyond a measure, this function is called again.
                Else, the else."""
            else:
                if self.current_count >= self.subdivisions:
                    self.current_beat.add_note(self.current_note)
                    self.advance_current_beat_count(self.current_count)
                else:
                    # append to beat, do not advance beats
                    self.current_beat.add_note(self.current_note)
        # self.wrap_up()
