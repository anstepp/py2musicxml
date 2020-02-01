from py2musicxml.notation import Score, Note, Part
from riemann import RiemannChord
from voice import Flute, Clarinet, Bassoon, Voice
from riemann_generator import RiemannGenerator

from typing import Iterable

import random


new_chord = RiemannChord(0,4,7)

next_chord = new_chord.P()

another_chord = next_chord.R()

chord_list = [chord for chord in [new_chord, next_chord, another_chord]]

bass = []
alto = []
soprano = []

for chord in chord_list:

    bass.append(Note(4, 2, chord.root))
    alto.append(Note(4, 4, chord.third))
    soprano.append(Note(4, 5, chord.fifth))

ts = [(4,4)]

part_list = [p for p in [soprano, alto, bass]]

parts = [Part(p, ts) for p in part_list]

the_score = Score(score_parts=parts)

the_score.convert_to_xml("two_chords.musicxml")