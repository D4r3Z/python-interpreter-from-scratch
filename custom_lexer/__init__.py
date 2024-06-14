"""Custom lexer for lexical analyzation of input buffer."""

from .interface import ILexer
from .lexer import Lexer

__all__ = ["Lexer", "ILexer"]
