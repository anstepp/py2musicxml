import pytest

from py2musicxml.notation import Measure, Note


def test_measure_beaming_simple():

    middle_c = Note(1,4,0)

    time_signature = (4,4)

    m = Measure(time_signature, 4)

    for n in [middle_c for x in range(4)]:
        m.add_note(n)

    m.clean_up_measure()

    for beat in m.beats:
        assert beat.subdivisions == 4

        for note in beat.notes:
            assert note == middle_c

def test_eighth_note_beams():

    eighth_note_c = Note(0.5,4,0)

    note_list = [eighth_note_c for x in range(8)]

    time_sig = (4,4)
    measure_factor = 4 # will be called by Part

    m = Measure(time_sig, measure_factor)

    for note in note_list:
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
