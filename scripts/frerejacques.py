import pathlib
import sys

# package_dir = pathlib.Path(__file__).parent.parent

# sys.path.append(package_dir)

from py2musicxml import Note, NoteList, Score, Part

pitches = [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5, 4, 0, 0, -5, 0, 0, -5, 0]
durs = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2]

frerejacques = [Note(x, 4, y) for x, y in zip(durs, pitches)]

time_signature = [(4,4)]

part_fj = Part(frerejacques, time_signature)
part_list = [part_fj]

print(part_fj)
print(part_fj.final_list)
print(len(part_fj.final_list))

print(part_fj.final_list[0].beats)
print(len(part_fj.final_list[0].beats))

for i in range(len(part_fj.final_list[0].beats[0].notes)):
    print(part_fj.final_list[0].beats[0].notes[i])


score = Score(score_parts=part_list)
score.convert_to_xml("frerejacquesadj.xml")