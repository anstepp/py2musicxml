from py2musicxml.notation import Note, Score, Part, Rest
from itertools import cycle, product, starmap
import random

random = random.Random()


aaronPitches = [8, 8, 1, 0, 6]
morganPitches = [4, 0, 2, 7, 9, 7]
rachelPitches = [2, -3, 0, 11, 4, 9]
johnPitches = [4, 0, 11, 7]

names = [aaronPitches, morganPitches, rachelPitches, johnPitches]

def add(x,y):
    return x+y

cartesian_names = [starmap(add, y) for x in names for y in x]

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


def fibonacci_generator(start: int, distance: int, factor: float):

    current_value = start

    last_value = 0

    for x in range(distance):

        sum_of_values = current_value + last_value

        last_value = current_value
        current_value = sum_of_values

        yield sum_of_values * factor

fib = cycle(list(fibonacci_generator(1, 4, 0.25)))
fib_2 = cycle(list(fibonacci_generator(1,5,0.25)))

fibs = [fib, fib_2]

iterateme = fractalNames(2, aaronPitches, morganPitches)
iterateme_2 = fractalNames(2, johnPitches, morganPitches)
iterateme_3 = fractalNames(2, aaronPitches, rachelPitches)
iterateme_4 = fractalNames(2, johnPitches, rachelPitches)

iterate_list = [iterateme, iterateme_2, iterateme_3, iterateme_4]

lists = [[Note(0.25, 5, y) for y in x] for x in iterate_list]

ts = [(4, 4)]

parts = [Part(x, ts) for x in lists]

theScore = Score(score_parts=parts)
theScore.convert_to_xml("fractal.musicxml")
