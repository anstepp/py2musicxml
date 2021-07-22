import pytest

from py2musicxml.notation import Tempo, Measure, Score

@pytest.fixture
def basic_tempo():
    bpm = 60
    note = 1 # quarter
    tempo = Tempo(bpm, note)
    return tempo, bpm, note

@pytest.fixture
def basic_score():
    time_sig = [(4,4)]
    measures = [m.Measure(time_sig, 1) for x in range(5)]
    test_part = Part(measures)
    score = Score([test_part])


def test_tempo_init(basic_tempo):
    tempo, bpm, note = basic_tempo
    assert tempo.tempo == bpm
    assert tempo.note_value == note
    assert tempo.measure == 1

def test_set_tempo(basic_tempo):
    tempo, bpm, note = basic_tempo
    new_bpm = 120
    new_note = 2 # half note
    tempo.set_tempo(new_bpm, new_note)
    assert tempo.tempo == new_bpm
    assert tempo.note_value == new_note

def test_set_measure(basic_tempo):
    tempo, bpm, note = basic_tempo
    new_m = 3
    tempo.set_measure(new_m)
    assert tempo.measure == new_m