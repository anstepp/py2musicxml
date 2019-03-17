import pytest

from py2musicxml import Note

TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS = 10, 8, 2


def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        n = Note()


def test_object_init_success_with_args():
    n = Note(TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS)
    assert n.dur == TEST_DURATION
    assert n.octave == TEST_OCTAVE
    assert n.pc == TEST_PITCH_CLASS


def test_get_step_name():
    test_cases = {
        'no key': {
            'pitch_class': 2,
            'starting_pitch': 0,
            'expected_result': ['D', '0', 'natural'],
        },
        'flat key': {
            'pitch_class': 6,
            'starting_pitch': 5,
            'expected_result': ['G', '-1', 'flat'],
        },
        'sharp key': {
            'pitch_class': 9,
            'starting_pitch': 11,
            'expected_result': ['A', '0', 'natural'],
        },
    }

    for test_case in test_cases.keys():
        n = Note(TEST_DURATION, TEST_OCTAVE, test_cases[test_case]['pitch_class'])
        result = n._get_step_name(test_cases[test_case]['starting_pitch'])
        assert result == test_cases[test_case]['expected_result']

    try:
        n = Note(TEST_DURATION, TEST_OCTAVE, TEST_PITCH_CLASS)
        n._get_step_name(999)
    except Exception as e:
        assert str(e) == 'starting_pitch must be zero, a flat key, or sharp key'
