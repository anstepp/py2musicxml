import matplotlib.pyplot as plt
import numpy as np
import random
import statistics

from mpl_toolkits.mplot3d import Axes3D
import mpld3
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from typing import Iterable


from py2musicxml.notation import Score, Note, Rest
from riemann import RiemannChord
from voice import Flute, Clarinet, Bassoon, Voice, Violin, Cello
from riemann_generator import RiemannGenerator


# create instruments

flute = Flute()
clarinet = Clarinet()
violin = Violin()
cello = Cello()

# make a list for easy assignment

instruments = [flute, clarinet, violin, cello]

# create pitch generation algorithm

rg_1 = RiemannGenerator(RiemannChord(0, 4, 7))
rg_2 = RiemannGenerator(RiemannChord(2, 6, 9))
rg_3 = RiemannGenerator(RiemannChord(3, 6, 10))

# run algorithm, populate generations

print("Generating Riemann Fractal")

rg_1.generation_algorithm(2500, (10, 60))
rg_2.generation_algorithm(2500, (5, 65))
rg_3.generation_algorithm(2500, (0, 70))


# make a super simple chorale that goes further into the
# target replacement algorithm

time_signature = [(4, 4), (3, 4), (2, 4)]

generated_scores = []

n_samples = 2000

for generation in range(100, n_samples + 100):

    random.seed(generation)

    print("generation",generation,"of",n_samples+100)

    # if (generation % 3) == 2:

    #     flute.extend_pitches(rg_3.arp(generation, random.randint(6,12)))
    #     rhythm = [0.25 for x in flute.pitches]
    #     flute.extend_durations(rhythm)
    #     flute.make_note_list(6)
    #     flute.check_range()

    #     clarinet.extend_pitches(rg_3.get_note_list(generation, 2))
    #     cl_rhythm = [random.randint(1,4) for x in clarinet.pitches]
    #     clarinet.extend_durations(cl_rhythm)
    #     clarinet.make_note_list(4)
    #     clarinet.check_range()

    #     violin.extend_pitches(rg_3.arp(generation, random.randint(6,12)))
    #     violin_rhythm = [0.25 for x in violin.pitches]
    #     violin.extend_durations(violin_rhythm)
    #     violin.make_note_list(6)
    #     violin.check_range() 

    #     cello.extend_pitches(rg_3.get_note_list(generation, 0))
    #     cello_rhythm = [random.randint(1,4) for x in cello.pitches]
    #     cello.extend_durations(cello_rhythm)
    #     cello.make_note_list(2)
    #     cello.check_range()

    if (generation % 2) == 1:

        flute.extend_pitches(rg_2.arp(generation, random.randint(5,10)))
        rhythm = [0.25 for x in flute.pitches]
        flute.extend_durations(rhythm)
        flute.make_note_list(5)
        flute.check_range()

        clarinet.extend_pitches(rg_2.get_note_list(generation, 2))
        cl_rhythm = [random.randint(1,4) for x in clarinet.pitches]
        clarinet.extend_durations(cl_rhythm)
        clarinet.make_note_list(4)
        clarinet.check_range()

        violin.extend_pitches(rg_2.arp(generation, random.randint(6,12)))
        violin_rhythm = [0.25 for x in violin.pitches]
        violin.extend_durations(violin_rhythm)
        violin.make_note_list(5)
        violin.check_range() 

        cello.extend_pitches(rg_2.get_note_list(generation, 0))
        cello_rhythm = [random.randint(1,4) for x in cello.pitches]
        cello.extend_durations(cello_rhythm)
        cello.make_note_list(2)
        cello.check_range()

    if (generation % 2) == 0:   

        flute.extend_pitches(rg_1.arp(generation, random.randint(6,12)))
        rhythm = [0.25 for x in flute.pitches]
        flute.extend_durations(rhythm)
        flute.make_note_list(5)
        flute.check_range()

        clarinet.extend_pitches(rg_1.get_note_list(generation, 2))
        cl_rhythm = [random.randint(1,4) for x in clarinet.pitches]
        clarinet.extend_durations(cl_rhythm)
        clarinet.make_note_list(4)
        clarinet.check_range()

        violin.extend_pitches(rg_1.arp(generation, random.randint(5,10)))
        violin_rhythm = [0.25 for x in violin.pitches]
        violin.extend_durations(violin_rhythm)
        violin.make_note_list(5)
        violin.check_range() 

        cello.extend_pitches(rg_1.get_note_list(generation, 0))
        cello_rhythm = [random.randint(1,4) for x in cello.pitches]
        cello.extend_durations(cello_rhythm)
        cello.make_note_list(2)
        cello.check_range() 

    generated_scores.append(
        Score(
            score_parts=[
                instrument.make_part(time_signature) for instrument in instruments
            ]
        )
    )

    [instrument.clear_list() for instrument in instruments]

counter = 0

for score in generated_scores:
    file_name = "xml/score_data_set_" + str(counter) + ".xml"
    score.convert_to_xml(file_name)
    counter += 1
    print("score",counter,"of",len(generated_scores))

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
    score_duration_mean = statistics.mean(score_beat_durations)

    scores_features.append(
        [score_downbeat_pitch_class, score_measures, score_duration_mean]
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

pca = PCA(n_components=3)
pca.fit(X)
Xpca = pca.transform(X)

print(Xpca.shape)

# Xpca_embedded = TSNE(n_components=2).fit_transform(Xpca)

# print(Xpca_embedded.shape)

random_state = 900
n_clusters = 12

kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)

output = kmeans.fit_predict(Xpca)
for idx, item in enumerate(output):
    print(idx, item)

kmeanslabels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

fig = plt.figure(1, figsize=(20, 4))

ax = fig.add_subplot(111, projection='3d')
ax.scatter(Xpca[:,0], Xpca[:, 1], Xpca[:,2], c=kmeanslabels)

labels = ['score {0}'.format(i + 1) for i in range(len(scores_dataset))]
tooltip = mpld3.plugins.PointLabelTooltip(ax, labels=labels)
mpld3.plugins.connect(fig, tooltip)


plt.show()
