import Synthesizer as Sy
import Track as Tr
from ADSR import ADSR


class State:
    def __init__(self, time=0.0, note=0, length=0):
        self.time = time
        self.note = note
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
    def __init__(self, scale=None):
        super(SimpleInterpreter, self).__init__()
        if scale is None:
            scale = [0, 2, 4, 5, 7, 9, 11]
        self.scale = scale

    def interpret(self, sequence):
        adsr = ADSR(0.3, 0.1, 1.0, 0.4)
        states = [State(0.0, 0)]
        symbol = 0

        while symbol < len(sequence):

            match sequence[symbol].name:
                case 'F':
                    new_length = 1.0
                    if len(sequence[symbol].params) > 0:
                        new_length = sequence[symbol].params[0]
                    states[-1].length += new_length
                case '[':
                    self.synth.adjust_gain(-4)
                    states.append(State(states[-1].time + states[-1].length, states[-1].note))
                case '+':
                    states[-1].note += 2
                case '-':
                    states[-1].note -= 2
                case ']':
                    note = Sy.scale_note(states[-1].note, self.scale)

                    self.track.append_signals_at_time([
                        self.synth.play(self.synth.calc_note(note), states[-1].length / (len(states) / 2), adsr)
                    ], states[-1].time)
                    states.pop()
                    self.synth.adjust_gain(4)
                case _:
                    ...
            symbol += 1
