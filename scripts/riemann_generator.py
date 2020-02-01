from py2musicxml.notation import Note, Score, Part, Rest
from riemann import RiemannChord
from itertools import cycle

import random

from typing import Iterable, Tuple, List

class RiemannGenerator:

    def __init__(self, starting_chord: RiemannChord):
        self.starting_chord = starting_chord
        self.generations_list = []
        self.voice_leading = False

        self.transformation_replacement = {
            'P' : 'LPL',
            'L' : 'SPS',
            'R' : 'PSP',
            'S' : 'LSL',
            'N' : 'PLR',
            'H' : 'LPL',
        }

    def set_replacements(self, transformation_replacements: dict) -> None:

        self.transformation_replacements = transformation_replacements


    def _get_windows(transformation: str, slice_start: int, slice_end: int):
            
        transform_window = None

        if len(transformation) < slice_start:
            transform_window = transformation
        elif len(transformation) < slice_end:
            transform_window = transformation[slice_start:]
        else:
            transform_window = transformation[slice_start:slice_end]

        return transform_window

    def _create_transformation_fractal(self, original_transformation: str, generations: int, window_start: int, window_end: int) -> List[str]:

        transformation_generations = []

        transform_this = original_transformation

        for generation in range(generations):

            transformed_transformations = []

            # transform = char in string
            for transform in transform_this:
                transformed_transform = self.transformation_replacement[transform]
                transformed_transformations.append(transformed_transform)
                new_transform = ''.join(transformed_transformations)


            windowed_transformation = self._get_windows(new_transform, window_start, window_end)
            transformation_generations.append(windowed_transformation)
            transform_this = windowed_transformation

        return transformation_generations


    def get_chords(self, original_transformation: str, generations: int, window_start: int, window_end: int) -> None:

        transformation_generations = self._create_transformation_fractal(original_transformation, generations, window_start, window_end)

        for generation in transformation_generations:

            chord = self.starting_chord

            current_chord_generation = [chord]

            for transformation in generation:

                chord = getattr(chord, transformation)()

                current_chord_generation.append(chord)

            self.generations_list.append(current_chord_generation)


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
            cycle_arp = cycle([chord.root, chord.third, chord.fifth])
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

    def _get_windows(self, transformation: str, slice_start: int, slice_end: int):
            
        transform_window = None

        if len(transformation) < slice_start:
            transform_window = transformation
        elif len(transformation) < slice_end:
            transform_window = transformation[slice_start:]
        else:
            transform_window = transformation[slice_start:slice_end]

        return transform_window

 


class Rests:

    def __init__(self, dur: int) -> None:
        self.dur = random.randint(1, dur)

    def change_dur(self, dur: int) -> None:
        self.dur = random.randint(1, dur)

    def get_list(self, iterations) -> list:
        rest_list = [Rest(self.dur) for x in range(iterations)]
        return rest_list



