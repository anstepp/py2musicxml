import note
from pitchMath import convertToXML
from lxml import etree
import copy

class noteList:
    def __init__(self, theList):
        self.initalList = None
        self.measureFactor = None
        self.measureBeats = None
        self.currentList = theList
        self.finalList = None

    # is this redundant with the cleanList(), or do we make that default beahvior?
    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""
    def getList(self, **kwargs):
        if kwargs.get("factor"):
            self.measureFactor = kwargs.get("factor")
        else:
            self.measureFactor = 1
        if kwargs.get("beats"):
            self.measureBeats = kwargs.get("beats")
        else:
            self.measureBeats = 4
        if kwargs.get("how"):
            noteSortMethod = kwargs.get("how")
        else:
            noteSortMethod = "Default"
        self.cleanList(noteSortMethod)

    def cleanList(self, how):
        if how is "Implied":
            self.finalList = self.groupByImpliedMeter()
        if how is "Map":
            self.finalList = self.groupByMap()
        # default to 4/4
        if how is "Default":
            self.finalList = self.groupList()
        else:
            self.finalList = self.groupList()


    def groupList(self):
        currentCount = 0
        returnList = []
        subdivisions = self.measureFactor * self.measureBeats
        # print(subdivisions)
        for location, item in enumerate(self.currentList):
            currentCount += item.dur
            # print("currentCount", currentCount)
            if currentCount == subdivisions:
                if location != len(self.currentList) - 1:
                    self.currentList[location + 1].measureFlag = True
                alteredDuration = copy.deepcopy(self.currentList[location])
                alteredDuration.dur = alteredDuration.dur / self.measureFactor
                returnList.append(alteredDuration)
                currentCount = 0
            elif currentCount > subdivisions:
                currentNote = copy.deepcopy(self.currentList[location])
                # print("logic for ties", currentCount, subdivisions)
                overflow = currentCount - subdivisions
                # print("overflow", overflow)
                preTie = self.currentList[location].dur - overflow
                # print("pre-tie", preTie)
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

    def groupByImpliedMeter(self):
        pass
        """eventually, group measures by emphasis of rhythm and pitch
        this might have to find a way to work between two different
        pitch class objects to create a list of interactions. Not
        sure what to do yet. There also needs to be a way to pass
        the measure information onto the XML parser."""

    """this method is designed to take an input map to allow
    for various time signatures being user defined, or to 
    have different proportions per measure.
    It may not work yet."""

    def groupByMap(self, inputMap):
        mapToGroup = Map
        for mapValue in mapToGroup:
            currentBeats = mapValue[0]
            currentMultiplier = mapValue[1]
            subdivisions = currentBeats * currentMultiplier
            for location, item in enumerate(self.currentList):
                currentCount += item.dur
                # print("currentCount", currentCount)
                if currentCount == subdivisions:
                    if location != len(currentList) - 1:
                        self.currentList[location + 1].measureFlag = True
                    alteredDuration = copy.deepcopy(self.currentList[location])
                    alteredDuration.dur = alteredDuration.dur / currentMultiplier
                    returnList.append(alteredDuration)
                    currentCount = 0
                elif currentCount > subdivisions:
                    currentNote = copy.deepcopy(self.currentList[location])
                    # print("logic for ties", currentCount, subdivisions)
                    overflow = currentCount - subdivisions
                    # print("overflow", overflow)
                    preTie = self.currentList[location].dur - overflow
                    # print("pre-tie", preTie)
                    currentNote.dur = preTie / currentMultiplier
                    currentNote.tieStart = True
                    returnList.append(currentNote)
                    # there should probably be a "no accidental" flag, too
                    tiedNote = copy.deepcopy(self.currentList[location])
                    tiedNote.dur = overflow / measureFactor
                    tiedNote.tieEnd = True
                    tiedNote.measureFlag = True
                    returnList.append(tiedNote)
                    currentCount = overflow
                else:
                    alteredDuration = copy.deepcopy(self.currentList[location])
                    alteredDuration.dur = alteredDuration.dur / currentMultiplier
                    returnList.append(alteredDuration)
        return returnList
