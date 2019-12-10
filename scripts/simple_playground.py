import random

from py2musicxml.notation import Note, Score, Part, Rest


e = Note(duration=1, octave=5, pitch_class=4)
c = Note(duration=1, octave=5, pitch_class=0)
a = Note(duration=1, octave=4, pitch_class=9)
f = Note(duration=1, octave=4, pitch_class=5)

melody = [c, a, c, c, f, e, c]

other_stuff = [Note(x.dur*0.5, x.octave, x.pc * random.randrange(1, 5, 1)) for x in melody]

parts = [Part(p, [(4, 4)]) for p in [melody, other_stuff]]

score = Score(
    score_parts=parts, title="I don't even play a composer on TV", composer='Anon.'
)


score.convert_to_xml("simple_playground.xml")
