class notePC:
    def __init__(self, octave, pc):
        self.octave = octave
        self.pc = pc
        self.overflowTest()

    """turn into oct.pc format for rtcmix"""

    def makeCmix(self):
        decimal = self.pc / 100.0
        makeNote = self.octave + decimal
        return makeNote

    def overflowTest(self):
        if self.pc > 0:
            newpc = self.pc % 12
            newoctave = self.octave + self.pc // 12
            self.pc = newpc
            self.octave = newoctave
        elif self.pc < 0:
            newpc = self.pc % 12
            newoctave = self.octave - self.pc // 12
            self.pc = newpc
            self.octave = newoctave
