from note import note
from noteList import noteList
from score import Score

aaronPitches = [9, 9, 2, 0, 7]
morganPitches = [4, 0, 2, 7, 9, 7]


def fractalNames(generations, list1, list2):
    oddList = list1
    evenList = list2
    returnList = oddList
    for i in range(generations):
        tempList = []
        if i % 2 is 0:
            for item in returnList:
                if item % 2 is 0:
                    for value in evenList:
                        tempList.append(value + item)
                else:
                    for value in evenList:
                        tempList.append(value + item)
        else:
            for item in returnList:
                if item % 2 is 0:
                    for value in oddList:
                        tempList.append(value + item)
                else:
                    for value in evenList:
                        tempList.append(value + item)
        returnList = tempList
    return returnList


iterateme = fractalNames(2, aaronPitches, morganPitches)
iterateme2 = fractalNames(3, aaronPitches, morganPitches)
iterateme3 = fractalNames(4, morganPitches, aaronPitches)
notes = [note(4, 2, x) for x in iterateme]
notes2 = [note(3, 4, x) for x in iterateme2]
notes3 = [note(5, 3, x) for x in iterateme3]
theList = noteList(notes)
theList.getList(factor=1)
theList2 = noteList(notes2)
theList2.getList(factor=2)
theList3 = noteList(notes3)
theList3.getList(factor=2)
theScore = Score(theList, theList2, theList3)

theScore.convertToXML("fractal.xml")
