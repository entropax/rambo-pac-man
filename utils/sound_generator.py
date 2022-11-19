import math
import numpy as np
from pygame import mixer, sndarray, time

BITS = 16           # the number of channels specified here is NOT
FREQUENCE = 44100
CHANNELS = 1


mixer.pre_init(FREQUENCE, -BITS, CHANNELS)
mixer.init()

def generate_note():
    pass

def generate_sound(freqency: int=44100, length: float=0.25,) -> np.array:
    sound_array = np.arange(0, length, 1 / freqency)
    for i in range(200, 1600, 25):
        # 0.5 to avoid clipping sound card DAC
        sound = 0.5 * np.sin(2*np.pi*i*sound_array)
        sound = (sound*32768).astype(np.int16)  # scale to int16 for sound card

        sound = sndarray.make_sound(sound)
        print(sound.__sizeof__())

        sound.play()
        time.delay(250)
