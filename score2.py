import pitchMath
import noteList

# noteList: variance, seed
# noteList.getList:type, startingOctave, startingNote, generations, startingPitch, rType, rhythm, measure, factor
import random

random.seed(0)

one = noteList.noteList(0.5, 9)
two = noteList.noteList(0.5, 2)
three = noteList.noteList(0.25, 5)

generations = 10

# FIXME - old style, needs better way of differentating between ES and EU
# first = one.getList("SWG", 5, 5, generations, 5, "ES", [random.uniform(10, 20) for x in range(20)])
# second = two.getList("SWG", 4, 10, generations, 10, "ES", [random.uniform(10, 20) for x in range(20)])

factor1 = 1
factor2 = 3
factor3 = 2
beats = 4

first = one.getList("SG", 6, 5, generations, 5, "ES", [7, 20, 10], factor1, beats)
second = two.getList("SWG", 3, 10, generations, 10, "ES", [9, 22, 20], factor2, beats)
third = three.getList("SWG", 5, 0, generations, 10, "ES", [10, 31, 20], factor3, beats)

# print(first)
# print(second)

listList = [[first, factor1, beats], [second, factor2, beats], [third, factor3, beats]]

pitchMath.convertToXML(listList, "score2.xml")
