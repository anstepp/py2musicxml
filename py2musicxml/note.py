from .noteRhythm import noteRhythm
from .notePC import notePC

# the life of a note

# in a tuplet, we change the subdivision of the beat
# groups of 3 in the space of 2
# grouping of notes other than the subdivision of the meter
# it has to change in the subdivsion, feel of music changes
# how is this unit of time divided, and then subdivided

# when beat is divided by 2, subdivisions are in groups of 2 - simple time
# by 3, compound
# 4 is outgrowth of 2, can be reduced into 2


class Note(noteRhythm, notePC):
    # default flags for ties & tuplets
    tieStart, tieContinue, tieEnd = False, False, False
    tupletStart, tupletContinue, tupletEnd = False, False, False

    # measure defaults
    measureFactor, measureFlag = 1, False

    def __init__(self, r, octave, pc):
        self.dur, self.octave, self.pc = r, octave, pc

        # called to correct any errant pitch classes
        self.overflowTest()

        # get these variables upon instantiation in the case the list is acted upon
        self.stepName, self.alter, self.accidental = self._get_step_name(0)

    #  # Needs a way to be able to make a note given a note rhythm and pitch class
    # @classmethod
    #  def initFromList(cls, noteRhythm, notePC):
    #      dur = noteRhythm.dur
    #      octave = notePC.octave
    #      pc = notePC.pc
    #      return cls(dur, octave, pc)

    def _get_step_name(self, starting_pitch):
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

    def make_octave_pc(self):
        raise Exception('self.pitch is not defined anywhere yet')
        octave = int(self.pitch)
        floatPC = self.pitch % 1
        pc = int(round(floatPC, 2) * 100)
        return octave, pc
