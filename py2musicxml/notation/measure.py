import copy

from typing import Iterable, List, Optional, Tuple, Union

from py2musicxml import Note, Beat, Rest


METER_DIVISION_TYPES = {2: "Duple", 3: "Triple", 4: "Quadruple"}


class Measure:
    def __init__(self, time_signature: Tuple, factor: int):

        self.time_signature = time_signature

        # A Measure contains a list of Beat objects
        self.beats = []

        # default to non-additive meter, this self corrects
        # equal divisions means all beats are the same, eg. 4/4, 3/4, but not 5/8
        self.equal_divisions = True

        # Measure number relative to order in Part()
        self.measure_number = None

        # hypermetric weight of measure
        # self.weight = None

        self.meter_division, self.meter_type, self.measure_map = (
            self._create_measure_map(factor)
        )

        self.cumulative_beats = list((x for x in self._cumulative_beat_generator()))
        self.total_cumulative_beats = self.cumulative_beats[-1]

    def is_empty(self) -> bool:
        if len(self.beats) == 0:
            return True
        else:
            return False

    def _cumulative_beat_generator(self) -> None:
        count = 0
        for beat in self.measure_map:
            count += beat
            yield count

    def add_beat(self, beat: Beat) -> None:
        self.beats.append(beat)

    def _create_measure_map(self, subdivisions: int) -> Tuple[Optional[str], str, List[int]]:
        '''
        1. Determines the measure division and type
            (measure_type will always be Simple, Compound, or Additive)

        2. Creates the measure map.
            measure map is a list of the beat durations in the measure; it maps out the beats of a measure
        '''

        meter_division = None
        meter_type = None
        measure_map = []

        if self.equal_divisions:

            # time sig denominator is divisible by 3
            if ((self.time_signature[0] % 3) == 0) and (self.time_signature[0] > 3):

                beats_in_measure = int(self.time_signature[0] / 3)

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Compound"
                measure_map = [subdivisions * 1.5 for x in range(beats_in_measure)]

            # time sig denominator is divisible by 2
            elif self.time_signature[1] % 2 == 0:

                beats_in_measure = self.time_signature[0]

                meter_division = METER_DIVISION_TYPES.get(beats_in_measure, None)
                meter_type = "Simple"
                measure_map = [subdivisions for x in range(beats_in_measure)]

            # time sig denominator is not divisible by 2 or 3
            else:
                self.equal_divisions = False

                # meter_division remains None
                meter_type = "Additive"
                measure_map = self.bjorklund()
        else:
            # meter_division remains None
            meter_type = "Additive"
            measure_map = self.bjorklund()

        return meter_division, meter_type, measure_map



    def bjorklund(self):
        '''Evenly spaces two numbers that are not divisible by each other'''

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
            remainderCount = [
                counter + 1 for x in remainderList if x is min(remainderList)
            ]
            remainder = len(remainderList)
        
        # return returnList[0]
        return [0]

