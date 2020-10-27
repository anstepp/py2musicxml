"""
The Measure object generally should not be called by a user.

Measure includes information that py2musicxml uses to keep
track of metric structure. 
"""

import copy

from typing import Iterable, List, Optional, Tuple, Union

from .note import Note
from .beat import Beat
from .rest import Rest


METER_DIVISION_TYPES = {2: "Duple", 3: "Triple", 4: "Quadruple"}


class Measure:

    """
    A class to represent a musical measure.

    Attributes:

    time_signature : Tuple(int, int)
    The time signature for the measure, with the first int representing
    the top note.

    beats : List(float)
    Collection of beat objects

    equal_divisions : bool
    Flag for if the measure is additive meter or not

    measure_number : int
    The measure's index + 1 in a part object.

    meter_division : 
    subdivision of the meter by beat

    meter_type :
    The type of meter: simple, compound, etc

    measure_map : list
    A list of the values of the beats in the measure.

    cumulative_beats: list
    Additive list of the values of the beats in the measure.

    total_cumulative_beats : int
    Total addtitive beat count.

    Methods:
    --------

    is_empty()
    Tests for any beats in self.beats. Returns a bool.

    add_beat(Beat)
    Appends beat to the end of self.beats. You should append Notes to a
    Beat object, then append the Beat object.
    
    """

    def __init__(self, time_signature: Tuple, factor: int):

        """Init a measure with a time signature and factor. This
        sets all the relevant information about a measure.

        Arguments:
        ----------

        time_signature (Time Signature): a Time Signature tuple

        factor (int): unused scaling factor


        """

        self.time_signature = time_signature

        # A Measure contains a list of Beat objects
        self.beats = []

        # default to non-additive meter, this self corrects
        # equal divisions means all beats are the same, eg. 4/4, 6/8, but not 5/8
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
        """Tests for an empty measure.
    
        Arguments:

        None.

        Returns:

        Bool.

        """
        if len(self.beats) == 0:
            return True
        else:
            return False

    def _cumulative_beat_generator(self) -> None:
        """Using the measure map, creates a list of the values for each beat
        that is cummulative. This is used in the Part.get_internal_measures
        method.

        Arguments:

        None

        Returns:

        None

        """
        count = 0
        for beat in self.measure_map:
            count += beat
            yield count

    def add_beat(self, beat: Beat) -> None:
        """
        Add a beat to Measure.Beats, adding the notes inside the beat.

        Arguments:
        ----------

        beat: a Beat object with or without consitiuent notes.

        Returns:

        None

        """
        self.beats.append(beat)

    def _create_measure_map(self, factor: int) -> Tuple[Optional[str], str, List[int]]:
        '''
        1. Determines the measure division and type
            (measure_type will always be Simple, Compound, or Additive)

        2. Creates and returns the measure map.
            measure map is a list of the beat durations in the measure; it maps out the beats of a measure

        Arguments:
        ----------

        factor: scaling factor for the internal notes.

        Returns:

        Tuple

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
            measure_map = self._bjorklund()

        return meter_division, meter_type, measure_map

    def _bjorklund(self, subdivisions: int, divisions: int) -> Tuple:
        """Evenly spaces two numbers that are not divisible by each other

        Arguments:

        subdivisions (int): how many subdivsions in measure

        divisions (int): how many beats/attacks are in measure

        Returns:

        Tuple

        """

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
