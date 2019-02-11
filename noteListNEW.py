import note


class noteList:
    def __init__(self):
        self.initalList = None
        self.measureFactor = None
        self.measureBeats = None
        self.currentList = None
        self.finalList = None

    def getList(self, inputList, factor, beats):
        self.measureFactor = factor
        self.measureBeats = beats
        self.currentList = inputList
        self.finalList = groupList()

    def groupList(self):
        currentCount = 0
        returnList = []
        subdivisions = self.measureFactor * self.measureBeats
        print(subdivisions)
        for location, item in enumerate(self.currentList):
            currentCount += item.dur
            print("currentCount", currentCount)
            if currentCount == subdivisions:
                if location != len(currentList) - 1:
                    self.currentList[location + 1].measureFlag = True
                alteredDuration = copy.deepcopy(self.currentList[location])
                alteredDuration.dur = alteredDuration.dur / self.measureFactor
                returnList.append(alteredDuration)
                currentCount = 0
            elif currentCount > subdivisions:
                currentNote = copy.deepcopy(self.currentList[location])
                print("logic for ties", currentCount, subdivisions)
                overflow = currentCount - subdivisions
                print("overflow", overflow)
                preTie = self.currentList[location].dur - overflow
                print("pre-tie", preTie)
                currentNote.dur = preTie / self.measureFactor
                currentNote.tieStart = True
                returnList.append(currentNote)
                tiedNote = copy.deepcopy(self.currentList[location])
                tiedNote.dur = overflow / measureFactor
                tiedNote.tieEnd = True
                tiedNote.measureFlag = True
                returnList.append(tiedNote)
                currentCount = overflow
            else:
                alteredDuration = copy.deepcopy(self.currentList[location])
                alteredDuration.dur = alteredDuration.dur / self.measureFactor
                returnList.append(alteredDuration)
        return returnList
