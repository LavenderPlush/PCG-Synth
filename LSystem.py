class LSystem:
    def __init__(self, grammar):
        self.grammar = grammar

    def generate(self, sequence: str, iterations: int):
        if iterations == 0:
            return sequence

        return self.generate(
            ''.join((self.grammar.get(s) or s) for s in sequence), iterations - 1)
