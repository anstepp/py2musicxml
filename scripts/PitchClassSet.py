from itertools import cycle, compress

class PitchClassSet:

    def __init__(self, pc_set: Iterable[int]) -> None:
        self.pc_set = pc_set
        self.set_normal_order = self._normal_order(set(pc_set))

    def _normal_order(self, pc_set: Iterable[int]) -> Iterable[int]:
 
        ordered_set = sort(pc_set)
        list_of_possibles = self._make_orders(ordered_set)
        set_pc_size = [s[-1] - s[0] for s in list_of_possibles]
        set_minimum_size = min(set_pc_size)
        minimum_sets = [1 if x == set_minimum_size else 0 for x in set_pc_size]
        compressed_sets = compress(list_of_possibles, minimum_sets)
        if len(compressed_sets) == 1:
            return compressed_sets[0]
        else:
            normal_order = self._smallest_intervals_in_a_set(compressed_sets)
            return normal_order

    def _make_orders(self) -> Iterable[int]:
        pass

    def _smallest_intervals_in_a_set(self) -> Iterable[int]:
        pass

        



