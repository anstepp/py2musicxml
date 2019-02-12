from notePC import notePC

aaronPitches = [9,9,2,0,7]
morganPitches = [4,0,2,7,9,7]

def fractalNames(generations, list1, list2):
	oddList = list1
	evenList = list2
	returnList = oddList
	for i in range(generations):
		tempList = []
		if i % 2 is 0:
			for item in returnList:
				for value in evenList:
					tempList.append(value + item)
		else:
			for item in returnList:
				for value in oddList:
					tempList.append(value + item)
		returnList = tempList
	return returnList


iterateme = fractalNames(3, aaronPitches, morganPitches)
noteList = [notePC(4, x) for x in iterateme]
