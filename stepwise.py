import random
from itertools import cycle, dropwhile, islice

from py2musicxml import Pitch


class grammar:
    def __init__(self, testVal, seed, tonic):
        self.R1 = random
        self.R2 = random
        self.R3 = random
        self.R4 = random
        self.R5 = random
        self.R6 = random
        self.R7 = random
        self.testVal = testVal
        self.tonic = tonic
        """get test targets set to starting pitch"""
        diatonic = [0, 2, 4, 5, 7, 9, 11]
        self.pitchedDiatonic = list()
        for item in diatonic:
            self.pitchedDiatonic.append(self.targetOverflowTest(item + self.tonic))
        self.cycledDiatonic = cycle(self.pitchedDiatonic)
        self.reversedCycledDiatonic = cycle(reversed(self.pitchedDiatonic))
        self.target1 = self.targetOverflowTest(0 + self.tonic)
        self.target2 = self.targetOverflowTest(2 + self.tonic)
        self.target3 = self.targetOverflowTest(4 + self.tonic)
        self.target4 = self.targetOverflowTest(5 + self.tonic)
        self.target5 = self.targetOverflowTest(7 + self.tonic)
        self.target6 = self.targetOverflowTest(9 + self.tonic)
        self.target7 = self.targetOverflowTest(11 + self.tonic)
        """Make rules - these are in steps not absolute values"""
        self.A1R1 = 1
        self.A1R2 = -2
        self.A2R1 = 1
        self.A2R2 = -2
        self.A3R1 = 1
        self.A3R2 = -2
        self.A4R1 = 1
        self.A4R2 = -2
        self.A5R1 = 1
        self.A5R2 = -2
        self.A6R1 = 1
        self.A6R2 = -2
        self.A7R1 = 1
        self.A7R2 = -2

    def setRules(self, **args):
        if len(args) is 2:
            self.A1R1, self.A2R1, self.A3R1, self.A4R1, self.A5R1, self.A6R1, self.A7R1 = args[
                0
            ]
            self.A1R2, self.A2R2, self.A3R2, self.A4R2, self.A5R2, self.A6R2, self.A7R2 = args[
                1
            ]
        if len(args) is 14:
            self.A1R1 = args[0]
            self.A1R2 = args[1]
            self.A2R1 = args[2]
            self.A2R2 = args[3]
            self.A3R1 = args[4]
            self.A3R2 = args[5]
            self.A4R1 = args[6]
            self.A4R2 = args[7]
            self.A5R1 = args[8]
            self.A5R2 = args[9]
            self.A6R1 = args[10]
            self.A6R2 = args[11]
            self.A7R1 = args[12]
            self.A7R2 = args[13]
        else:
            # FIXME: make error handling event
            pass

    def targetOverflowTest(self, inNote):
        if inNote > 11:
            fixedPC = inNote - 12
            return fixedPC
        elif inNote < 0:
            fixedPC = inNote + 12
            return fixedPC
        else:
            return inNote

    def overflowTest(self, inNote):
        if inNote.pc > 11:
            fixedPC = inNote.pc - 12
            fixedNote = Pitch(inNote.octave, fixedPC)
            return fixedNote
        elif inNote.pc < 0:
            fixedPC = inNote.pc + 12
            fixedNote = Pitch(inNote.octave, fixedPC)
            return fixedNote
        else:
            return inNote

    def getAbsPitch(self, current, motion):
        if motion >= 0:
            step = motion
            startRight = dropwhile(lambda x: x != current, self.cycledDiatonic)
            intermediateList = islice(startRight, None, step + 1)
            finalList = list(intermediateList)
            finalValue = finalList[len(finalList) - 1]
            finalList.pop(0)
            if min(self.pitchedDiatonic) in finalList:
                return 1, finalValue
            else:
                return 0, finalValue
        else:
            step = abs(motion)
            startLeft = dropwhile(lambda x: x != current, self.reversedCycledDiatonic)
            intermediateList = islice(startLeft, None, step + 1)
            finalList = list(intermediateList)
            finalValue = finalList[len(finalList) - 1]
            finalList.pop(0)
            if max(self.pitchedDiatonic) in finalList:
                return -1, finalValue
            else:
                return 0, finalValue

    def nextStepwiseGen(self, string):
        # print string
        newGeneration = list()
        for current in string:
            if current.pc == self.target1:
                flip = self.R1.random()
                # print current.pc, self.target1
                if flip > self.testVal:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A1R1)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote, current]
                else:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A1R2)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote]
            if current.pc == self.target2:
                flip = self.R2.random()
                # print current.pc, self.target2
                if flip > self.testVal:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A2R1)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote, current]
                else:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A2R2)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote]
            if current.pc == self.target3:
                flip = self.R3.random()
                # print current.pc, self.target3
                if flip > self.testVal:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A3R1)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote, current]
                else:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A3R2)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote]
            if current.pc == self.target4:
                flip = self.R4.random()
                # print current.pc, self.target4
                if flip > self.testVal:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A4R1)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote, current]
                else:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A4R2)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote]
            if current.pc == self.target5:
                flip = self.R5.random()
                # print current.pc, self.target5
                if flip > self.testVal:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A5R1)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote, current]
                else:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A5R2)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote]
            if current.pc == self.target6:
                flip = self.R6.random()
                # print current.pc, self.target6
                if flip > self.testVal:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A6R1)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote, current]
                else:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A6R2)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote]
            if current.pc == self.target7:
                flip = self.R7.random()
                # print current.pc, self.target7
                if flip > self.testVal:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A7R1)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote, current]
                else:
                    octaveFlag, thePC = self.getAbsPitch(current.pc, self.A7R2)
                    stage1 = Pitch(current.octave + octaveFlag, thePC)
                    newNote = self.overflowTest(stage1)
                    newGeneration += [current, newNote]
        return newGeneration

    def makeSystem(self, start, generations):
        lastGen = start
        for i in range(generations):
            currentGen = self.nextStepwiseGen(lastGen)
            lastGen = currentGen
        return currentGen
