import pytest

from py2musicxml import Measure, Beat, Note

TEST_TIME = [(4,4)]
TEST_DUR = 1
TEST_OCTAVE = 4
TEST_PITCH = 0


def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        m = Measure()


def test_object_init_success_with_args():
    m = Measure(time_signature=TEST_TIME)
    assert m.time_signature == TEST_TIME

def test_measure_empty():
    m = Measure(time_signature=TEST_TIME)
    assert not m.notes
    assert not m.beats

def test_measure_equality():
    measure_a = Measure(time_signature=TEST_TIME)
    measure_b = Measure(time_signature=TEST_TIME)
    test_note = Note(duration=TEST_DUR, octave=TEST_OCTAVE, pitch_class=TEST_PITCH)
    measure_a.add_note(test_note)
    measure_b.add_note(test_note)
    measure_c = Measure(time_signature=TEST_TIME)
    

    assert measure_a != measure_b
    assert measure_a != measure_c
    assert not measure_c.beats
    assert not measure_c.notes
