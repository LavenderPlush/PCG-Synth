import numpy as np


class ADSR:
    def __init__(self, attack, decay, sustain_level, release):
        self.attack = attack
        self.decay = decay
        self.sustain_level = sustain_level
        self.release = release

    def envelope(self, note_duration, sample_rate):
        a = int(self.attack * sample_rate)
        d = int(self.decay * sample_rate)
        r = int(self.release * sample_rate)

        sustain_time = max(0, note_duration - self.attack - self.decay)

        s = int(sustain_time * sample_rate)

        attack = np.linspace(0, 1, a)

        decay = np.linspace(1, self.sustain_level, d)

        sustain = np.full(s, self.sustain_level)

        release = np.linspace(self.sustain_level, 0, r)

        return np.concatenate([
            attack,
            decay,
            sustain,
            release
        ])
