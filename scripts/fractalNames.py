from py2musicxml import Note, Score, Part

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


iterateme = fractalNames(4, aaronPitches, morganPitches)
iterateme2 = fractalNames(2, rachelPitches, aaronPitches)
iterateme3 = fractalNames(2, morganPitches, rachelPitches)
iterateme4 = fractalNames(2, nicer2, nicer1)
notes = [Note(0.25, 3, x) for x in iterateme]
notes2 = [Note(3, 3, x) for x in iterateme2]
notes3 = [Note(0.5, 3, x) for x in iterateme3]
notes4 = [Note(5, 3, x) for x in iterateme4]
notes5 = [Note(0.33, 3, x) for x in iterateme]
theList = Part(notes, [[4,4]])
theList2 = Part(notes2, [[4,4]])
theList3 = Part(notes3, [[4,4]])
theList4 = Part(notes4, [[4,4]])
theList5 = Part(notes5, [(4,4)])
theScore = Score([theList, theList2, theList3, theList4, theList5])
theScore.convert_to_xml("fractal.xml")
