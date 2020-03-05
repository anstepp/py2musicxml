from py2musicxml.notation import Note, Part, Score

middle_c = Note(4,4,0)

time_signature = [(4,4)]

simple_part = Part([middle_c], time_signature)

our_score = Score(score_parts=[simple_part])
our_score.convert_to_xml("middle_c.musicxml")