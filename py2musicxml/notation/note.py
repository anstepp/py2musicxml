"""
The Note object contains and represents notes with pitch and duration.
Pitches are represented in two domains: octave and pitch class. Each
is a separate data member, and can be modified separately. Duration
is one member.

Because the Measure and Part objects contain code to split notes across
measures, you can create a list of Notes objects and not split them for
the measure. This is useful for prototyping.

Users should only need to instantiate a Note object, or use the overloaded 
math operators. To create a note, simply create the object:

>>> middle_C_whole_note = Note(4,4,0)

The Note object overloads operators to allow for comparison of note objects.
There is an attempt to be intutitive. Equality tests for pitches, greater
than/less than test for pitch relationships, and greater than or equal/less
than or equal test for duration relationships. As follows:

note_1 = Note(4,4,0) # Whole note middle C
note_2 = Note(2,4,1) # Half note middle C#

>>> note_1 == note_2 # Middle C is not Middle C#
False
>>> note_1 > note_2 # Middle C is lower than Middle C#
False
>>> note_1 >= note_2 # A whole note is longer than a half note
True

"""

from typing import Tuple

# The Life of a Note

# in a tuplet, we change the subdivision of the beat
# groups of 3 in the space of 2
# grouping of notes other than the subdivision of the meter
# it has to change in the subdivsion, feel of music changes
# how is this unit of time divided, and then subdivided

# when beat is divided by 2, subdivisions are in groups of 2 - simple time
# by 3, compound
# 4 is outgrowth of 2, can be reduced into 2


class Note:
    # default flags for ties & tuplets
    tie_start, tie_continue, tie_end = False, False, False
    tuplet_start, tuplet_continue, tuplet_end = False, False, False
    beam_start, beam_continue = False, False

    # measure defaults
    measure_factor, measure_flag = 1, False

    # chord
    is_chord_member = False

    def __init__(self, duration: int, octave: int, pitch_class: int) -> None:

        self.dur = duration

        # called to correct any errant pitch classes
        self.octave, self.pc = self._fix_pitch_overflow(octave, pitch_class)

        # force starting_pitch to be keyless
        self.step_name, self.alter, self.accidental = self._get_step_name(0)

        self.articulation = None

    def fix_pitch_overflow(self, octave: int, pitch_class: int) -> Tuple[int, int]:
        new_pitch_class, new_octave = None, None

        if pitch_class > 11:
            new_pitch_class = pitch_class % 12
            new_octave = octave + pitch_class // 12
            return new_octave, new_pitch_class

        elif pitch_class < 0:
            new_pitch_class = pitch_class % 12
            new_octave = octave + pitch_class // 12
            return new_octave, new_pitch_class

        else:
            return octave, pitch_class

    def _get_step_name(self, starting_pitch: int) -> Tuple[str, int, str]:
        flat_keys = [1, 3, 5, 8, 10]
        sharp_keys = [2, 4, 6, 7, 9, 11]

        step_names = {}

        if starting_pitch == 0:
            step_names = {
                0: ['C', '0', 'natural'],
                1: ['C', '1', 'sharp'],
                2: ['D', '0', 'natural'],
                3: ['E', '-1', 'flat'],
                4: ['E', '0', 'natural'],
                5: ['F', '0', 'natural'],
                6: ['F', '1', 'sharp'],
                7: ['G', '0', 'natural'],
                8: ['A', '-1', 'flat'],
                9: ['A', '0', 'natural'],
                10: ['B', '-1', 'flat'],
                11: ['B', '0', 'natural'],
            }
        elif starting_pitch in flat_keys:
            step_names = {
                0: ['C', '0', 'natural'],
                1: ['D', '-1', 'flat'],
                2: ['D', '0', 'natural'],
                3: ['E', '-1', 'flat'],
                4: ['E', '0', 'natural'],
                5: ['F', '0', 'natural'],
                6: ['G', '-1', 'flat'],
                7: ['G', '0', 'natural'],
                8: ['A', '-1', 'flat'],
                9: ['A', '0', 'natural'],
                10: ['B', '-1', 'flat'],
                11: ['B', '0', 'natural'],
            }
        elif starting_pitch in sharp_keys:
            step_names = {
                0: ['C', '0', 'natural'],
                1: ['C', '1', 'sharp'],
                2: ['D', '0', 'natural'],
                3: ['D', '1', 'sharp'],
                4: ['E', '0', 'natural'],
                5: ['F', '0', 'natural'],
                6: ['F', '1', 'sharp'],
                7: ['G', '0', 'natural'],
                8: ['G', '1', 'sharp'],
                9: ['A', '0', 'natural'],
                10: ['A', '1', 'sharp'],
                11: ['B', '0', 'natural'],
            }
        else:
            raise Exception('starting_pitch must be zero, a flat key, or sharp key')

        return step_names[self.pc]

    def add_articulation(self, notation: str) -> None:

        """FIX ME: Create possible notation list"""

        self.articulation = notation

    def set_as_tie(self, tie_type: str) -> None:

        if tie_type is 'tie_start':
            self.tie_start = True
        if tie_type is 'tie_continue':
            self.tie_continue = True
            self.articulation = None
        if tie_type is 'tie_end':
            self.tie_end = True
            self.articulation = None

    def __eq__(self, other) -> bool:
        if (
            (self.dur == other.dur)
            and (self.octave == other.octave)
            and (self.pc == other.pc)
        ):
            return True
        else:
            return False

    # Evaluate pitch relative to another

    def __gt__(self, other) -> bool:
        if self.octave > other.octave:
            return True
        elif self.octave == other.octave:
            if self.pc > other.pc:
                return True
            else:
                return False
        else:
            return False

    # Evaluate duration equality

    def __ge__(self, other) -> bool:
        if self.dur > other.dur:
            return True
        else:
            return False

    # Pretty printing in terminal output

    def __str__(self) -> str:
        return 'Duration: {}, Octave: {}, Pitch Class: {}'.format(
            self.dur, self.octave, self.pc
        )
