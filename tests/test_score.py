import pytest

from lxml import etree

from py2musicxml import Note, NoteList, Score


def test_simple_score():

    test_note = Note(duration=4, octave=8, pitch_class=2)
    test_notelist = NoteList([test_note, test_note])
    test_notelist.getList()

    score = Score(score_parts=[test_notelist])

    musicxml_score = score._convert_score_parts_to_xml()

    expected_score = '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">\n<score-partwise version="3.0"><part-list><score-part id="P1"><part-name/></score-part></part-list><part id="P1"><measure number="1"><attributes><divisions>1</divisions><key><fifths>0</fifths><mode>none</mode></key><time><beats>4</beats><beat-type>4</beat-type></time><clef><sign>G</sign><line>2</line></clef></attributes></measure><measure number="2"><note><pitch><step>D</step><alter>0</alter><octave>8</octave></pitch><duration>4</duration><accidental>natural</accidental></note></measure><measure number="3"><note><pitch><step>D</step><alter>0</alter><octave>8</octave></pitch><duration>4</duration><accidental>natural</accidental></note></measure></part></score-partwise>'

    assert etree.tostring(musicxml_score).decode('utf-8') == expected_score
