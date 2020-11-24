import copy
import itertools

from typing import Iterable, List, Optional, Tuple, Union

from .note import Note
from .beat import Beat
from .rest import Rest


METER_DIVISION_TYPES = {2: "Duple", 3: "Triple", 4: "Quadruple"}
TimeSignature = Tuple[int, int]


class Measure:
    def __init__(self, time_signature: Tuple, factor: int):

        self.time_signature = time_signature

        self.notes = []

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

    def add_note(self, note: Note) -> None:
        self.notes.append(note)

    def add_beat(self, beat: Beat) -> None:
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

            elif ((self.time_signature[0] % 2) == 0) and (self.time_signature[0] > 2):

                beats_in_measure = self.time_signature[0]

                #print("Duple", beats_in_measure)

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

    def clean_up_measure(self) -> None:
        """
        Called to group beats in measure and check ties and accidentals.

        Arguments:
        ----------

        None

        Returns:
        --------

        None
        """

        notes = self.notes
        notes.reverse()
        beats = self.cumulative_beats
        beats.reverse()
        if notes and beats:
            current_count = 0
            current_note = notes.pop()
            beat_breakpoint = beats.pop()
            print("init bp", beat_breakpoint)
            current_beat = Beat(beat_breakpoint)
            old_dur = 0
            note_for_next_beat = None

            # break 

            print("pre-loop", current_note, beat_breakpoint)

            while beats and notes:

                print('new breakpoint', beat_breakpoint)

                # check for multi-beat note
                if current_note.dur in self.cumulative_beats:
                    print('it worked')

                # cleanup any leftover note stuff from the last iteration
                if note_for_next_beat:
                    beat_breakpoint = beats.pop()
                    current_beat = Beat(beat_breakpoint)
                    current_beat.add_note(note_for_next_beat)
                    note_for_next_beat = None
                    self.add_beat(current_beat)
                else:
                    self.add_beat(current_beat)
                    beat_breakpoint = beats.pop()
                    current_beat = Beat(beat_breakpoint)

                # keep adding notes until we hit or break the breakpoint
                while current_count < beat_breakpoint:
                    old_dur = current_note.dur
                    current_beat.add_note(current_note)
                    if notes:
                        current_note = notes.pop()
                        current_count += current_note.dur
                    else:
                        break
                    self.add_beat(current_beat)

                # add note and beat as we equal the breakpoint
                if current_count == beat_breakpoint:
                    print('equal', current_count, beat_breakpoint)
                    old_dur = current_note.dur
                    current_beat.add_note(current_note)
                    beat_breakpoint = beats.pop()
                    current_beat = Beat(beat_breakpoint)

                # divide note into two parts - one for current beat, one for next beat
                elif current_count > beat_breakpoint:

                    print("current count", current_count, 'beat_breakpoint', beat_breakpoint)

                    overflow = current_note.dur - beat_breakpoint
                    remainder = beat_breakpoint - old_dur
                    old_beat_note = copy.deepcopy(current_note)
                    old_beat_note.dur = remainder
                    old_beat_note.tie_start = True
                    current_beat.add_note(old_beat_note)
                    note_for_next_beat = copy.deepcopy(current_note)
                    note_for_next_beat.dur = overflow
                    old_dur = overflow

                else:
                    # eventually throw error
                    pass

                if notes:
                    current_note = notes.pop()
                    current_count += current_note.dur


        [beat.make_beams() for beat in self.beats]

