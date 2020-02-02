import math
import numpy as np

from math import log2, pow

from scipy.io import wavfile
from scipy.signal import blackmanharris, find_peaks


filename = "sine440.wav"

fs, data = wavfile.read(filename)

sig = np.array(data)

Nsig = len(sig)
print(Nsig)

windowed = sig * blackmanharris(Nsig)

real_part = np.fft.rfft(windowed)

true_i = np.argmax(abs(real_part))

freq = fs * true_i / Nsig

L = 2048

M = L
Nfft = M / 2
print(Nfft)
M = Nfft - L
print(M)
R = M 
Nframes = math.floor((Nsig-M)/R)
print(Nframes)

y = np.zeros(Nsig + Nfft)

for m in range(Nsig):
    start_index = m * R + 1 
    end_index = min([m*R+M, Nsig])
    xm = sig[start_index:end_index]
    zp = np.zeros(Nfft - len(xm))
    xmzp = xm + zp
    Xm = np.fft.fft(xmzp)
    current_peak = np.argmax(abs(Xm))
    current_peak_freq = fs * current_peak / Nsig
    print(current_peak_freq)
    Ym = Xm
    ym = np.fft.ifft(Ym)
    start_outindex = m*R+1
    end_outindex = m*R+Nfft
    y[start_outindex:end_outindex] = y[start_outindex:end_outindex] + ym


A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def pitch(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

