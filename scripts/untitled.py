from py2musicxml import Note, NoteList, Score

pitches = [0, 2, 4, 0, 0, 2, 4, 0, 4, 5, 7, 4, 5, 7, 7, 9, 7, 5, 4, 0, 7, 9, 7, 5, 4, 0, 0, -5, 0, 0, -5, 0]
durs = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2]

frerejacques = [Note(x, 4, y) for x, y in zip(durs, pitches)]

notelist_fj = NoteList(frerejacques)
part_fj = notelist_fj.get_list()
score = Score(score_parts=part_fj)
score.convert_to_xml("frerejacques.xml")