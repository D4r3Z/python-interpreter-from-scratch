from abc import ABC, abstractmethod
from typing import Iterable


class IParser(ABC):
    @abstractmethod
    def parse(self, tokens: Iterable) -> None:
        raise NotImplementedError
