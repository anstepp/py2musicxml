import pytest

import numpy as np

from py2musicxml.notation import Note
from py2musicxml.analysis import AutoTranscribe

@pytest.fixture
def a_440():
    fs = 44100
    t = np.linspace(0, 2.0, int(2.0*fs), endpoint=False)
    sin_440 = a * np.sin(2*np.pi*440*t)
    return sin_440

@pytest.fixture
def basic_at():
    fs = 44100
    N = 4096
    at = AutoTranscribe(N)
    return at

def test_init_estimator():

    at = AutoTranscribe(2)

    assert at

    with pytest.raises(ValueError):
        at_fail = AutoTranscribe(3)

def test_supply_audio():

    at = AutoTranscribe(1024)

    at.supply_audio("test_audio/sine440.wav")

def test_fft(basic_at):

    at = basic_at

    at.supply_audio("test_audio/sine440.wav")

    resulting_pitches = at.get_peak_pitches()

    assert len(resulting_pitches) > 0
    assert Note(30, 5, 9) == resulting_pitches[0]




 