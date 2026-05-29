from Symbol import Symbol
from Rule import Rule


class LSystem:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def generate(self, sequence: list[Symbol], iterations: int):
        raise NotImplementedError


class SimpleLS(LSystem):
    def generate(self, sequence: list[Symbol], iterations: int):
        if iterations == 0:
            return sequence

        new_sequence = []

        for symbol in sequence:
            success = False

            for rule in self.rules:
                if rule.match(symbol):
                    new_sequence.extend(rule.apply(symbol))
                    success = True
                    break

            if not success:
                new_sequence.append(symbol)

        return self.generate(new_sequence, iterations - 1)
