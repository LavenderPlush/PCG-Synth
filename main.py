import time

from Synthesizer import calc_note
from Synthesizer import Waveform as wf
from Synthesizer import Synthesizer as Synth
from LSystem import LSystem as LS
import Track

SAMPLE_RATE = 44100


def main():
    synth = Synth(wf.SINE, SAMPLE_RATE)
    track = Track.Track(SAMPLE_RATE)

    grammar = {
        'F': 'F[-F]F[+F][F]'
    }

    ls = LS(grammar)
    print(ls.generate('F', 3))


if __name__ == '__main__':
    main()
