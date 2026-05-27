import Synthesizer as Sy
import Track as Tr
from ADSR import ADSR


class State:
    def __init__(self, time=0.0, note=0, length=0):
        self.time = time
        self.note = note
        self.octave = 0
        self.length = length


class LSInterpreter:
    def __init__(self):
        self.synth = Sy.Synthesizer(waveform=Sy.Waveform.SINE, sample_rate=44100)
        self.track = Tr.Track(sample_rate=44100)

    def interpret(self, sequence):
        raise NotImplementedError

    def play(self):
        self.track.play()


class SimpleInterpreter(LSInterpreter):
    """ Simple interpretation of LSystem sequence, no graphical mapping

    Translation:
        time    sequential, F is equivalent to playing for 1 second
        tone    branching, direction is up and down, but kept within scale
    """

    def __init__(self, scale=None):
        super(SimpleInterpreter, self).__init__()
        if scale is None:
            scale = [0, 2, 4, 5, 7, 9, 11]
        self.scale = scale

    def interpret(self, sequence):
        adsr = ADSR(0.3, 0.1, 1.0, 0.4)
        states = [State(0.0, 0)]
        character = 0

        while character < len(sequence):

            match (sequence[character]):
                case 'F':
                    states[-1].length += 1.0
                case '[':
                    self.synth.set_gain(self.synth._gain - 8)
                    states.append(State(states[-1].time + states[-1].length, states[-1].note))
                case '+':
                    states[-1].note += 2
                case '-':
                    states[-1].note -= 2
                case ']':
                    note = Sy.scale_note(states[-1].note, self.scale)

                    self.track.append_signals_at_time([
                        self.synth.play(Sy.calc_note(note), states[-1].length / (len(states) / 2), adsr)
                    ], states[-1].time)
                    states.pop()
                    self.synth.set_gain(self.synth._gain + 8)
                case _:
                    ...
            character += 1
        note = Sy.scale_note(states[-1].note, self.scale)
        self.track.append_signals_at_time([
            self.synth.play(Sy.calc_note(note), states[-1].length, adsr)
        ], states[-1].time)
