import itertools
import random


class bangleize:
    def __init__(self):
        pass

    def bjorklund(self, attacks, size):
        unspacedList = []
        returnList = []
        remainder = size - attacks
        for x in range(0, size):
            if x < attacks:
                returnList.append([1])
            else:
                returnList.append([0])

        minimumLength = 0
        listCounter = 0
        tempList = returnList
        while remainder > 1:
            listCounter = 0
            if minimumLength is 0:
                for currentSeries in returnList:
                    if currentSeries[0] is 0 and listCounter < attacks:
                        tempList[listCounter] += currentSeries
                        tempList[tempList.index(currentSeries)] = []
                        listCounter += 1
            else:
                for item in returnList:
                    if len(item) is minimumLength:
                        if len(item) is minimumLength:
                            tempList[listCounter] += item
                            tempList[tempList.index(item)] = []
                            listCounter += 1
            tempList = [x for x in tempList if x != []]
            returnList = tempList
            listCounter = 0
            remainderList = [len(x) for x in returnList]
            minimumLength = min(remainderList)
            counter = 0
            remainderCount = [
                counter + 1 for x in remainderList if x is min(remainderList)
            ]
            remainder = len(remainderList)
        return returnList[0]

    def eSpaced(self, attacks, size, count):
        shortList = self.bjorklund(attacks, size)
        longList = []
        for x in range(0, count):
            longList += shortList
        for location, attack in enumerate(longList):
            if attack is 0:
                longList[location - 1] += 1
        longList = [x for x in longList if x > 0]
        for item in longList:
            if item is 0:
                print(item)
        return longList

    def euclid(self, u, v):
        tempList = list()
        while v > 0:
            if u % v is not 0 and u // v is not 0:
                tempList.append(u // v)
            u, v = v, u % v
        return tempList

    def euclidize(self, theNoteList):
        last = None
        theList = list()
        for item in theNoteList:
            if last is not None:
                theList += self.euclid(last, item.duration)
            last = item.duration
        return theList
