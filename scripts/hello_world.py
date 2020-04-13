from py2musicxml.notation import Note, Part, Score

middle_c = Note(8,4,0)

middle_c.add_articulation("accent")

time_signature = [(2,4)]

simple_part = Part([middle_c], time_signature)

our_score = Score(parts=[[simple_part]])
our_score.convert_to_xml("with_accent.musicxml")