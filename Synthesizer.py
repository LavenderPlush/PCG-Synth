import numpy as np
import math


def scale_note(index, scale):
    scale_len = len(scale)

    octave = math.floor(index / scale_len)
    degree = index % scale_len

    return scale[degree] + octave * 12


def _generate_wavetable(waveform, length=64):
    wave_table = np.zeros((length,))

    for n in range(length):
        wave_table[n] = waveform(2 * np.pi * n / length)

    return wave_table


class Waveform:
    SINE = np.sin
    SAWTOOTH = lambda x: (x + np.pi) / np.pi % 2 - 1


class Synthesizer:
    def __init__(self, waveform=Waveform, sample_rate=44100, base_note=220):
        self._wavetable = _generate_wavetable(waveform)
        self._sample_rate = sample_rate
        self._gain = -20
        self._base_note = base_note

    def set_waveform(self, waveform):
        self._wavetable = _generate_wavetable(waveform)

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def get_sample_rate(self):
        return self._sample_rate

    def adjust_gain(self, gain):
        self._gain += gain

    def set_base_note(self, frequency):
        self._base_note = frequency

    def get_base_note(self):
        return self._base_note

    def calc_note(self, note):
        return 2 ** (note / 12) * self._base_note

    def play(self, frequency, note_length, adsr=None):
        wt = self._wavetable
        wt_length = len(wt)

        index_increment = frequency * wt_length / self._sample_rate

        if adsr is None:
            num_samples = math.ceil(note_length * self._sample_rate)
            env = None
        else:
            env = adsr.envelope(note_length, self._sample_rate)
            num_samples = len(env)

        indices = (np.arange(num_samples) * index_increment) % wt_length

        i0 = np.floor(indices).astype(np.int32)
        i1 = (i0 + 1) % wt_length
        frac = indices - i0

        output = wt[i0] + frac * (wt[i1] - wt[i0])

        output *= 10 ** (self._gain / 20)

        if env is not None:
            output *= env

        return output.astype(np.float32)
