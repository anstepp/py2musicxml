from noteRhythm import noteRhythm
from notePC import notePC
from math import ceil


class note(noteRhythm, notePC):
    def __init__(self, r, octave, pc):
        notePC.__init__(self, octave, pc)
        noteRhythm.__init__(self, dur=r)
        self.dur = r
        self.octave = octave
        self.pitch = pc
        # flags for ties
        self.tieStart = False
        self.tieContinue = False
        self.tieEnd = False
        # flags for tuplets
        self.tupletStart = False
        self.tupletContinue = False
        self.tupletEnd = False
        self.overflowTest()

    @classmethod
    def initFromList(cls, r, octave, pc):
        self.dur = r
        self.octave = octave
        self.pitch = pc
        self.overflowTest()

    def overflowTest(self):
        if self.pc > 0:
            self.pc = self.pc % 12
            self.octave = self.octave + self.pc // 12
        elif self.pc < 0:
            self.pc = 12 - self.pc % 12
            self.octave = self.octave - self.pc // 12
            pass


# the life of a note

# in a tuplet, we change the subdivision of the beat
# groups of 3 in the space of 2
# grouping of notes other than the subdivision of the meter
# it has to change in the subdivsion, feel of music changes
# how is this unit of time divided, and then subdivided

# when beat is divided by 2, subdivisions are in groups of 2 - simple time
# by 3, compound
# 4 is outgrowth of 2, can be reduced into 2
#


# pc - pitch class


class note(noteRhythm, notePC):
    duration = None
    octave = None
    pitch = None

    # flags for ties
    tieStart = False
    tieContinue = False
    tieEnd = False

    # flags for tuplets
    tupletStart = False
    tupletContinue = False
    tupletEnd = False

    def __init__(self, duration, octave, pitch):

        notePC.__init__(self, octave, pitch)

        noteRhythm.__init__(self, dur=duration)

        self.duration = duration
        self.octave = octave
        self.pitch = pitch

    def makeOctavePC(self):
        octave = int(self.pitch)
        floatPC = self.pitch % 1
        pc = int(round(floatPC, 2) * 100)
        return octave, pc
