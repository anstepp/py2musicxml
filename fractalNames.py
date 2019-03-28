from py2musicxml import Note, NoteList, Score

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
                    for value in oddList:
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


iterateme = fractalNames(1, aaronPitches, morganPitches)
iterateme2 = fractalNames(1, morganPitches, aaronPitches)
# iterateme3 = fractalNames(4, morganPitches, aaronPitches)
# iterateme4 = fractalNames(5, morganPitches, aaronPitches)
notes = [Note(5, 2, x) for x in iterateme]
notes2 = [Note(5, 4, x) for x in iterateme2]
# notes3 = [Note(6, 3, x) for x in iterateme3]
# notes4 = [Note(1, 2, x) for x in iterateme4]
theList = NoteList(notes)
theList.getList(factor=1)
theList2 = NoteList(notes2)
theList2.getList(factor=2)
# theList3 = NoteList(notes3)
# theList3.getList(factor=2)
# theList4 = NoteList(notes4)
# theList4.getList(factor=5)
theScore = Score(theList, theList2)
theScore.convertToXML("fractal.xml")
