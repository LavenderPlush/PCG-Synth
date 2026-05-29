from LSystem import SimpleLS as SLS
from Rule import DRule, SRule, update_param as up
from LSInterpreter import SimpleInterpreter as SI
from Symbol import parse_sequence as ps

SAMPLE_RATE = 44100


def main():
    deterministic_rules_1 = [
        DRule('X', lambda x: ps('F[+X][-X]FX')),
        DRule('F', lambda x: ps('FF')),
    ]

    deterministic_rules_2 = [
        DRule('F', lambda x: ps('F[-F]F[+F][F]'))
    ]

    stochastic_rules = [
        SRule('F', [
            (lambda x: ps('F[+F(' + str(up(x, 0, 0.7)) + ')]F[-F(' + str(up(x, 0, 0.6)) + ')]F'), 1.0),
            (lambda x: ps('F[+F(' + str(up(x, 0, 0.7)) + ')]F'), 1.0),
            (lambda x: ps('F[-F(' + str(up(x, 0, 0.7)) + ')]F'), 1.0),
            (lambda x: ps('F(' + str(up(x, 0, 1.5)) + ')'), 0.5),
        ]),
    ]

    ls = SLS(stochastic_rules)
    sequence = ls.generate(ps('F(1)'), 5)

    interpreter = SI()
    interpreter.interpret(sequence)
    interpreter.track.write('parameterized_1')
    #interpreter.play()

if __name__ == '__main__':
    main()
