class Card:
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10,
              "A": 0}

    def __init__(self, symbol, suit: str):
        self.suit = suit
        str_symbol = str(symbol)
        assert str_symbol in self.values, str_symbol + " not found in known card symbols"
        self.symbol = str_symbol

    def value(self, high=True) -> int:
        if self.symbol == "A":
            return 11 if high else 1
        return self.values[self.symbol]

    def __str__(self):
        return self.symbol + " " + self.suit
