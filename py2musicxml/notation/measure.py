"""
The Measure object generally should not be called by a user.

Measure includes information that py2musicxml uses to keep
track of metric structure. 
"""

import copy
import logging

from typing import Iterable, List, Optional, Tuple, Union

from .note import Note
from .beat import Beat
from .rest import Rest

measure_logger = logging.getLogger('Measure').setLevel(logging.INFO)

METER_DIVISION_TYPES = {2: "Duple", 3: "Triple", 4: "Quadruple"}
TimeSignature = Tuple[int, int]


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
        logging.debug(f"Appending beat and len: {beat} {len(beat.notes)}")

        self.beats.append(beat)

    def set_time_signature(self, time_signature: TimeSignature) -> None:
        """For future use - eventally this should trigger a cascade
        measure rewrite in a part object that contains the re-sig'd 
        measure.
        
        This should also consider allowing a rewrite of just the measure
        with rests to fill, or deletion of notes.
        """

        self.time_signature = time_signature
        self._create_measure_map(1)

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

                #print("Triple", beats_in_measure)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Compound"
                measure_map = [factor * 1.5 for x in range(beats_in_measure)]

            # time sig denominator is divisible by 4, but not 2
            elif ((self.time_signature[0] % 4) == 0) and (self.time_signature[0] > 2):

                beats_in_measure = self.time_signature[0]

                #print("Quadruple", beats_in_measure)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [factor for x in range(beats_in_measure)]

            elif ((self.time_signature[0] % 2) == 0):

                beats_in_measure = self.time_signature[0]

                #print("Duple", beats_in_measure)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [factor for x in range(beats_in_measure)]

            elif self.time_signature[0] == 3:

                beats_in_measure = self.time_signature[0]

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [factor for x in range(beats_in_measure)]

            # time sig denominator is not divisible by 2 or 3
            else:
                #print("non div")
                self.equal_divisions = False

                beats_in_measure = self.time_signature[0]

                denominator = self.time_signature[1]

                if denominator > 4:
                    scale = (denominator / 4)
                else:
                    scale = 1

                # meter_division remains None
                meter_type = "Additive"
                measure_map = [factor / scale for x in range(beats_in_measure)]
        else:
            #print("bail out")
            # meter_division remains None
            meter_type = "Additive"
            

        return meter_division, meter_type, measure_map

    def _front_load_measure(self, subdivisions: int, divisions: int):
        '''front loads divisions on two numbers that are not divisible by each other'''

        return_list = [1 for x in range(divisions)]
        remainder = subdivisions - divisions

        idx = 0

        while remainder > 0:
            #print("_front_load_measure, remainder", remainder)
            return_list[idx] += 1
            idx = (idx + 1) % len(return_list)
            remainder -= 1

        return return_list
