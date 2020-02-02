import matplotlib.pyplot as plt
import mpld3
import numpy as np
import random
import re
import statistics

from collections import Counter
from importlib import import_module
from itertools import cycle
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from typing import Iterable, Tuple

from py2musicxml.analysis import PitchClassSet
from py2musicxml.composition import RiemannChord
from py2musicxml.composition.voice import Flute, Clarinet, Bassoon, Voice, Violin, Cello
from py2musicxml.notation import Score, Note, Rest

from riemann_generator import RiemannGenerator


PITCH_CLASS_SETS = {
    # trichords are 0-11
    0: [0, 1, 2],
    1: [0, 1, 3],
    2: [0, 1, 4],
    3: [0, 1, 5],
    4: [0, 1, 6],
    5: [0, 2, 4],
    6: [0, 2, 5],
    7: [0, 2, 6],
    8: [0, 2, 7],
    9: [0, 3, 6],
    10: [0, 3, 7],
    11: [0, 4, 8],
    # tetrachords are 12-40
    12: [0, 1, 2, 3],
    13: [0, 1, 2, 4],
    14: [0, 1, 2, 5],
    15: [0, 1, 2, 6],
    16: [0, 1, 2, 7],
    17: [0, 1, 3, 4],
    18: [0, 1, 3, 5],
    19: [0, 1, 3, 6],
    20: [0, 1, 3, 7],
    21: [0, 1, 4, 5],
    22: [0, 1, 4, 6],
    23: [0, 1, 4, 7],
    24: [0, 1, 4, 8],
    25: [0, 1, 5, 6],
    26: [0, 1, 5, 7],
    27: [0, 1, 5, 8],
    28: [0, 1, 6, 7],
    29: [0, 2, 3, 5],
    30: [0, 2, 3, 6],
    31: [0, 2, 3, 7],
    32: [0, 2, 4, 6],
    33: [0, 2, 4, 7],
    34: [0, 2, 4, 8],
    35: [0, 2, 5, 7],
    36: [0, 2, 5, 8],
    37: [0, 2, 6, 8],
    38: [0, 3, 4, 7],
    39: [0, 3, 5, 8],
    40: [0, 3, 6, 9],
    # pentachords are
    41: [0, 1, 2, 3, 4],
    42: [0, 1, 2, 3, 5],
    43: [0, 1, 2, 3, 6],
    44: [0, 1, 2, 3, 7],
    45: [0, 1, 2, 4, 5],
    46: [0, 1, 2, 4, 6],
    47: [0, 1, 2, 4, 7],
    48: [0, 1, 2, 4, 8],
    49: [0, 1, 2, 5, 6],
    50: [0, 1, 2, 5, 7],
    51: [0, 1, 2, 5, 8],
    52: [0, 1, 2, 6, 7],
    53: [0, 1, 2, 6, 8],
    54: [0, 1, 3, 4, 6],
    55: [0, 1, 3, 4, 7],
    56: [0, 1, 3, 4, 8],
    57: [0, 1, 3, 5, 6],
    58: [0, 1, 3, 5, 7],
    59: [0, 1, 3, 5, 8],
    60: [0, 1, 3, 6, 7],
    61: [0, 1, 3, 6, 8],
    62: [0, 1, 3, 6, 9],
    63: [0, 1, 4, 5, 7],
    64: [0, 1, 4, 5, 8],
    65: [0, 1, 4, 6, 8],
    66: [0, 1, 4, 6, 9],
    67: [0, 1, 4, 7, 8],
    68: [0, 1, 5, 6, 8],
    69: [0, 2, 3, 4, 6],
    70: [0, 2, 3, 4, 7],
    71: [0, 2, 3, 5, 7],
    72: [0, 2, 3, 6, 8],
    73: [0, 2, 4, 5, 8],
    74: [0, 2, 4, 6, 8],
    75: [0, 2, 4, 6, 9],
    76: [0, 2, 4, 7, 9],
    77: [0, 3, 4, 5, 8],
}

PITCH_CLASS_ASSIGNMENT = {str(v): k for k, v in PITCH_CLASS_SETS.items()}


