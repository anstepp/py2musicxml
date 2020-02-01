from py2musicxml.notation import Note, Score, Part

aaronPitches = [9, 9, 2, 0, 7]
morganPitches = [4, 0, 2, 7, 9, 7]
rachelPitches = [2, -3, 0, 11, 4, 9]
johnPitches = [4, 0, 11, 11]


def fractalNames(generations, list1, list2):
    oddList = list1
    evenList = list2
    returnList = oddList
    for i in range(generations):
        tempList = []
        if i % 2 == 0:
            for item in returnList:
                if item % 2 == 0:
                    for value in oddList:
                        tempList.append(value + item)
                else:
                    for value in evenList:
                        tempList.append(value + item)
        else:
            for item in returnList:
                if item % 2 == 0:
                    for value in oddList:
                        tempList.append(value + item)
                else:
                    for value in evenList:
                        tempList.append(value + item)
        returnList = tempList
    return returnList


iterateme = fractalNames(4, aaronPitches, morganPitches)

notes = [Note(0.25, 3, x) for x in iterateme]

theList = Part(notes, [(4,4)])

theScore = Score([theList])
theScore.convert_to_xml("fractal.musicxml")
