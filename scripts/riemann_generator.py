from py2musicxml.notation import Note, Score, Part, Rest
from riemann import RiemannChord
from itertools import cycle

import random

from typing import Iterable

class RiemannGenerator:

    def __init__(self, starting_chord: Iterable[RiemannChord]):
        self.starting_chord = starting_chord
        self.generations_list = []
        self.voice_leading = False

    def generation_algorithm(self, max_generations: int, input_slice: tuple):

        current_generation = [self.starting_chord]
        self.generations_list = [current_generation]
        generation = 1

        while generation < max_generations:

            generation_to_process = self.generations_list[generation - 2]
            current_generation = []
            if input_slice[0] > len(generation_to_process):
                slice_start = 0
                slice_end = len(generation_to_process)
            else:
                slice_start = input_slice[0]
                slice_end = input_slice[1]

            for index, chord in enumerate(generation_to_process[slice_start:slice_end]):

                if generation % 2 is True:

                    if chord.major is True:
                        new_chord = chord.S()
                        next_chord = new_chord.P()
                        final_chord = next_chord.S()
                        another_chord = final_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord, another_chord])

                    elif chord.minor is True:
                        new_chord = chord.S()
                        next_chord = new_chord.P()
                        final_chord = next_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord])

                else:

                    if chord.major is True:
                        new_chord = chord.R()
                        next_chord = new_chord.S()
                        final_chord = next_chord.R()
                        another_chord = final_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord, another_chord])

                    elif chord.minor is True:
                        new_chord = chord.L()
                        next_chord = new_chord.P()
                        final_chord = next_chord.S()

                        current_generation.extend([chord, new_chord, next_chord, final_chord])

            self.generations_list.append(list(current_generation)[slice_start:slice_end])
            generation += 1

    def get_note_list(self, generation: int, part: int):

        output_list = []

        list_to_operate_on = self.generations_list[generation]

        for chord in list_to_operate_on:

            part_dictionary = {0:chord.root, 1:chord.third, 2:chord.fifth}

            append_for_part = part_dictionary.get(part)

            output_list.append(append_for_part)
        
        return output_list

    def arp(self, generation: int, per_chord_notes: int) -> Iterable[int]:

        output_list = []

        for chord in self.generations_list[generation]:
            cycle_arp = cycle(chord.proper_voice_leading)
            for i in range(per_chord_notes):
                output_list.append(next(cycle_arp))
            
        return output_list

    def invert_list(self) -> Iterable[int]:

        inverted_list = []

        for pitch in output_list:
            inverted_list.append(12 - pitch)

        return inverted_list

    def transpose_list(self, transposition: int) -> Iterable[int]:
        
        transposed_list = []

        for pitch in output_list:
            transposed_list.append(pitch + transposition)

        return transposed_list

    def trans_invert_list(self, transposition: int) -> Iterable[int]:

        trans_inverted_list = []

        for pitch in self.output_list:
            trans_inverted_list.append((12 - pitch) + transposition)

        return trans_inverted_list


class Rests:

    def __init__(self, dur: int) -> None:
        self.dur = random.randint(1, dur)

    def change_dur(self, dur: int) -> None:
        self.dur = random.randint(1, dur)

    def get_list(self, iterations) -> list:
        rest_list = [Rest(self.dur) for x in range(iterations)]
        return rest_list



