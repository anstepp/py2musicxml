from pprint import pprint
from typing import List

class RiemannChord:
    def __init__(self, note_a: int, note_b: int, note_c: int) -> None:
        self.root = note_a
        self.third = note_b
        self.fifth = note_c
        self.major = None
        self.minor = None

        self.proper_voice_leading = [self.root, self.third, self.fifth]
        self.proper_voice_leading.sort()

        test_fifth = (self.fifth - self.root) % 12
        if test_fifth == 7 or test_fifth == -5:
            test_third = (self.third - self.root) % 12
            if test_third == 4 or test_third == -8:

                self.major = True
                self.minor = False
            elif test_third == 3 or test_third == -9:

                self.major = False
                self.minor = True
            else:
                print("test failed - third", test_third)
        else:
            print("test failed - fifth.", test_fifth)

    # parallel
    def P(self):
        if self.major is True:
            new_third = (self.third - 1) % 12
        elif self.minor is True:
            new_third = (self.third + 1) % 12
        return RiemannChord(self.root, new_third, self.fifth)

    # relative
    def R(self):
        if self.major is True:
            new_root = (self.fifth + 2) % 12
            return RiemannChord(new_root, self.root, self.third)
        elif self.minor is True:
            new_fifth = (self.root - 2) % 12
            return RiemannChord(self.third, self.fifth, new_fifth)

    # leading tone
    def L(self):
        if self.major is True:
            new_fifth = (self.root - 1) % 12
            return RiemannChord(self.third, self.fifth, new_fifth)
        elif self.minor is True:
            new_root = (self.fifth + 1) % 12
            return RiemannChord(new_root, self.root, self.third)

    # Slide
    def S(self):
        a = self.L()
        b = a.P()
        c = b.R()
        return c

    # nebenverwandt
    def N(self):
        a = self.R()
        b = a.L()
        c = b.P()
        return c

    # Hexatonic pole
    def H(self):
        a = self.L()
        b = a.P()
        c = b.L()
        return c

    def __str__(self):
        return 'Root: {}, Third: {}, Fifth: {}'.format(
            self.root, self.third, self.fifth
        )


def _get_windows(transformation: str, slice_start: int, slice_end: int):
        
    transform_window = None

    if len(transformation) < slice_start:
        transform_window = transformation
    elif len(transformation) < slice_end:
        transform_window = transformation[slice_start:]
    else:
        transform_window = transformation[slice_start:slice_end]

    return transform_window

def create_transformation_fractal(original_transformation: str, generations: int, window_start: int, window_end: int) -> List[str]:

    transformation_replacement = {
        'P' : 'LPL',
        'L' : 'SPS',
        'R' : 'PSP',
        'S' : 'LSL',
        'N' : 'PLR',
        'H' : 'LPL',
    }

    transformation_generations = []

    transform_this = original_transformation

    for generation in range(generations):

        transformed_transformations = []

        # transform = char in string
        for transform in transform_this:
            transformed_transform = transformation_replacement[transform]
            transformed_transformations.append(transformed_transform)
            new_transform = ''.join(transformed_transformations)

        windowed_transformation = _get_windows(new_transform, window_start, window_end)
        transformation_generations.append(windowed_transformation)
        transform_this = windowed_transformation

    return transformation_generations


chord = RiemannChord(0,4,7)
start_transformations = "PLRPLRPLRPLR"

result = create_transformation_fractal(start_transformations, 1000, 0, 100)

for generation in result:
    print('\n')
    for letter in generation:
        current_transformation = getattr(chord, letter)
        new_chord = current_transformation()
        print(new_chord)
        chord = new_chord



