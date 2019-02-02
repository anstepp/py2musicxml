from rtcmix import *

rtsetparams(44100, 2)
import random

import playback  # factor, type, inst, generations, upDown, seed

instrumentList = list()


PB1 = playback.playback(0.125, 0, 5, 8, 0.5, 100)
PB2 = playback.playback(0.125, 0, 4, 8, 0.5, 0)
PB3 = playback.playback(0.250, 0, 2, 8, 0.6, 14)
instrumentList = [PB1, PB2, PB3]

for x in range(0, 4):
    y = playback.playback(8, 1, 3, 3, random.random(), x)
    instrumentList.append(y)

for item in instrumentList:
    choice = [0, 2, 4, 5, 7, 9, 11]
    item.play(random.randint(6, 9), random.choice(choice))
