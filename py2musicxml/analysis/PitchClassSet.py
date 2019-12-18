from __future__ import annotations

from itertools import cycle, compress
from typing import Iterable



class PitchClassSet():

    def __init__(self, pcs: Iterable[int]) -> None:

        self.ordered_set = set(pcs)

        self.ordered_list = list(self.ordered_set)

        self.ordered_list.sort()

        self.cardinality = len(self.ordered_list)

        self.normal_order = self._get_normal_order(self.ordered_list)


    def _get_normal_order(self, pclist: Iterable[int]) -> Iterable[int]:

        cycled_set = cycle(pclist)

        potential_set_orders = []

        for set_start in range(self.cardinality):

            current_set = []

            for current_pc in range(self.cardinality):

                current_set.append(next(cycled_set))

            zeroed_set = self._get_zero_start(current_set)
            zeroed_set_reversed = self._reverse_TI(zeroed_set)

            potential_set_orders.append(zeroed_set)

            if zeroed_set != zeroed_set_reversed:

              potential_set_orders.append(zeroed_set_reversed)

            next(cycled_set)

        first_to_last_pc_distance = [(s[-1] - s[0]) % 12 for s in potential_set_orders]

        minimum_distance = min(first_to_last_pc_distance)

        compression_mask = [1 if dist == minimum_distance else 0 for dist in first_to_last_pc_distance]

        minimum_distance_list = list(compress(first_to_last_pc_distance, compression_mask))
            
        candidates = []

        for idx, value in enumerate(compression_mask):
            if value == 1:
                minimum_potential = potential_set_orders[idx]
                candidates.append(minimum_potential)

        smallest_intervals = self._get_smallest_intervals_sorted(candidates)
        return smallest_intervals
        

    def _get_zero_start(self, pcs: Iterable[int]) -> Iterable[int]:
        zero_set = [(x - pcs[0]) % 12 for x in pcs]
        return zero_set

    def _get_smallest_intervals_sorted(self, candidates: Iterable[list]) -> Iterable[int]:

        generators = [self._interval_generator(candidate) for candidate in candidates]

        for idx in range(self.cardinality):
            current_intervals = [next(g) for g in generators]
            minimum_interval = min(current_intervals)
            counter = 0
            for interval in current_intervals:
                if interval == minimum_interval:
                    counter += 1
            if counter == 1:
                for interval, candidate in zip(current_intervals, candidates):
                    if interval == minimum_interval:
                        return candidate


    def _interval_generator(self, candidate: Iterable[int]):

        last_pc = 0

        for pc in candidate:
            interval = last_pc + pc
            last_pc = pc
            yield interval

    def _reverse(self, reverse_me: Iterable[int]) -> Iterable[int]:
        reversed_list = []
        for var in reverse_me[::-1]:
            reversed_list.append(var)

        return reversed_list

    def _reverse_TI(self, reverse_me: Iterable[int]) -> Iterable[int]:
        reversed_list = []

        for var in reverse_me[::-1]:
            if var == 0:
                var = 12

            tied = (((12 - var) + reverse_me[-1]) % 12)

            reversed_list.append(tied)

        return reversed_list

    def transpose(self, interval: int) -> PitchClassSet:

        new_pcs = [(pc + interval) % 12 for pc in self.ordered_list]

        return PitchClassSet(new_pcs)

    def invert(self) -> PitchClassSet:

        new_pcs = [(12 - pc) % 12 for pc in self.ordered_list]

        return PitchClassSet(new_pcs)

    def transpositional_inversion(self, interval: int) -> PitchClassSet:

        new_pcs = [((12 - var) + reverse_me[-1]) % 12 for pc in self.ordered_list]

        return PitchClassSet(new_pcs)

