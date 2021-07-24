import pytest

import numpy as np

from py2musicxml.notation import Note, Part, Score, Tempo
from py2musicxml.analysis import AutoTranscribe

@pytest.fixture
def a_440():
    T = 2.0
    fs = 44100
    t = np.linspace(0, 2.0, int(T*fs), endpoint=False)
    sin_440 = a * np.sin(2*np.pi*440*t)
    return sin_440

@pytest.fixture
def basic_tempo():
    return Tempo(60, 1)

@pytest.fixture
def basic_at(basic_tempo):
    fs = 44100
    N = 4096
    at = AutoTranscribe(N, basic_tempo)
    return at

def test_init_estimator(basic_tempo):

    at = AutoTranscribe(2, basic_tempo)

    assert at

    with pytest.raises(ValueError):
        at_fail = AutoTranscribe(3, 60)

# def test_supply_audio(basic_tempo):

#     at = AutoTranscribe(1024, basic_tempo)

#     at.supply_audio("test_audio/sine440.wav")

# def test_fft_one_pitch():
    
#     N = 4096
#     auto_transcribe = AutoTranscribe(N, Tempo(30, 1))

#     auto_transcribe.supply_audio("test_audio/sine440.wav")

#     resulting_pitches = auto_transcribe.get_peak_pitches()

#     assert len(resulting_pitches) > 0
#     assert Note(29.907, 4, 9) == resulting_pitches[0]

#     time_sig = [(4,4)]

#     test_part = Part(resulting_pitches, time_sig)
#     for note in resulting_pitches:
#         print(note)
#     test_score = Score([test_part])

#     test_score.convert_to_xml("scripts/test440.musicxml")

# def test_viola():

#     test_tempo = Tempo(250, 0.5)

#     at = AutoTranscribe(1024, test_tempo)

#     at.supply_audio("test_audio/y2monoChunk.wav")

#     time_sig = [(4,4)]

#     resulting_pitches = at.get_peak_pitches()

#     test_part = Part(resulting_pitches, time_sig)
#     test_score = Score([test_part])

#     test_score.convert_to_xml("scripts/viola.musicxml")

