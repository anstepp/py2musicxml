import copy
import fractions

from functools import reduce
from lxml import etree

from .pitchMath import convertToXML

DEFAULT_MEASURE_BEATS = 4
DEFAULT_MEASURE_FACTOR = 1


class NoteList:
    measureFactor, measureBeats = None, None
    initalList, currentList, finalList = None, None, None

    def __init__(self, theList):
        self.currentList = theList
        self.subdivisions = None
    # is this redundant with the _clean_list(), or do we make that default beahvior?
    """default behavior is to simply clean an input list to 4/4
       it's also an option to feed extra arguments with keywords to 
       modify behavior for optional cleaning methods or user choices
       for measure groupings of factors"""

    def getList(self, **kwargs):

        self.measureFactor = (
            kwargs.get("factor") if kwargs.get("factor") else DEFAULT_MEASURE_FACTOR
        )

        self.measureBeats = (
            kwargs.get("beats") if kwargs.get("beats") else DEFAULT_MEASURE_BEATS
        )

        noteSortMethod = kwargs.get("how") if kwargs.get("how") else "Default"

        self._clean_list(noteSortMethod)

    def _clean_list(self, how):
        if how is "Implied":
            self.finalList = self.groupByImpliedMeter()
        if how is "Map":
            self.finalList = self.groupByMap()
        # default to 4/4
        if how is "Default":
            self.finalList = self.groupList()
        else:
            self.finalList = self.groupList()

    def gcd(self, a, b):
        if type(a) and type(b) is int:
            while b:
                a, b = b, a % b
            return a
        else:
            # convert float to fraction by approximating denominator then gcd
            return fractions.gcd(
                fractions.Fraction(a).limit_denominator(),
                fractions.Fraction(b).limit_denominator(),
            )

    def lcm(self, a, b):
        return a * b // self.gcd(a, b)

    def getUniques(self, theList):
        uniques = []
        for item in theList:
            if item.dur not in uniques:
                uniques.append(item.dur)
            else:
                pass
        return uniques

    def groupList(self):
        currentCount = 0
        # current count of number of self.subdivisions including the new note (item)
        lastCurrentCount = 0
        middleList = []
        returnList = []
        self.subdivisions = self.measureBeats * self.measureFactor

        for location, item in enumerate(self.currentList):
            currentCount += item.dur
            currentCountFloor = currentCount // self.subdivisions
            currentCountMod = currentCount % self.subdivisions
            if currentCountMod == 0 and currentCountFloor == 1:
                #print("zero, equal")
                if location != len(self.currentList) - 1:
                    self.currentList[location + 1].measureFlag = True
                if item.dur > self.subdivisions:
                    how_many_measures = currentCount // self.subdivisions
                    what_goes_to_the_first_measure = (
                        item.dur - currentCount // self.subdivisions
                    )
                    last_note_of_old_measure = copy.deepcopy(self.currentList[location])
                    last_note_of_old_measure.dur = what_goes_to_the_first_measure
                    last_note_of_old_measure.tieStart = True
                    middleList.append(last_note_of_old_measure)
                    while how_many_measures > 0:
                        whole_measure_note = copy.deepcopy(self.currentList[location])
                        whole_measure_note.dur = self.subdivisions
                        if how_many_measures > 1:
                            whole_measure_note.tieStart = True
                        else:
                            whole_measure_note.tieEnd = True
                        middleList.append(whole_measure_note)
                        how_many_measures -= 1
                else:
                    alteredDuration = copy.deepcopy(self.currentList[location])
                    middleList.append(alteredDuration)
                currentCount = 0
            elif currentCountMod == 0 and currentCountFloor > 1:
                #print("zero, greater than")
                how_many_measures = currentCount // self.subdivisions
                if location != len(self.currentList) - 1:
                    self.currentList[location + 1].measureFlag = True
                how_many_measures = currentCount // self.subdivisions - 1
                what_goes_to_the_first_measure = (
                    item.dur - self.subdivisions * how_many_measures
                )
                last_note_of_old_measure = copy.deepcopy(self.currentList[location])
                last_note_of_old_measure.dur = what_goes_to_the_first_measure
                last_note_of_old_measure.tieStart = True
                middleList.append(last_note_of_old_measure)
                while how_many_measures > 0:
                    note_to_add = copy.deepcopy(self.currentList[location])
                    note_to_add.dur = self.subdivisions
                    note_to_add.measureFlag = True
                    middleList.append(note_to_add)
                    how_many_measures -= 1
                lastCurrentCount = currentCountMod
                currentCount = 0
            elif currentCountMod > 0 and currentCountFloor == 1:
                #print("greater than, zero")
                currentNote = copy.deepcopy(self.currentList[location])
                overflow = currentCount - self.subdivisions
                if overflow // self.subdivisions > 1:
                    newDur = self.subdivisions
                    currentNote.dur = newDur
                    currentNote.tieStart = True
                    middleList.append(currentNote)
                    tiedNote = copy.deepcopy(self.currentList[location])
                    tiedDur = overflow % self.subdivisions
                    tiedNote.dur = newDur
                    tiedNote.tieEnd = True
                    tiedNote.measureFlag = True
                    middleList.append(tiedNote)
                else:
                    preTie = self.currentList[location].dur - overflow
                    newDur = preTie
                    currentNote.dur = newDur
                    currentNote.tieStart = True
                    middleList.append(currentNote)
                    tiedNote = copy.deepcopy(self.currentList[location])
                    tiedDur = overflow % self.subdivisions
                    tiedNote.dur = tiedDur
                    tiedNote.tieEnd = True
                    tiedNote.measureFlag = True
                    middleList.append(tiedNote)
                lastCurrentCount = currentCount % self.subdivisions
                currentCount = overflow
            elif currentCountMod > 0 and currentCountFloor > 1:
                #print("greater than, greater than")
                currentNote = copy.deepcopy(self.currentList[location])
                last_measure_count = self.subdivisions - lastCurrentCount
                overflow = currentCountMod
                if last_measure_count > 0:
                    how_many_measures = currentCount // self.subdivisions - 1
                    what_goes_to_the_first_measure = self.subdivisions - lastCurrentCount
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = self.subdivisions * how_many_measures
                else:
                    how_many_measures = currentCount // self.subdivisions
                    what_goes_to_the_first_measure = False
                    what_goes_to_the_last_measure = overflow
                    extra_measure_beats = self.subdivisions * how_many_measures
                if what_goes_to_the_first_measure:
                    currentNote = copy.deepcopy(self.currentList[location])
                    currentNote.dur = what_goes_to_the_first_measure
                    currentNote.tieStart = True
                    middleList.append(currentNote)
                while how_many_measures > 0:
                    currentNote = copy.deepcopy(self.currentList[location])
                    currentNote.dur = self.subdivisions
                    currentNote.tieStart = True
                    # FIXME: This needs to not get switched on first note
                    currentNote.measureFlag = True
                    if what_goes_to_the_last_measure > 0:
                        currentNote.tieEnd = True
                    currentNote.tieEnd = True
                    middleList.append(currentNote)
                    how_many_measures -= 1
                if what_goes_to_the_last_measure > 0:
                    currentNote = copy.deepcopy(self.currentList[location])
                    currentNote.dur = what_goes_to_the_last_measure
                    currentNote.tieEnd = True
                    currentNote.measureFlag = True
                    middleList.append(currentNote)
                lastCurrentCount = currentCount % self.subdivisions
                currentCount = overflow % self.subdivisions
            elif currentCountMod > 0 and currentCountFloor < 1:
                #print("buisness as usual")
                alteredDuration = copy.deepcopy(self.currentList[location])
                middleList.append(alteredDuration)
                lastCurrentCount = currentCountMod
        uniqueDurations = self.getUniques(middleList)
        print("durs", uniqueDurations)
        lcmOfDurations = reduce(self.lcm, uniqueDurations)
        print("lcm", lcmOfDurations)
        #self.subdivisions = self.measureFactor * lcmOfDurations
        print("self.subdivisions", self.subdivisions)
        # in the future, this will do scaling, etc.
        returnList = middleList
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
            self.subdivisions = currentBeats * currentMultiplier
            for location, item in enumerate(self.currentList):
                currentCount += item.dur
                # print("currentCount", currentCount)
                if currentCount == self.subdivisions:
                    if location != len(currentList) - 1:
                        self.currentList[location + 1].measureFlag = True
                    alteredDuration = copy.deepcopy(self.currentList[location])
                    alteredDuration.dur = alteredDuration.dur / currentMultiplier
                    returnList.append(alteredDuration)
                    currentCount = 0
                elif currentCount > self.subdivisions:
                    currentNote = copy.deepcopy(self.currentList[location])
                    # print("logic for ties", currentCount, self.subdivisions)
                    overflow = currentCount - self.subdivisions
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
