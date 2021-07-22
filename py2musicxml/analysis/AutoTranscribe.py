from math import log2, ceil, floor

import numpy as np
import scipy.io.wavfile as scwav

import py2musicxml.log as logger
log = logger.get_logger()

class AutoTranscribe:

    def __init__(self, N, fs):
        self.array = None
        try:
            if ceil(log2(N)) == floor(log2(N)):
                self.N = N
        except ValueError as e:
            log.error(f"N must be power of two not {N}")
            raise
        self.fs = fs

    def supply_audio(self, fname):
        try:
            self.fs, self.audio = scwav.read(fname)
            self.filedur = len(self.audio)
        except FileNotFoundError as e:
            log.error(e)
            raise

    def transform_x(self, zpf):
        start = 0
        zp = np.zeros((zpf-1)*self.N)
        for stop in range(self.N,self.filedur+1,self.N):
            x = self.audio[start:stop]
            log.warning(type(x), type(zp))
            xzp = np.concatenate(x, zp)
            start = stop
            try:
                X = np.fft.fft(xzp)
            except:
                log.error("No audio")
                raise
