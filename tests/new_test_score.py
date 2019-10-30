import pytest

from lxml import etree

from py2musicxml import Note, Part, Score, Measure, Beat


def test_simple_score():

    test_note_a = Note(4, 4, 4)
    test_note_b = Note(3, 3, 0)
    test_notelist = [test_note_a, test_note_b]

    time_signature = [(3, 4)]

    test_part = Part(test_notelist, time_signature)

    assert len(test_part.measure_list[0].notes) == 1
    assert len(test_part.measure_list[1].notes) == 2
    assert test_part.measure_list[0].beats[0].notes[0].dur == 3

    part_list = [test_part]
    score = Score(score_parts=part_list)

    assert test_part.measure_list[0].beats[0].notes[0].dur == 3

    score.convert_to_xml("frerejacques.xml")