class Fractal:
    def __init__(self, n_samples: int, n_generators: int) -> None:

        self.n_samples = n_samples

        self.generators = self.initiate_generators(n_generators)

        self.instrument_list = []

        self.generated_scores = []

        # create instruments

    def set_time_signature(self, ts: Tuple) -> None:

        self.time_signature = ts

    def generate_instruments(self, instruments: Iterable[Voice]) -> None:

        self.instrument_list = instruments

    def initiate_generators(self, number: int) -> None:

        print("Generating Riemann Fractal")

        root = 0
        third = 3
        fifth = 7

        generators = []

        # create pitch generation algorithm

        for x in range(number):
            generators.append(
                RiemannGenerator(
                    RiemannChord((root + x) % 12, (third + x) % 12, (fifth + x) % 12)
                )
            )

        # run algorithm, populate generations

        for generator in generators:
            generator.get_chords('PLR', self.n_samples + 100, 0, 50)

        return generators

    def fibonacci_generator(self, start: int, distance: int, factor: float):

        current_value = start

        last_value = 0

        for x in range(distance):

            sum_of_values = current_value + last_value

            last_value = current_value
            current_value = sum_of_values

            yield sum_of_values * factor

    def _create_part_arpeggio(
        self,
        generation: int,
        generator: int,
        instrument: Voice,
        arp_duration: int,
        octave: int,
        durations: Iterable[int],
    ) -> None:

        cycled_durs = cycle(durations)

        instrument.extend_pitches(generator.arp(generation, arp_duration))
        rhythm = [next(cycled_durs) for x in instrument.pitches]
        instrument.extend_durations(rhythm)
        instrument.make_note_list(octave)
        instrument.check_range()
        return instrument

    def _create_part_long_notes(
        self,
        generation: int,
        generator: int,
        instrument: Voice,
        octave: int,
        durations: Iterable[int],
        voice,
    ) -> None:

        cycled_durs = cycle(durations)

        instrument.extend_pitches(generator.get_note_list(generation, voice))
        rhythm = [next(cycled_durs) for x in instrument.pitches]
        instrument.extend_durations(rhythm)
        instrument.make_note_list(4)
        instrument.check_range()
        return instrument

    def make_internal_scores(
        self,
        offset: int,
        arp_instruments: Iterable[str],
        sustain_instruments: Iterable[str],
    ) -> None:

        arp_generator = cycle(list(self.fibonacci_generator(1, 10, 1)))
        duration_generator = cycle(list(self.fibonacci_generator(1,6,0.25)))
        long_duration_generator = cycle(list(self.fibonacci_generator(1,6,1)))
        long_distance_generator = cycle(list(self.fibonacci_generator(3,6,1)))

        for generation in range(offset, self.n_samples + offset):

            random.seed(generation)

            print("generation", generation, "of", self.n_samples + offset)

            for instrument_idx, instrument in enumerate(self.instrument_list):
                instrument_type = re.match(r'.*voice.(.*)\'>$', str(type(instrument))).group(1)

                if instrument_type in arp_instruments:
                    arp_dur = next(arp_generator)
                    octave = 6
                    durs = duration_generator
                    for dur in durs:
                        print(dur)
                    self.instrument_list[instrument_idx] = self._create_part_arpeggio(
                        generation,
                        self.generators[generation % len(self.generators)],
                        instrument,
                        arp_dur,
                        octave,
                        durs,
                    )

                if instrument_type in sustain_instruments:
                    octave = 3
                    durs = [next(long_duration_generator) for x in range(next(long_distance_generator))]
                    voice = generation % 3
                    self.instrument_list[instrument_idx] = self._create_part_long_notes(
                        generation,
                        self.generators[generation % len(self.generators)],
                        instrument,
                        octave,
                        durs,
                        voice,
                    )

            self.generated_scores.append(
                Score(
                    score_parts=[
                        instrument.make_part(time_signature)
                        for instrument in self.instrument_list
                    ]
                )
            )

            [instrument.clear_list() for instrument in self.instrument_list]

        counter = 0

    def make_scores(self):

        counter = 0

        for score in self.generated_scores:
            file_name = "xml/score_data_set_" + str(counter) + ".musicxml"
            score.convert_to_xml(file_name)
            counter += 1
            print("score", counter, "of", len(self.generated_scores))


time_signature = [(4, 4)]

f = Fractal(n_samples=3500, n_generators=4)

f.set_time_signature(time_signature)

f.generate_instruments([Flute(), Clarinet(), Violin(), Cello()])

arp_instruments = ['Flute', 'Violin']
sustain_instruments = ['Clarinet', 'Cello']

f.make_internal_scores(100, arp_instruments, sustain_instruments)

#f.make_scores()


scores_downbeats = []
scores_features = []

def get_measure_downbeat_stress(stress_list: Iterable[int]) -> Iterable[int]:
    pass

def get_mode_pc_normal_order(no_list: Iterable[int]) -> Iterable[int]:

    no_list = [tuple(no) for no in no_list]

    no_list_uniques = []

    for no in no_list:
        if no in no_list_uniques:
            pass
        else:
            no_list_uniques.append(no)

    pc_set_dict = {}

    for item in no_list_uniques:
        pc_set_dict[item] = 0

    for item in no_list:

        pc_set_dict[item] = pc_set_dict[item] + 1

    max_pc_set = max(pc_set_dict, key=pc_set_dict.get)

    max_pc_str = [str(pc) for pc in max_pc_set]

    return " ".join(max_pc_str)

