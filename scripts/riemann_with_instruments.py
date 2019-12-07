from py2musicxml import Score
from riemann import RiemannChord
from voice import Flute, Clarinet, Bassoon, Voice
from riemann_generator import RiemannGenerator

from typing import Iterable

import random

# create instruments

flute = Flute()
clarinet = Clarinet()
bassoon = Bassoon()

# make a list for easy assignment

instruments = [i for i in [bassoon, clarinet, flute]]

#create pitch generation algorithm

rg_1 = RiemannGenerator(RiemannChord(0,4,7))
rg_2 = RiemannGenerator(RiemannChord(2,6,9))

# run algorithm, populate generations

rg_1.generation_algorithm(200, (3,50))
rg_2.generation_algorithm(200, (2,10))


# make a super simple chorale that goes further into the 
# target replacement algorithm

generation = 50
time_signature = [(4,4), (3,4), (2,4)]

score_list = []

for generation in range(0, 100):

    flute.extend_pitches(rg_1.arp(generation, 4))
    rhythm = [0.25 for x in flute.pitches]
    flute.extend_durations(rhythm)
    flute.make_note_list(6)
    flute.check_range()

    clarinet.extend_pitches(rg_2.get_note_list(generation, 2))
    cl_rhythm = [1 for x in clarinet.pitches]
    clarinet.extend_durations(cl_rhythm)
    clarinet.make_note_list(4)
    clarinet.check_range()
    clarinet.make_staccato((random.randint(0,10), random.randint(10,20)))
    clarinet.make_staccato((random.randint(20,30), random.randint(40,50)))

    bassoon.extend_pitches(rg_2.get_note_list(generation, 0))
    bsn_rhythm = [1 for x in bassoon.pitches]
    bassoon.extend_durations(bsn_rhythm)
    bassoon.make_note_list(4)
    bassoon.check_range()
    bassoon.make_staccato((random.randint(0,10), random.randint(10,20)))
    bassoon.make_staccato((random.randint(20,30), random.randint(40,50)))

    score_list.append(Score(score_parts=[instrument.make_part(time_signature) for instrument in instruments[::-1]]))

print(len(score_list))

counter = 0

for score in score_list:
    file_name = "score_data_set_" + str(counter) + ".xml"
    score.convert_to_xml(file_name)
    counter += 1



