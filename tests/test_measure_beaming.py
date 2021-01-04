import pytest

from py2musicxml.notation import Measure, Note

BASE_MEASURE_FACTOR = 4

def test_measure_beaming_simple():

    dur = 1

    middle_c = Note(dur,4,0)

    time_signature = (4,4)

    m = Measure(time_signature, 4)

    for n in [middle_c for x in range(4)]:
        m.add_note(n)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 4

        for note in beat.notes:
            assert note.dur == dur

def test_eighth_note_beams():

    eighth_note_c = Note(0.5,4,0)

    time_sig = (4,4)
    measure_factor = 4 # will be called by Part

    m = Measure(time_sig, measure_factor)

    for note in [eighth_note_c for x in range(8)]:
        m.add_note(note)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 4
        for idx, note in enumerate(beat.notes):
            assert note == eighth_note_c
            if idx % 2 == 0:
                assert note.beam_start
            else:
                pass

    assert len(m.beats) == m.time_signature[0]

def test_five_sixteenths():

    five_sixteenths_c = Note(1.25, 4, 0)

    time_sig = (4,4)
    measure_factor = 4

    m = Measure(time_sig, measure_factor)

    m.add_note(five_sixteenths_c)

    m.clean_up_measure()

    assert m.beats[0].notes[0].dur == 4
    assert m.beats[1].notes[0].dur == 1

def test_half_note_multibeat():

    half_note_c = Note(2, 4, 0)

    time_sig = (4,4)
    measure_factor = 4

    m = Measure(time_sig, measure_factor)

    m.add_note(half_note_c)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 4

    assert m.beats[0].multi_beat == True
    assert m.beats[0].notes[0].dur == 2

def test_quarter_half_multibeat():

    quarter_note_c = Note(1, 4, 0)
    half_note_d = Note(2, 4, 2)

    time_sig = (4,4)
    measure_factor = 4

    m = Measure(time_sig, measure_factor)

    m.add_note(quarter_note_c)
    m.add_note(half_note_d)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 4

    assert m.beats[0].multi_beat == False
    assert m.beats[0].notes[0].dur == 1
    assert m.beats[0].notes[0].pc == 0

    assert m.beats[1].multi_beat == True
    assert m.beats[1].notes[0].dur == 2
    assert m.beats[1].notes[0].pc == 2
