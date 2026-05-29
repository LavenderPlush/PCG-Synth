import random
from typing import Callable

import Symbol


def update_param(symbol: Symbol, param: int, new_value: float):
    if len(symbol.params) - 1 < param:
        return new_value

    return symbol.params[param] * new_value

class Rule:
    def match(self, symbol: Symbol):
        raise NotImplementedError

    def apply(self, symbol: Symbol):
        raise NotImplementedError


class DRule(Rule):
    def __init__(self, symbol_name: str, func: Callable):
        self.symbol_name = symbol_name
        self.func = func

    def match(self, symbol: Symbol):
        return symbol.name == self.symbol_name

    def apply(self, symbol: Symbol):
        return self.func(symbol)


class SRule(Rule):
    def __init__(self, symbol_name: str, choices: list[tuple[Callable, float]]):
        self.symbol_name = symbol_name
        self.choices = [
            (func, weight)
            for func, weight in choices
        ]

    def match(self, symbol):
        return symbol.name == self.symbol_name

    def apply(self, symbol):
        values = [v[0] for v in self.choices]
        weights = [v[1] for v in self.choices]

        func = random.choices(values, weights=weights, k=1)[0]
        return func(symbol)
