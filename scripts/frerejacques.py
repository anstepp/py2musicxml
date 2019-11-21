import pathlib
import random
import sys

# package_dir = pathlib.Path(__file__).parent.parent

# sys.path.append(package_dir)

from py2musicxml import Note, NoteList, Score, Part, Rest

# fmt: off
pitches = [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5, 4, 0, 0, -5, 0, 0, -5, 0]
durs = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 2, 4]
# fmt: on


frerejacques = [Note(x, 4, y) for x, y in zip(durs, pitches)]
frerejacques_delayed = [Rest(4) for x in range(4)] + frerejacques
frerejacques_delayed2 = [Rest(4) for x in range(4)] + frerejacques_delayed

frerejacques_delayed = frerejacques_delayed + frerejacques
frerejacques_delayed2 = frerejacques_delayed2 + frerejacques
frerejacques = frerejacques + frerejacques

time_signature = [(4,4),(3,4),(2,4)]

part_list = [
    Part(p, time_signature)
    for p in [frerejacques_delayed2, frerejacques_delayed, frerejacques]
]


score = Score(score_parts=part_list)
score.convert_to_xml("frerejacques.xml")
