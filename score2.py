import pitchMath
import noteList
# noteList: variance, seed
# noteList.getList:type, startingOctave, startingNote, generations, startingPitch, rType, rhythm
import random

random.seed(0)

one = noteList.noteList(0.5, 0)
two = noteList.noteList(0.5, 2)

generations = 10

#FIXME - old style, needs better way of differentating between ES and EU
#first = one.getList("SWG", 5, 5, generations, 5, "ES", [random.uniform(10, 20) for x in range(20)])
#second = two.getList("SWG", 4, 10, generations, 10, "ES", [random.uniform(10, 20) for x in range(20)])

first = one.getList("SWG", 5, 5, generations, 5, "ES", [7, 20, 10])
second = two.getList("SWG", 3, 10, generations, 10, "ES", [9, 22, 10])

print(first)
print(second)

listList = [[first, 1], [second, 2]]

pitchMath.convertToXML(listList, "score2.xml")