from typing import Tuple

from .utils import fix_pitch_overflow

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
    is_rest = True

    def __init__(self, duration: int, octave: int, pitch_class: int) -> None:

        self.dur = duration

        # called to correct any errant pitch classes
        self.octave, self.pc = fix_pitch_overflow(octave, pitch_class)

        # get these variables upon instantiation in the case the list is acted upon
        self.stepName, self.alter, self.accidental = self._get_step_name(0)

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

    def __eq__(self, other) -> bool:
        if (
            (self.dur == other.dur)
            and (self.octave == other.octave)
            and (self.pc == other.pc)
        ):
            return True
        else:
            return False

    """For the greater than override, we don't care about
    duration. We can easily just compare duration by calling
    note.dur. Pitch is more complicated because of the octave/
    pitch class design."""

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

    def __str__(self) -> str:
        return 'Duration: {}, Octave: {}, Pitch Class: {}'.format(
            self.dur, self.octave, self.pc
        )

