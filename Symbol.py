import re


def parse_sequence(sequence):
    symbol_pattern = r'([A-Za-z+\-\[\]<>])(?:\((.*?)\))?'
    symbols = []

    for match in re.finditer(symbol_pattern, sequence):
        name = match.group(1)
        raw_params = match.group(2)

        if raw_params:
            params = [
                float(p.strip()) for p in raw_params.split(',')
            ]
        else:
            params = []

        symbols.append(Symbol(name, params))
    return symbols


class Symbol:
    def __init__(self, name, params=None):
        self.name = name
        self.params = params or []
