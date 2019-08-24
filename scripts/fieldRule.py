import random


class rule:
    def __init__(self, three, two, testVal):
        self.two = two
        self.three = three
        self.test = testVal

    def getValues(self, inputChar):
        flip = random.random()
        if flip > self.test:
            returnList = list()
            returnList.append(inputChar)
            returnList.append(inputChar + self.three)
            returnList.append(inputChar)
            return returnList
        else:
            returnList = list()
            returnList.append(inputChar)
            returnList.append(inputChar + self.two)
            return returnList
