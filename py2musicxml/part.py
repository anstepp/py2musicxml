import copy
import fractions

from lxml import etree
from typing import Iterable, List, NamedTuple, Tuple, Union
from py2musicxml import Measure, Note, Beat, Rest

# from collections import namedtuple

TimeSignatures = List[Tuple[int, int]]


class CurrentCountDivisions(NamedTuple):
    beat_floor: int
    beat_mod: int
    measure_floor: int
    measure_mod: int


class Part:
    def __init__(self, input_list: Iterable[Note], time_signatures: TimeSignatures):

        self.current_list = input_list

        self.measures = []

        # TS stuff
        self.time_signatures = time_signatures
        self.time_signature_index = 0

        self.subdivisions, self.max_subdivisions = None, None

        # where we are in the cumulative beats
        self.current_beat_count = None
        self.current_measure = None
        # value of note duration that needs to be written
        # current count gets incremented when we intake the next note
        # gets decremented when we write a measure
        self.current_count = 0

        # current count mod or floor divided by current cumulative beat
        self.current_count_mod, self.current_count_floor = None, None

        #  self.current_measure_mod, self.current_measure_floor
        uniques = self.get_uniques()
        self.measure_factor = self._get_factor(uniques)

        self.create_part()

    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def create_part(self):
        '''Transform input list of notes into a list of measures'''
        self.group_list_to_measures()

    def get_uniques(self) -> list:
        '''unique durations of the notes in the list'''
        uniques = []
        for item in self.current_list:
            if item.dur not in uniques:
                uniques.append(item.dur)
            else:
                pass
        return uniques

    def _get_factor(self, input_list: list) -> int:
        current = 1
        factor = 1
        for item in input_list:
            if item <= 0.5:
                current *= item
                factor = round(1/current)
        return factor

    def assign_measure_weight(self):
        weight = 0
        for index, measure in enumerate(self.measures):
            pass

    def compare_weight(self):
        pass

    # def get_change_pitch(self, range: window):
    #     for item, value in group[1:-1]:
    #         if item > group[value - 1] and item < group[value + 1]:
    #             return True
    #         elif item < group[value - 1] and item > group[value + 1]:
    #             return True

    def get_change_group(self):
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

    def _advance_time_signature_index(self) -> None:
        self.time_signature_index = (self.time_signature_index + 1) % len(
            self.time_signatures
        )

    def append_and_increment_measure(self) -> None:
        '''The measure is full, so add in the current beat and push into self.measures
        then create a fresh measure and beat

        Call this function to advance to the next measure.
            This should only be called when a measure is full, that is,
            current_beat_count is full, or the subdivisions are full.
        '''

        self.current_measure.add_beat(self.current_beat)
        self.measures.append(self.current_measure)

        self._advance_time_signature_index()

        self.current_measure = Measure(self.time_signatures[self.time_signature_index], self.measure_factor)
        self.max_subdivisions = self.current_measure.total_cumulative_beats
        self.current_beat_count = 0
        self.subdivisions = self.current_measure.cumulative_beats[
            self.current_beat_count
        ]

        self.current_beat = Beat(self.subdivisions)

        self.current_beat_count = 0


    def advance_current_beat_count(self) -> None:
        """If the measure is full of beats, we need to append the measure
        and advance to a new measure. Otherwise, just advance the current
        count"""

        self.current_beat_count += 1
        if self.current_beat_count >= len(self.current_measure.cumulative_beats):
            pass
        else:
            self.current_measure.add_beat(self.current_beat)
            self.subdivisions = self.current_measure.cumulative_beats[
                self.current_beat_count
            ]
            self.current_beat = Beat(self.subdivisions)

    def make_whole_measure_note(self, duration: int, advance: int, tie: bool) -> None:
        note_to_add = copy.deepcopy(self.current_note)
        note_to_add.dur = duration * self.measure_factor
        if tie:
            note_to_add.tie_start = True
        #print(note_to_add)
        self.current_beat.add_note(note_to_add)
        self.current_beat.multi_beat = True
        self.append_and_increment_measure()

    def make_multi_beat_rest(self, rest: Rest, advance: int) -> None:
        multi_beat = Beat(self.subdivisions)
        multi_beat.add_note(rest)
        self.current_measure.add_beat(multi_beat)
        for index in range(advance):
            self.advance_current_beat_count()

    def _full_measure_tie_check(self) -> bool:
        if self.current_measure_mod > 0:
            return True
        elif self.current_measure_floor > 1:
            return True
        else:
            return False

    def get_internal_measures(self) -> int:
        #print("get_internal_measures invoked")
        # print("current_beat_count", self.current_beat_count)
        # Get any remainder of the note that belongs in the last measure

        if self.current_beat_count > 0:
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

            # how many measures do we need to write
            while self.current_measure_floor >= 1:
                """This uses the type of measure to write a whole measure.
                Eventually, we need to take cases of dotted notes that cross
                one level of subdivisions, as well as half notes in 3 and 4/4"""
                if self.current_measure.meter_division is "Duple":
                    if self._full_measure_tie_check():
                        self.make_whole_measure_note(2, 2, True)
                    else:
                        self.make_whole_measure_note(2,2,False)
                    if self.current_count == 2:
                        self.current_count = 0
                    else:
                        self.current_count -= 2
                    self.set_current_count_adjacencies()

                elif self.current_measure.meter_division is "Triple":
                    if self._full_measure_tie_check():
                        self.make_whole_measure_note(3, 3, True)
                    else:
                        self.make_whole_measure_note(3,3,False)
                    if self.current_count == 3:
                        self.current_count = 0
                    else:
                        self.current_count -= 3
                    self.set_current_count_adjacencies()

                elif self.current_measure.meter_division is "Quadruple":
                    if self._full_measure_tie_check():
                        self.make_whole_measure_note(4, 4, True)
                    else:
                        self.make_whole_measure_note(4,4,False)
                    if self.current_count == 4:
                        self.current_count = 0
                    else:
                        self.current_count -= 4
                    self.set_current_count_adjacencies()

        else:
            """Eventually, this will deal with additive meters.
            For now, skip, and fail on a test by testing:
            assert self.current_measure.equal_divisions = True"""
            pass
        last_current_count = self.current_count
        return last_current_count

    def set_current_count_adjacencies(self) -> None:
        self.current_count_floor = self.current_count // self.subdivisions
        self.current_count_mod = self.current_count % self.subdivisions
        self.current_measure_floor = self.current_count // self.max_subdivisions
        self.current_measure_mod = self.current_count % self.max_subdivisions

    def _get_current_count_divisions(
        self,
        current_count: int,
        measure_subdivisions: int,
        measure_max_subdivisions: int,
    ) -> CurrentCountDivisions:
        return CurrentCountDivisions(
            beat_floor=current_count // measure_subdivisions,
            beat_mod=current_count % measure_subdivisions,
            measure_floor=current_count // measure_max_subdivisions,
            measure_mod=current_count % measure_max_subdivisions,
        )

    def wrap_up(self, remainder: int) -> None:
        self.current_beat.add_note(Rest(remainder))
        self.current_measure.add_beat(self.current_beat)
        self.measures.append(self.current_measure)

    def group_list_to_measures(self) -> None:

        self.current_measure = Measure(self.time_signatures[self.time_signature_index], self.measure_factor)
        

        # how many beats in measure we have traveled
        self.current_beat_count = 0

        # keep track of how full the beat is

        # MEASURE subdivisions and max subdivisions
        self.subdivisions = self.current_measure.cumulative_beats[
            self.current_beat_count
        ]

        self.current_beat = Beat(self.subdivisions)

        self.max_subdivisions = self.current_measure.total_cumulative_beats

        remainder = 0
        for location, note in enumerate(self.current_list):

            """Iterate through the list of notes and group them into
            measures and beats. As we iterate, we advance a counter called
            current_count (that persists outside this function) to measure
            how many counts that need to be allocated. It gets
            incrememted when we have a new note, and either set to zero or 
            decrememted when measures pass."""

            self.current_note = note
            self.current_count += round(self.current_note.dur * self.measure_factor)
            #print("new iteration",self.current_count)

            """We call this function now, and when current count changes
            to set variables to measure the relationship of the current count
            to the measure length."""
            self.set_current_count_adjacencies()

            if self.current_measure_floor == 1 and self.current_measure_mod == 0:
                measure_or_less_test = True
            else:
                measure_or_less_test = False

            if measure_or_less_test or self.current_measure_floor == 0:
                #print("less than a measure, location {}, note {}, remainder {}, current_count {}, current_measure_floor {}, current_measure_mod {}, max_subdivisions {}".format(location, note, remainder, self.current_count, self.current_measure_floor, self.current_measure_mod, self.max_subdivisions))
                note_to_add = copy.deepcopy(self.current_note)
                note_to_add.dur = round(self.measure_factor * note_to_add.dur)
                self.current_beat.add_note(note_to_add)
                if self.current_count >= self.subdivisions:
                    self.advance_current_beat_count()
                if self.current_count < self.max_subdivisions:
                    remainder = self.current_count

                else:
                    self.append_and_increment_measure()
                    self.current_count = 0
                    self.set_current_count_adjacencies()
                    remainder = 0

            if self.current_measure_floor >= 1:
                #print("over a measure, location {}, note {}, remainder {}, current_measure_floor {}, current_measure_mod {}, current_count {}, max_subdivisions {}".format(location, note, remainder, self.current_measure_floor, self.current_measure_mod, self.current_count, self.max_subdivisions))
                if remainder > 0:
                    """In this case, we have leftover note duration from the previous
                    measure. We write that note, then decrement current_count to reflect
                    that note being written."""
                    if self.current_count >= self.max_subdivisions:
                        #print("if")
                        last_measure_remaining_duration = (
                            self.max_subdivisions - remainder
                        )
                        note_to_add_to_old_measure = copy.deepcopy(self.current_note)
                        note_to_add_to_old_measure.dur = last_measure_remaining_duration
                        note_to_add_to_old_measure.tie_start = True
                        #print(note_to_add_to_old_measure)
                        self.current_beat.add_note(note_to_add_to_old_measure)
                        self.current_count -= self.max_subdivisions
                        #print(self.current_count)
                        self.append_and_increment_measure()
                        self.set_current_count_adjacencies()
                        #print("over a measure adj, location {}, note {}, current_measure_floor {}, current_measure_mod {}, current_count {}, max_subdivisions {}".format(location, note, self.current_measure_floor, self.current_measure_mod, self.current_count, self.max_subdivisions))
                        remainder = 0

                    else:
                        #print("else")
                        self.current_beat.add_note(self.current_note)
                        remainder = self.max_subdivisions - self.current_count
                        self.set_current_count_adjacencies()

                # Our current count exceeds the max duration of the current measure
                if (
                    self.current_measure_floor >= 1
                    and self.current_count >= self.max_subdivisions
                ):
                    #print("get_internal_measures, ")
                    # use this to clean up the measures that exist

                    # there is at least one measure to be filled
                    # ie break into measures and beats
                    remainder = self.get_internal_measures()
                    # would need to pass current_beat_count

                if self.current_count > 0:
                    #print("tail, location {}, dur {}, current_count {}".format(location, note.dur, self.current_count))
                    note_to_add_to_old_measure = copy.deepcopy(self.current_note)
                    note_to_add_to_old_measure.dur = self.current_count
                    self.current_beat.add_note(note_to_add_to_old_measure)
                    self.advance_current_beat_count()
                    remainder = self.current_count


        self.current_measure.add_beat(self.current_beat)
        self.current_beat = Beat(self.subdivisions)
        if remainder:
            self.wrap_up(self.max_subdivisions - remainder)
