from py2musicxml.notation import Note, Part, Score

middle_c = Note(8,4,0)

short_note = Note(.5,4,2)
offset_note = Note(0.25,4,4)

middle_c.add_articulation("accent")
short_note.add_articulation("tenuto")

time_signature = [(3,4)]

simple_part = Part([middle_c, middle_c], time_signature)

our_score = Score(parts=[[simple_part]])
our_score.convert_to_xml("with_accent.musicxml")