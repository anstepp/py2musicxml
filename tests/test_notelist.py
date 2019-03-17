import pytest

from py2musicxml import Note, NoteList

TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS = 10, 8, 2


def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        nlist = NoteList()


def test_object_init_success_with_args():
    test_note = Note(TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS)

    nlist = NoteList([test_note, test_note])
