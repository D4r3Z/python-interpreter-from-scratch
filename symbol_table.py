"""symbol table for storing variables while programm is working."""

from typing import Any


class SymbolTable:
    def __init__(self) -> None:
        self.symbols = {}

    def get(self, name: str) -> Any:  # noqa: ANN401
        return self.symbols.get(name)

    def set(self, name: str, link: object) -> None:
        self.symbols.update({name: link})

    def remove(self, name: str) -> None:
        self.symbols.pop(name, None)
