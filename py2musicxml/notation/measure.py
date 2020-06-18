import copy

from typing import Iterable, List, Optional, Tuple, Union

from .note import Note
from .beat import Beat
from .rest import Rest


METER_DIVISION_TYPES = {2: "Duple", 3: "Triple", 4: "Quadruple"}


class Measure:
    def __init__(self, time_signature: Tuple, factor: int):

        self.time_signature = time_signature

        # A Measure contains a list of Beat objects
        self.beats = []

        # default to non-additive meter, this self corrects
        # equal divisions means all beats are the same, eg. 4/4, 3/4, but not 5/8
        self.equal_divisions = True

        # Measure number relative to order in Part()
        self.measure_number = None

        # hypermetric weight of measure
        # self.weight = None

        (
            self.meter_division,
            self.meter_type,
            self.measure_map,
        ) = self._create_measure_map(factor)

        self.cumulative_beats = list((x for x in self._cumulative_beat_generator()))
        self.total_cumulative_beats = self.cumulative_beats[-1]
        self.measure_factor = None

    def is_empty(self) -> bool:
        if len(self.beats) == 0:
            return True
        else:
            return False

    def _cumulative_beat_generator(self) -> None:
        count = 0
        for beat in self.measure_map:
            count += beat
            yield count

    def add_beat(self, beat: Beat) -> None:
        self.beats.append(beat)

    def _create_measure_map(self, factor: int) -> Tuple[Optional[str], str, List[int]]:
        '''
        1. Determines the measure division and type
            (measure_type will always be Simple, Compound, or Additive)

        2. Creates the measure map.
            measure map is a list of the beat durations in the measure; it maps out the beats of a measure
        '''

        meter_division = None
        meter_type = None
        measure_map = []

        if self.equal_divisions:

            # time sig denominator is divisible by 3
            if ((self.time_signature[0] % 3) == 0) and (self.time_signature[0] > 3):

                beats_in_measure = int(self.time_signature[0] / 3)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Compound"
                measure_map = [factor * 1.5 for x in range(beats_in_measure)]

            # time sig denominator is divisible by 2
            elif self.time_signature[1] % 2 == 0:

                beats_in_measure = self.time_signature[0]

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [factor for x in range(beats_in_measure)]

            # time sig denominator is not divisible by 2 or 3
            else:
                self.equal_divisions = False

                # meter_division remains None
                meter_type = "Additive"
                measure_map = self.bjorklund(
                    self.time_signature[1], self.time_signature[0]
                )
        else:
            # meter_division remains None
            meter_type = "Additive"
            measure_map = self.bjorklund()

        return meter_division, meter_type, measure_map

    def bjorklund(self, subdivisions: int, divisions: int) -> Tuple:
        '''Evenly spaces two numbers that are not divisible by each other'''

        return_list = []
        remainder = subdivisions - divisions

        return_list = [1 for x in range(divisions)] + [
            0 for x in range(subdivisions - divisions)
        ]

        minimum_length = 0
        list_counter = 0
        temp_list = return_list
        while remainder > 1:
            list_counter = 0
            if minimum_length == 0:
                if list_counter < divisions:
                    temp_list[list_counter] += 1
                    list_counter += 1
            else:
                for item in return_list:
                    if len(item) is minimum_length:
                        if len(item) is minimum_length:
                            temp_list[list_counter] += item
                            temp_list[temp_list.index(item)] = []
                            list_counter += 1
            temp_list = [x for x in temp_list if x != []]
            return_list = temp_list
            list_counter = 0
            counter = 0

        measure_map = (2, 3)
        return measure_map
