from py2musicxml.notation import Note, Score, Part, Rest

aaronPitches = [9, 9, 1, 0, 7]
morganPitches = [4, 0, 2, 7, 9, 7]
rachelPitches = [2, -3, 0, 11, 4, 9]
johnPitches = [4, 0, 11, 7]

aaronCompleteTransposed = [Note(1, 4, x + y) for y in range(0,11) for x in aaronPitches]
morganCompleteTransposed = [Note(1, 4, x + y) for y in range(0,11) for x in morganPitches]

ts = [(4,4)]

parts = [Part(x, ts) for x in [aaronCompleteTransposed, morganCompleteTransposed]]

score = Score(score_parts=parts)
score.convert_to_xml("example_transposed.musicxml")

cross_tranposed = [Note(1, 4, x + y) for y in aaronPitches for x in morganPitches]

part = Part(cross_tranposed, ts)

score_2 = Score(score_parts=[part])
score_2.convert_to_xml("nested_transposition.musicxml")