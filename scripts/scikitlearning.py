import matplotlib.pyplot as plt
import numpy as np
import random
import statistics

from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from typing import Iterable


from py2musicxml.notation import Score, Note, Rest
from riemann import RiemannChord
from voice import Flute, Clarinet, Bassoon, Voice
from riemann_generator import RiemannGenerator


# create instruments

flute = Flute()
clarinet = Clarinet()
bassoon = Bassoon()

# make a list for easy assignment

instruments = [i for i in [bassoon, clarinet, flute]]

# create pitch generation algorithm

rg_1 = RiemannGenerator(RiemannChord(0, 4, 7))
rg_2 = RiemannGenerator(RiemannChord(2, 6, 9))

# run algorithm, populate generations

rg_1.generation_algorithm(1200, (3, 50))
rg_2.generation_algorithm(1200, (2, 10))


# make a super simple chorale that goes further into the
# target replacement algorithm

time_signature = [(4, 4), (3, 4), (2, 4)]

generated_scores = []

n_samples = 500

for generation in range(0, n_samples):

    random.seed(generation)

    print(generation)

    if (generation % 2) == 1:

        flute.extend_pitches(rg_1.arp(generation, 6))
        rhythm = [0.25 for x in flute.pitches]
        flute.extend_durations(rhythm)
        flute.make_note_list(6)
        flute.check_range()

        clarinet.extend_pitches(rg_2.get_note_list(generation, 2))
        cl_rhythm = [random.randint(4,8) for x in clarinet.pitches]
        clarinet.extend_durations(cl_rhythm)
        clarinet.make_note_list(4)
        clarinet.check_range()

        bassoon.extend_pitches(rg_1.get_note_list(generation, 1))
        bsn_rhythm = [random.randint(1,4) for x in bassoon.pitches]
        bassoon.extend_durations(bsn_rhythm)
        bassoon.make_note_list(4)
        bassoon.check_range()

    if (generation % 2) == 0:

        flute.extend_pitches(rg_2.arp(generation, 7))
        rhythm = [0.25 for x in flute.pitches]
        flute.extend_durations(rhythm)
        flute.make_note_list(6)
        flute.check_range()

        clarinet.extend_pitches(rg_1.get_note_list(generation, 2))
        cl_rhythm = [random.randint(1,4) for x in clarinet.pitches]
        clarinet.extend_durations(cl_rhythm)
        clarinet.make_note_list(4)
        clarinet.check_range()

        bassoon.extend_pitches(rg_2.get_note_list(generation, 1))
        bsn_rhythm = [random.randint(4,8) for x in bassoon.pitches]
        bassoon.extend_durations(bsn_rhythm)
        bassoon.make_note_list(3)
        bassoon.check_range()   

    generated_scores.append(
        Score(
            score_parts=[
                instrument.make_part(time_signature) for instrument in instruments[::-1]
            ]
        )
    )


# counter = 0

# for score in generated_scores:
#     file_name = "score_data_set_" + str(counter) + ".xml"
#     score.convert_to_xml(file_name)
#     counter += 1
#     print(counter)

scores_downbeats = []
scores_features = []

for score in generated_scores:
    score_downbeats = []
    score_beat_durations = []
    measures = 0

    for part in score.score_parts:
        for measure in part.measures:

            first_measure_beat = measure.beats[0]
            first_measure_note = first_measure_beat.notes[0]

            score_beat_durations.append(first_measure_note.dur)

            if type(first_measure_note) is Note:
                score_downbeats.append(first_measure_note.pc)

            elif type(first_measure_note) is Rest:
                score_downbeats.append(0)

            measures += 1

    score_downbeat_pitch_class = statistics.mean(score_downbeats)
    score_measures = measures / len(score.score_parts)
    score_duration_mode = statistics.mean(score_beat_durations)

    scores_features.append(
        [score_downbeat_pitch_class, score_measures, score_duration_mode]
    )
    scores_downbeats.append(score_downbeats)


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
    downbeats = scores_downbeats[score_idx]
    features = features + downbeats
    scores_dataset.append(features)


print("Running KMeans")

X = np.array(scores_dataset)
print(X.shape)

pca = PCA(n_components=10)
pca.fit(X)
Xpca = pca.transform(X)

print(X.shape)

Xpca_embedded = TSNE(n_components=2).fit_transform(Xpca)

print(X.shape)

random_state = 345
n_clusters = 4

kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

meaned_data = kmeans.fit_predict(Xpca_embedded)

labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

fig = plt.figure(1, figsize=(20, 4))
ax = fig.add_subplot(111, projection='3d')

rx, ry = 3., 1.
area = rx * ry * np.pi
theta = np.arange(0, 2 * np.pi + 0.01, 0.1)
verts = np.column_stack([rx / area * np.cos(theta), ry / area * np.sin(theta)])

x, y, s, c = np.random.rand(4, 30)
s *= 10**2.

fig, ax = plt.subplots()
ax.scatter(X[:,0], X[:,2], c=labels)

# plt.show()

# ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels)


ax.set_xlabel('Downbeat Most Freq. Pitch Class')
ax.set_ylabel('Downbeat Most Freq. Duration')

plt.show()
