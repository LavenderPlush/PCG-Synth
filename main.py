from LSystem import SimpleLS as SLS
from LSInterpreter import SimpleInterpreter as SI

SAMPLE_RATE = 44100


def main():
    rules = {
        'F': 'F[-F]F[+F][F]'
    }

    ls = SLS(rules)
    sequence = ls.generate('F', 3)

    interpreter = SI()
    interpreter.interpret(sequence)
    interpreter.play()
    # interpreter.track.write('TestLSystemSimple')


if __name__ == '__main__':
    main()
