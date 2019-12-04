from py2musicxml import Note, Score, Part, Rest
from riemann_fractal_2 import Generations_Generator, Rests
from riemann import Riemann_Chord

gg_1 = Generations_Generator(Riemann_Chord(0,4,7))
gg_1.generation_algorithm(200, (2,8))
soprano_1 = gg_1.get_note_list(7, 2)
alto_1 = gg_1.get_note_list(8, 1)
bass_1 = gg_1.get_note_list(9, 0)

assert soprano_1 != alto_1 != bass_1

soprano_list_of_notes_1 = [Note(0.25, 5, pitch_class) for pitch_class in soprano_1]
alto_list_of_notes_1 = [Note(0.5, 5, pitch_class) for pitch_class in alto_1]
bass_list_of_notes_1 = [Note(1, 5, pitch_class) for pitch_class in bass_1]

soprano = soprano_list_of_notes_1
alto = alto_list_of_notes_1
bass = bass_list_of_notes_1

soprano_2 = gg_1.get_note_list(12, 2)
soprano_list_of_notes_2 = [Note(0.25, 4, pitch_class) for pitch_class in soprano_2]

soprano.append(Rest(4))
soprano.extend(soprano_list_of_notes_2)

ts = [(3,4)]

parts = [Part(p, ts) for p in [soprano, alto, bass]]

score = Score(score_parts=parts)

score.convert_to_xml("riemann_2.xml")