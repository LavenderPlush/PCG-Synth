class LSystem:
    def __init__(self, rules):
        self.rules = rules

    def generate(self, sequence: str, iterations: int):
        raise NotImplementedError


class SimpleLS(LSystem):

    def generate(self, sequence: str, iterations: int):
        if iterations == 0:
            return sequence

        return self.generate(
            ''.join((self.rules.get(s) or s) for s in sequence), iterations - 1)
