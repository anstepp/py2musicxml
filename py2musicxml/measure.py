import bjorklund.py
from .note import Note
from .beat import Beat

class Measure():
    index = None
    beats = []
    weight = None
    #divisions is subdivisions of the quarter note
    divisions = None 
    #subdivisions is the musical
    subdivisions = []
    time_signature = tuple()
    notes = []

    def __init__(self, notes: Iterable[NoteList]):
        self.notes = notes
        self.get_divisions()

    def gcd(self, a: Union[int, float], b: Union[int, float]):
        if type(a) and type(b) is int:
            while b:
                a, b = b, a % b
            return a
        else:
            # convert float to fraction by approximating denominator then gcd
            return fractions.gcd(
                fractions.Fraction(a).limit_denominator(),
                fractions.Fraction(b).limit_denominator(),
            )

    def lcm(self, a: int, b: int):
        return a * b // self.gcd(a, b)

    def get_divisions(self):
        self.divisions = reduce(self.lcm, self.notes.dur)

    def divide_measure(self):
        current_count = 0
        current_beat = 0
        measure_map = []
        for beat in self.meter:
            measure_map.append(beat * self.subdivisions)

    def bjorklund(self, unspacedList: Iterable[NoteList]):
        unspacedList = unspacedList
        returnList = []
        remainder = len(unspacedList)

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
