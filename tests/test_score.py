import pytest

from lxml import etree

from py2musicxml.notation import Note, Part, Score, Measure, Beat


def test_simple_score():

    durs = [3, 1, 2, 1, 2, 3, 1]
    test_note_a = Note(4, 4, 4)
    test_note_b = Note(3, 3, 0)
    test_note_c = Note(6, 6, 2)
    test_notelist = [test_note_a, test_note_b, test_note_c]

    time_signature = [(3, 4), (2, 4)]

    test_part = Part(test_notelist, time_signature)

    assert len(test_part.measures[0].notes) == 1
    assert len(test_part.measures[1].notes) == 2
    assert test_part.measures[0].beats[0].notes[0].dur == 3
    assert len(test_part.measures) == 5

    part_list = [test_part]
    score = Score(score_parts=part_list)

    score.convert_to_xml("frerejacques.xml")
