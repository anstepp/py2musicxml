import pytest

from py2musicxml import Pitch, Duration, make_NoteList

TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS = 10, 8, 2


def test_pitch_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        pitch = Pitch()


def test_pitch_init_success_with_args():
    pitch = Pitch(TEST_OCTAVE, TEST_PITCH_CLASS)
    assert pitch.octave == TEST_OCTAVE
    assert pitch.pitch_class == TEST_PITCH_CLASS


def test_duration_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        duration = Duration()


def test_duration_init_success_with_args():
    duration = Duration(TEST_DURATION)
    assert duration.duration == TEST_DURATION
