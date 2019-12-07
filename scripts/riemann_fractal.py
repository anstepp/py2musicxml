from py2musicxml import Note, Score, Part, Rest
from riemann import RiemannChord

import random

starting_chord = RiemannChord(0,4,7)

def rules(input_chord, generation):

    if chord.major is True:
        new_chord = chord.S()
        next_chord = new_chord.P()
        final_chord = next_chord.S()
        another_chord = final_chord.L()

        return [[chord, generation], [new_chord, generation], [next_chord, generation], [final_chord, generation], [another_chord, generation]]


    elif chord.minor is True:
        new_chord = chord.S()
        next_chord = new_chord.P()
        final_chord = next_chord.S()

        return [[chord, generation], [new_chord, generation], [next_chord, generation], [final_chord, generation]]


generation = 1
generations = 3
chord_list = [[starting_chord, generation],]


while generation < generations:
    generation += 1
    append_me = []
    for entry in chord_list:
        chord = entry[0]
        append_me += rules(chord, generation)
    chord_list += append_me


rests = [Rest(random.randint(1,4)) for x in range(random.randint(1,4))]

fifths = [Note(0.25, 5, entry[0].fifth) for entry in chord_list]
fifths_2 = [Note(0.25, 5, entry[0].fifth + 1) for entry in chord_list]
fifths_3 = [Note(0.25, 5, entry[0].fifth + 2) for entry in chord_list]
fifths_4 = [Note(0.25, 5, entry[0].fifth + 3) for entry in chord_list]
thirds = [Note(0.5, 4, entry[0].third) for entry in chord_list]
thirds_2 = [Note(0.5, 4, entry[0].third - 2) for entry in chord_list]
roots = [Note(1, 3, entry[0].root) for entry in chord_list]

fifths = fifths + rests + fifths_2 + rests + fifths_3 + rests + fifths_4 + rests
thirds = thirds + rests + thirds_2 + rests

ts = [(4,4)]

fifths_5 = [Note(random.randint(1,3), 5, entry[0].proper_voice_leading[entry[1] % 3]) for entry in chord_list]
thirds_2 = [Note(random.randint(1,3), 5, entry[0].proper_voice_leading[(entry[1] % 2)]) for entry in chord_list]
roots_2 = [Note(random.randint(1,3), 4, entry[0].proper_voice_leading[(entry[1] % 1)]) for entry in chord_list]

fifths += fifths_5
thirds += thirds_2
roots += roots_2

new_bass = [Note(0.25, 3, entry[0].root) for entry in chord_list]

roots += new_bass + rests + [Note(0.25, 3, note.pc + 2) for note in new_bass] + rests + [Note(0.25, 3, note.pc + 4) for note in new_bass]

new_mezzo = [Note(0.25, 4, entry[0].root) for entry in chord_list]

thirds += new_mezzo + rests + [Note(0.25, 4, note.pc + 2) for note in new_mezzo] + rests + [Note(0.25, 4, note.pc + 4) for note in new_mezzo]

new_soprano = [Note(0.25, 5, entry[0].root) for entry in chord_list]
new_soprano_2 = [Note(0.25, 5, entry[0].third) for entry in chord_list]
new_soprano_3 = [Note(0.25, 5, entry[0].fifth) for entry in chord_list]

fifths = fifths + rests + new_soprano

final_chorale_sop = [Note(random.randint(2,6), 6, entry[0].proper_voice_leading[entry[1] % 3]) for entry in chord_list]
final_chorale_mezzo = [Note(random.randint(2,6), 5, entry[0].proper_voice_leading[(entry[1] % 2)]) for entry in chord_list]
final_chorale_bass = [Note(random.randint(2,6), 4, entry[0].proper_voice_leading[(entry[1] % 1)]) for entry in chord_list]

fifths += final_chorale_sop
thirds += final_chorale_mezzo
roots += final_chorale_bass

parts = [Part(p, ts) for p in [fifths, thirds, roots]]

score = Score(score_parts=parts)

score.convert_to_xml("riemann.xml")