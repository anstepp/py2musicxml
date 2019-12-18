import pytest

from py2musicxml.notation import Measure


def test_object_init_fail_without_args():
    with pytest.raises(TypeError) as e:
        m = Measure()


def test_object_init_success_with_args():
    time_sig = (4, 4)

    m = Measure(time_signature=time_sig)

    assert m.time_signature == time_sig
    assert m.is_empty() == True


@pytest.mark.parametrize(
    "time_signature, expected_meter_division, expected_meter_type, expected_meter_map",
    [
        ((4, 4), 'Quadruple', 'Simple', [1, 1, 1, 1]),
        ((3, 4), 'Triple', 'Simple', [1, 1, 1]),
        ((2, 4), 'Duple', 'Simple', [1, 1]),
        ((12, 8), 'Quadruple', 'Compound', [1, 1, 1, 1]),
        ((3, 8), 'Triple', 'Simple', [1, 1, 1]),
        ((2, 16), 'Duple', 'Simple', [1, 1]),
        ((6, 8), 'Duple', 'Compound', [1, 1]),
    ],
)
def test_create_measure_map(
    time_signature, expected_meter_division, expected_meter_type, expected_meter_map
):
    m = Measure(time_signature=time_signature)

    assert m.meter_division == expected_meter_division
    assert m.meter_type == expected_meter_type
    assert m.measure_map == expected_meter_map


@pytest.mark.parametrize(
    "time_signature, expected_cumulative_beats, expected_total_cumulative_beats",
    [
        # fmt: off
        ((4, 4), [1, 2, 3, 4], 4),
        ((3, 4), [1, 2, 3], 3),
        ((2, 4), [1, 2], 2),
        ((12, 8), [1, 2, 3, 4], 4),
        ((3, 8), [1, 2, 3], 3),
        ((2, 16), [1, 2], 2),
        ((6, 8), [1, 2], 2),
        # fmt: on
    ],
)
def test_cumulative_beats(
    time_signature, expected_cumulative_beats, expected_total_cumulative_beats
):
    m = Measure(time_signature=time_signature)

    assert m.cumulative_beats == expected_cumulative_beats
    assert m.total_cumulative_beats == expected_total_cumulative_beats
