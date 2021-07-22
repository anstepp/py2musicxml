from math import log2, ceil, floor, log10
from bisect import bisect_left
from tests.test_tempo import test_tempo_init

import numpy as np
import scipy.io.wavfile as scwav

from py2musicxml.notation import Note

import py2musicxml.log as logger
log = logger.get_logger()

A0 = 13.75

def twelve_tet_gen(f0):
    x = 0
    starting_pitch = f0
    next_half_step = f0
    while True:
        yield next_half_step
        next_half_step = (starting_pitch) * (2 ** (1/12))
        x += 1
        starting_pitch = next_half_step

pitchgen = twelve_tet_gen(A0)
TWELVETET = [next(pitchgen) for x in range(128)]

class AutoTranscribe:

    def __init__(self, N, tempo):
        self.array = None

        # Check if N is a power of 2.
        if ceil(log2(N)) == floor(log2(N)):
            self.N = N
        else:
            log.error(f"N ({N}) is not a power of 2")
            raise ValueError("N ({N}) is not a power of 2")
        
        self.tempo = tempo
        self.fs = None

    def supply_audio(self, fname):
        try:
            self.fs, self.audio = scwav.read(fname)
            self.filedur = len(self.audio)
        except FileNotFoundError as e:
            log.error(e)
            raise

    def _bin_peak_freq(self, bin_no, N, zpf, fs):
        return bin_no * fs / (N * zpf)

    def _estimate_offset(self, yn1, y0, y1):
        p = 0.5*(((yn1-y1)/(yn1-2*y0+yn1)))
        return p

    def _transform_x(self, zpf):
        pitch_array = []
        start = 0
        zp = np.zeros((zpf-1)*self.N)
        for stop in range(self.N,self.filedur+1,self.N):
            x = self.audio[start:stop]
            xzp = np.concatenate([x, zp])
            X = np.fft.fft(xzp)
            X_shift = np.fft.fftshift(X)
            half_N = int(np.ceil(np.rint((self.N*zpf)/2)))
            Xr = X_shift[half_N:]
            k_star = np.argmax(abs(Xr))
            y0 = 20*log10(abs(Xr[k_star]))
            yn1 = 20*log10(abs(Xr[k_star-1]))
            y1 = 20*log10(abs(Xr[k_star+1]))
            p = self._estimate_offset(yn1, y0, y1)
            est_peak = (k_star+p)
            freq = self._bin_peak_freq(est_peak, self.N, zpf, self.fs)
            pitch_array.append([freq, self.N/self.fs])
            start = stop
        return pitch_array


    def _get_nearest_tet(self, freq):
        idx = bisect_left(TWELVETET, freq)
        left = TWELVETET[idx]
        right = TWELVETET[idx+1]
        delta_l = freq - left
        delta_r = right - freq
        if delta_l > delta_r:
            return TWELVETET[idx + 1]
        else:
            return TWELVETET[idx]

    def _get_bb_notes(self, fft_note):
        rpitch = round(12 * log2(fft_note[0] / 8.175))
        octave = rpitch // 12
        pc = rpitch % 12
        return Note(round(fft_note[1]), octave, pc)

    def get_peak_pitches(self):
        pitches = self._transform_x(4)
        tranformed_pitches = []
        for pitch in pitches:
            tet_pitch = self._get_nearest_tet(pitch[0])
            tranformed_pitches.append([tet_pitch, pitch[1]])
        combined_pitches = []
        for idx, pitch in enumerate(tranformed_pitches):
            if idx > 0:
                if last_pitch[0] == pitch[0]:
                    combined_pitch[1] += pitch[1]
                else:
                    combined_pitches.append(combined_pitch)
                    last_pitch = pitch
            else:
                last_pitch = pitch
                combined_pitch = pitch 
        combined_pitches.append(combined_pitch) 
        
        bb_notes = []

        for fft_note in combined_pitches:
            bb_notes.append(self._get_bb_notes(fft_note))


        return bb_notes
