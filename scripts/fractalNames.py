from py2musicxml import Note, NoteList, Score

aaronPitches = [9, 9, 2, 0, 7]
morganPitches = [4, 0, 2, 7, 9, 7]
rachelPitches = [2, -3, 0, 11, 4, 9]

nicer1 = [0, 2, 4, 6, 8]
nicer2 = [0, 2, 4, 7, 9]

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
iterateme2 = fractalNames(3, rachelPitches, aaronPitches)
iterateme3 = fractalNames(3, morganPitches, rachelPitches)
iterateme4 = fractalNames(3, nicer2, nicer1)
notes = [Note(1, 2, x) for x in iterateme]
notes2 = [Note(1, 4, x) for x in iterateme2]
notes3 = [Note(1, 3, x) for x in iterateme3]
notes4 = [Note(1, 2, x) for x in iterateme4]
theList = NoteList(notes)
theList.getList(factor=1)
theList2 = NoteList(notes2)
theList2.getList(factor=2)
theList3 = NoteList(notes3)
theList3.getList(factor=3)
theList4 = NoteList(notes4)
theList4.getList(factor=4)
theScore = Score(theList2, theList4, theList3, theList)
theScore.convertToXML("fractal.xml")
