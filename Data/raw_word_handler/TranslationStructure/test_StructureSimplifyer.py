import unittest

from StructureSimplifyer import *
from Data.raw_word_handler.Helpers import ChainStatement, OrStatement


class StrCombine(unittest.TestCase):
    def test_combines_correctly(self):
        out = str_combine(ChainStatement("abc", " def ", "ghj"), False)
        equals = ('hello wut waa', False)
        self.assertEqual(out, equals)

    def test_does_not_combine_ChainStatement(self):
        out = str_combine(ChainStatement("abc", ChainStatement(" def "), "ghj"), False)
        equals = (ChainStatement(OrStatement('abc'), " def ", "ghj"), False)
        self.assertEqual(out, equals)

    def test_does_not_combine_OrStatement(self):
        out = str_combine(ChainStatement(OrStatement('abc'), " def ", "ghj"), False)
        equals = (ChainStatement(OrStatement('abc'), " def ", "ghj"), False)
        self.assertEqual(out, equals)

class DeChain(unittest.TestCase):
    def combines_correctly(self):
        pass

if __name__ == '__main__':
    unittest.main()
