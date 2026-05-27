import math

import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav


def _extend_start(signal, amount):
    silence = np.zeros((math.ceil(amount),))
    return np.append(silence, signal)


def _extend_end(signal, amount):
    silence = np.zeros((math.ceil(amount),))
    return np.append(signal, silence)


class Track:
    def __init__(self, sample_rate):
        self._sample_rate = sample_rate
        self.track = np.empty(0)
        self.current_time = 0.0

    def append_signals(self, signals):
        signal_sum = sum(signals)
        self.track = np.append(self.track, signal_sum)

    def append_signals_at_time(self, signals, time):
        signal_sum = sum(signals)
        samples = self._sample_rate * time
        signals_at_time = _extend_start(signal_sum, samples)

        if signals_at_time.shape[0] > self.track.shape[0]:
            time_diff = (signals_at_time.shape[0] - self.track.shape[0])
            self.track = _extend_end(self.track, time_diff)
        elif signals_at_time.shape[0] < self.track.shape[0]:
            time_diff = (self.track.shape[0] - signals_at_time.shape[0])
            signals_at_time = _extend_end(signals_at_time, time_diff)

        self.track = sum([signals_at_time, self.track])

    def play(self):
        sd.play(self.track)
        sd.wait()

    def write(self, name):
        wav.write('exports/' + name + '.wav', self._sample_rate, self.track.astype(np.float32))
