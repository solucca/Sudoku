from random import choice

class Field:
    def __init__(self, line, column) -> None:
        self.possible = set()
        self.final = None
        self.line = line
        self.column = column
        self.type = "anchor"

    def __str__(self) -> str:
        if self.final:
            if self.type == "anchor":
                return "\x1B[1;32m"+str(self.final)+"\x1B[0m "
            if self.type == "final":
                return "\x1B[1;33m"+str(self.final)+"\x1B[0m "
        if len(self.possible) > 0:
            return "\x1B[3m"+str(len(self.possible))+"\x1B[0m "
        return "_ "
    
    def __repr__(self) -> str:
        return f"{self.line},{self.column}:{self.possible}"
    
    def setAnchor(self, value: int):
        self.final = value
        self.possible = {value}
        self.type = "anchor"

    def update_state(self):
        if len(self.possible) == 1:
            self.final = tuple(self.possible)[0]
            self.type = "final"
        if len(self.possible) > 1:
            self.final = None
            self.type = "possible"

    def colapse(self):
        self.possible = choice(tuple(self.possible))
        self.update_state()
