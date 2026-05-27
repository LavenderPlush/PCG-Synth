import time

import numpy as np
import math


def calc_note(note):
    return 2**(note/12)*440


def _generate_wavetable(waveform, length=64):
    wave_table = np.zeros((length,))

    for n in range(length):
        wave_table[n] = waveform(2 * np.pi * n / length)

    return wave_table


class Waveform:
    SINE = np.sin
    SAWTOOTH = lambda x: (x + np.pi) / np.pi % 2 - 1


class Synthesizer:
    def __init__(self, waveform=Waveform, sample_rate=44100):
        self._wavetable = _generate_wavetable(waveform)
        self._sample_rate = sample_rate
        self._gain = -20

    def set_waveform(self, waveform):
        self._wavetable = _generate_wavetable(waveform)

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def set_gain(self, gain):
        self._gain = gain

    def play(self, frequency, t):
        num_samples = math.ceil(t * self._sample_rate)
        wt = self._wavetable
        wt_length = len(wt)

        index_increment = frequency * wt_length / self._sample_rate

        indices = (np.arange(num_samples) * index_increment) % wt_length

        i0 = np.floor(indices).astype(np.int32)
        i1 = (i0 + 1) % wt_length

        frac = indices - i0

        output = wt[i0] + frac * (wt[i1] - wt[i0])

        amplitude = 10 ** (self._gain / 20)
        output *= amplitude

        return output
