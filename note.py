from noteRhythm import noteRhythm
from notePC import notePC
from math import ceil


class note(noteRhythm, notePC):
    def __init__(self, r, octave, pc):
        # notePC.__init__(self, octave, pc)
        # noteRhythm.__init__(self, dur=r)
        self.dur = r
        self.octave = octave
        self.pc = pc
        # flags for ties
        self.tieStart = False
        self.tieContinue = False
        self.tieEnd = False
        # flags for tuplets
        self.tupletStart = False
        self.tupletContinue = False
        self.tupletEnd = False
        self.measureFactor = 1
        self.measureFlag = False
        self.overflowTest()
        self.stepName, self.alter, self.accidental = self.getNoteName(0)

    @classmethod
    def initFromList(cls, noteRhythm, notePC):
        dur = noteRhythm.dur
        octave = notePC.octave
        pc = notePC.pc
        return cls(dur, octave, pc)

    def getNoteName(self, startingPitch):
        flatKeys = [1, 3, 5, 8, 10]
        sharpKeys = [2, 4, 6, 7, 9, 11]
        if startingPitch is 0:
            if self.pc == 0:
                return ["C", "0", "natural"]
            elif self.pc == 1:
                return ["C", "1", "sharp"]
            elif self.pc == 2:
                return ["D", "0", "natural"]
            elif self.pc == 3:
                return ["E", "-1", "flat"]
            elif self.pc == 4:
                return ["E", "0", "natural"]
            elif self.pc == 5:
                return ["F", "0", "natural"]
            elif self.pc == 6:
                return ["F", "1", "sharp"]
            elif self.pc == 7:
                return ["G", "0", "natural"]
            elif self.pc == 8:
                return ["A", "-1", "flat"]
            elif self.pc == 9:
                return ["A", "0", "natural"]
            elif self.pc == 10:
                return ["B", "-1", "flat"]
            elif self.pc == 11:
                return ["B", "0", "natural"]
            else:
                print("Note out of bounds - this could be a problem.", self.pc)
                return [None, None, None]
        if startingPitch in flatKeys:
            if self.pc == 0:
                return ["C", "0", "natural"]
            elif self.pc == 1:
                return ["D", "-1", "flat"]
            elif self.pc == 2:
                return ["D", "0", "natural"]
            elif self.pc == 3:
                return ["E", "-1", "flat"]
            elif self.pc == 4:
                return ["E", "0", "natural"]
            elif self.pc == 5:
                return ["F", "0", "natural"]
            elif self.pc == 6:
                return ["G", "-1", "flat"]
            elif self.pc == 7:
                return ["G", "0", "natural"]
            elif self.pc == 8:
                return ["A", "-1", "flat"]
            elif self.pc == 9:
                return ["A", "0", "natural"]
            elif self.pc == 10:
                return ["B", "-1", "flat"]
            elif self.pc == 11:
                return ["B", "0", "natural"]
            else:
                print("Note out of bounds - this could be a problem.")
                return [None, None, None]
        if startingPitch in sharpKeys:
            if self.pc == 0:
                return ["C", "0", "natural"]
            elif self.pc == 1:
                return ["C", "1", "sharp"]
            elif self.pc == 2:
                return ["D", "0", "natural"]
            elif self.pc == 3:
                return ["D", "1", "sharp"]
            elif self.pc == 4:
                return ["E", "0", "natural"]
            elif self.pc == 5:
                return ["F", "0", "natural"]
            elif self.pc == 6:
                return ["F", "1", "sharp"]
            elif self.pc == 7:
                return ["G", "0", "natural"]
            elif self.pc == 8:
                return ["G", "1", "sharp"]
            elif self.pc == 9:
                return ["A", "0", "natural"]
            elif self.pc == 10:
                return ["A", "1", "sharp"]
            elif self.pc == 11:
                return ["B", "0", "natural"]
            else:
                print("Note out of bounds - this could be a problem.")
                return [None, None, None]

    def makeOctavePC(self):
        octave = int(self.pitch)
        floatPC = self.pitch % 1
        pc = int(round(floatPC, 2) * 100)
        return octave, pc


# the life of a note

# in a tuplet, we change the subdivision of the beat
# groups of 3 in the space of 2
# grouping of notes other than the subdivision of the meter
# it has to change in the subdivsion, feel of music changes
# how is this unit of time divided, and then subdivided

# when beat is divided by 2, subdivisions are in groups of 2 - simple time
# by 3, compound
# 4 is outgrowth of 2, can be reduced into 2
