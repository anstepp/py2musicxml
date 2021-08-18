import pytest

import numpy as np
from collections import namedtuple
from math import pi

from py2musicxml.notation import Note, Part, Score, Tempo
from py2musicxml.analysis import AutoTranscribe

peak = namedtuple("peak", ["bin", "freq", "amp", "dur"])

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

def test_parabolic(basic_at, a_440):
    frames = basic_at._transform_x(1024, np.ones(1024))
    for frame in frames:
        for peak in frame:
            assert peak.freq > 0
            assert peak.amp < 0

def test_supply_audio(basic_tempo):

    at = AutoTranscribe(1024, basic_tempo)

    at._supply_audio("test_audio/sine440.wav")

def test_get_pitch(basic_at):
    assert basic_at._get_pitch(259) == (4,0)
    assert basic_at._get_pitch(440) == (4,9)

def test_two_way_mismatch(basic_at):
    basic_at._two_way_mismatch

def test_fft_one_pitch():
    
    N = 2048
    auto_transcribe = AutoTranscribe(N, Tempo(60, 1))

    #print(auto_transcribe.__dict__)

    auto_transcribe._supply_audio("test_audio/violinclip1.wav")

    f0_range = (24, 48)

    resulting_pitches = auto_transcribe.get_note_list(f0_range)

    assert len(resulting_pitches) > 0
    resulting_pitches[0].dur = round(resulting_pitches[0].dur, 2)
    print(len(resulting_pitches))
    assert Note(0.88, 4, 3) == resulting_pitches[0]

def test_smooth_notes():
    
    N = 2048
    auto_transcribe = AutoTranscribe(N, Tempo(60,1))

    auto_transcribe._supply_audio("test_audio/violinclip1.wav")

    f0_range = (24, 48)

    resulting_pitches = auto_transcribe.get_note_list(f0_range)

    indices = auto_transcribe.smooth_notes(resulting_pitches, N)

    assert indices == [3, 7]

    auto_transcribe_2 = AutoTranscribe(N, Tempo(60,1))

    auto_transcribe_2._supply_audio("test_audio/y2monoChunk.wav")

    f0_range = (32, 48)

    resulting_pitches = auto_transcribe_2.get_note_list(f0_range)

    for pitch in resulting_pitches:
        print(pitch)

    indices = auto_transcribe_2.smooth_notes(resulting_pitches, N)

    assert indices == [1, 5, 7]