for score in f.generated_scores:
    score_downbeats = []
    score_beat_durations = []
    measures = 0
    
    downbeat_pitch_class_sets = []

    for part in score.score_parts:

        part_measure_first_beats = []

        for idx, measure in enumerate(part.measures):

            # first beat in the measure
            first_measure_beat = measure.beats[0]
            
            # if first beat contains notes
            if first_measure_beat.notes:
               first_measure_note = first_measure_beat.notes[0]

            # (notes and rests have durations)
            score_beat_durations.append(first_measure_note.dur)

            if type(first_measure_note) is Note:
                # first measure note is actually a note
                # append note pitch class
                part_measure_first_beats.append(first_measure_note.pc)

            elif type(first_measure_note) is Rest:
                # first measure note is actually a rest
                part_measure_first_beats.append(None)

            else:
                raise Exception('Invalid first measure note type')

            measures += 1

        # add list of part's first measure beats
        downbeat_pitch_class_sets.append(part_measure_first_beats)

    # print('part downbeats')
    # for part_downbeats in downbeat_pitch_class_sets:
    #     print(part_downbeats)

    # Figure out our score pitch classes
    total_measures = len(score.score_parts[0].measures)
    
    score_normal_orders = []

    for measure_idx in range(total_measures):

        downbeat_pitches = [x[measure_idx] for x in downbeat_pitch_class_sets]
        pc_set = PitchClassSet(downbeat_pitches)
        pc_set_normal_order = pc_set.normal_order

        # print(' measure idx: {}'.format(measure_idx))
        # print('downbeat pcs: {}'.format(downbeat_pitches))
        # print('normal order: {}'.format(pc_set_normal_order))

        if len(pc_set_normal_order) > 2:
            score_normal_orders.append(str(pc_set_normal_order))

    # print('Score Normal Orders')
    # for x in score_normal_orders:
    #     print(x)

    cnt = Counter()

    for normal_order in score_normal_orders:
        cnt[normal_order] += 1

    #score_downbeat_mode_pcset = get_mode_pc_normal_order([PitchClassSet(pcs).normal_order for pcs in downbeat_pcsets])

    scores_downbeats.append(score_downbeats)

    top_three_set_classes = cnt.most_common(3)

    score_downbeat_pitch_class_one = PITCH_CLASS_ASSIGNMENT[top_three_set_classes[0][0]]
    score_downbeat_pitch_class_two = PITCH_CLASS_ASSIGNMENT[top_three_set_classes[1][0]]
    score_downbeat_pitch_class_three = PITCH_CLASS_ASSIGNMENT[top_three_set_classes[2][0]]

    score_measures = measures / len(score.score_parts)
    score_duration_mean = statistics.mean(score_beat_durations)


    scores_features.append(
        [score_downbeat_pitch_class_one, 
        score_downbeat_pitch_class_two, 
        score_downbeat_pitch_class_three, 
        score_duration_mean,
        score_measures]
    )


# Zero pad any scores downbeat lists < max size downbeat list
max_score_downbeat_len = max(
    [len(score_downbeats) for score_downbeats in scores_downbeats]
)

for score_downbeats in scores_downbeats:
    if len(score_downbeats) < max_score_downbeat_len:
        for i in range(len(score_downbeats), max_score_downbeat_len):
            score_downbeats.append(0)


# Assemble all score features and downbeats into a dataset
scores_dataset = []
for score_idx in range(len(scores_downbeats)):
    features = scores_features[score_idx]
    # downbeats = scores_downbeats[score_idx]
    # features = features + downbeats
    scores_dataset.append(features)


print("Running KMeans")

X = np.array(scores_dataset, dtype=object)
print(X.shape)

pca = PCA(n_components=3)
pca.fit(X)
Xpca = pca.transform(X)

# print(Xpca.shape)

# Xpca = TSNE(n_components=3).fit_transform(X)

# print(Xpca.shape)

random_state = 900
n_clusters = 8

kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

output = kmeans.fit_predict(Xpca)
for idx, item in enumerate(output):
    print(idx, item)

kmeanslabels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

fig = plt.figure(1, figsize=(20, 4))

ax = fig.add_subplot(111, projection='3d')
ax.scatter(Xpca[:,0], Xpca[:, 1], Xpca[:,2], c=kmeanslabels)

# labels = ['score {0}'.format(i + 1) for i in range(len(scores_dataset))]
# tooltip = mpld3.plugins.PointLabelTooltip(ax, labels=labels)
# mpld3.plugins.connect(fig, tooltip)

plt.show()

