import notePC as NPC
import random
import fieldRule as R  # three, two, testVal
from itertools import cycle


class pitchField:
    def __init__(self, rule, startingPitch, test):
        self.rule = rule
        self.test = test
        self.rules = list()
        self.startingPitch = startingPitch

    def stripNote(self, inNote):
        octave = int(inNote)
        pc = (inNote % 1) * 100
        return octave, pc

    def overflowTest(self, inNote):
        octave, noteToFix = self.stripNote(inNote)
        if noteToFix > 11:
            fixedNote = noteToFix - 12
            return (octave + 1) + (fixedNote / 100)
        elif noteToFix < 0:
            fixedNote = noteToFix + 12
            return (octave - 1) + (fixedNote / 100)
        else:
            return inNote

    def makeField(self):
        pitchField = list()
        if isinstance(self.rule, list):
            cycleMe = cycle(self.rule)
            currentPitch = self.startingPitch
            while currentPitch < 10.12:
                pitchField.append(currentPitch)
                currentPitch += next(cycleMe) * 0.01
                currentPitch = self.overflowTest(currentPitch)
        elif isinstance(self.rule, str):
            theRule = list()
            for item in self.rule:
                try:
                    x = int(item)
                    theRule.append(x)
                except ValueError:
                    pass
            cycleMe = cycle(theRule)
            currentPitch = self.startingPitch
            while currentPitch < 12.12:
                pitchField.append(currentPitch)
                currentPitch += next(cycleMe) * 0.01
                currentPitch = self.overflowTest(currentPitch)
        return pitchField

    def makeRules(self, fieldRules):
        # set number of rules to be equal to field rules
        systemRules = len(fieldRules)
        for i in range(0, systemRules):
            x = R.rule(random.randint(1, 4), random.randint(-3, -1), self.test)
            self.rules.append(x)

    def makeFieldGen(self, string, gens):
        nextGen = list()
        for current in string:
            currentRule = self.rules[current]
            theString = currentRule.getValues(current)
            for item in theString:
                nextGen.append(item)


# x = pitchField([2, 3, 1, 2], NPC.notePC(1, 0), 0.5)
# y = x.makeField()
# for it in y:
# 	print(y)
# x.makeRules([4,8,12,14])
# x.makeFieldGen([3,],3)
# thing = x.makeFieldGen([0,], 4)
# print(thing)
