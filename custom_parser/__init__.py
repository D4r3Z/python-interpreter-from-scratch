"""Custom parser for token analyzation of input tokens."""

from .interface import IParser
from .parser import Parser

__all__ = ["Parser", "IParser"]
