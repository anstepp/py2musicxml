import pitchMath
import noteList
# noteList: variance, seed
# noteList.getList:type, startingOctave, startingNote, generations, startingPitch, rType, rhythm
import random

random.seed(3)

one = noteList.noteList(0.5, 0)
two = noteList.noteList(0.5, 2)
three = noteList.noteList(0.5, 4)
four = noteList.noteList(0.5, 6)
five = noteList.noteList(0.5, 8)

generations = 4

first = one.getList("SWG", 4, 10, generations, 10, "ES", [random.uniform(10, 20) for x in range(20)])
second = two.getList("SWG", 4, 5, generations, 5, "ES", [random.uniform(10, 20) for x in range(20)])
third = three.getList("SWG", 4, 0, generations, 0, "ES", [random.uniform(10, 20) for x in range(20)])
fourth = four.getList("SWG", 3, 7, generations, 0, "ES", [random.uniform(10, 20) for x in range(20)])
fifth = five.getList("SWG", 3, 2, generations, 0, "ES", [random.uniform(10, 20) for x in range(20)])


scale = 2

listList = [[first, scale], [second, scale], [third, scale], [fourth, scale], [fifth, scale]]

pitchMath.convertToXML(listList, "score1.xml")