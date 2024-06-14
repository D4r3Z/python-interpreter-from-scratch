from abc import ABC, abstractmethod
from io import IOBase


class ILexer(ABC):
    @abstractmethod
    def make_tokens(self, any_inp: IOBase) -> None:
        raise NotImplementedError
