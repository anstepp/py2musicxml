def bjorklund(attacks, size):
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
        remainderCount = [counter + 1 for x in remainderList if x is min(remainderList)]
        remainder = len(remainderList)
    return returnList[0]


# printme = bjorklund(7, 12)
# print(# printme)
