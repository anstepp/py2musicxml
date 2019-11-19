import pytest

from py2musicxml import Note, Part

TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS = 10, 8, 2

TEST_SIGNATURE = [(4,4)]


def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        nlist = Part()


def test_object_init_success_with_args():
    test_note = Note(TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS)

    nlist = Part([test_note, test_note], TEST_SIGNATURE)


def test_simple_test():
    test_note = Note(2, TEST_OCTAVE, TEST_PITCH_CLASS)
    test_tsig = TEST_SIGNATURE

    nlist = Part([test_note, test_note, test_note, test_note, test_note], test_tsig)

    nlist.get_part()

    assert nlist.currentList == nlist.finalList
