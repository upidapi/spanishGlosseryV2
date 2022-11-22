import re
from typing import Literal

from Structure.Helpers import ChainStatement, OrStatement


class SplitPatterns:
    """
    >>> re.findall(SplitPatterns.restrictive("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you', 'are/hes']
    >>> re.findall(SplitPatterns.normal("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you', 'are/hes', 'car/bicycle/house']
    >>> re.findall(SplitPatterns.permissive("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you are/hes', 'car/bicycle/house']
    >>> re.findall(SplitPatterns.greedy("/"), "hello im/you are/hes the car/bicycle/house")
    ['im/you are/hes the car/bicycle/house']
    >>> re.findall(SplitPatterns.super_greedy("/"), "hello im/you are/hes the car/bicycle/house")
    ['hello im/you are/hes the car/bicycle/house']
    """

    LARGE_NUMBER = 1000

    @staticmethod
    def mater_function(at, space_tolerance, extra_or_statements):
        wc = f"[^ {at}]+"  # word capture

        return re.compile(
            f"(?:(?<=^)|(?<= ))"  # is at start or starts with " "
            f"{wc}{at}"  # word {split}
            f"(?:(?:{wc} ){{,{space_tolerance}}}"  # captures (extra_words) words
            f"{wc}{at})"  # + one word, new or statement
            f"{{,{extra_or_statements}}}"  # captures (or_statements) or statements
            f"{wc}"  # last word
            f"(?:(?=$)|(?= ))")  # is at end or ends with " "

    @staticmethod
    def restrictive(at):
        return SplitPatterns.mater_function(at, 0, 0)

    @staticmethod
    def normal(at):
        return SplitPatterns.mater_function(at, 0, SplitPatterns.LARGE_NUMBER)

    @staticmethod
    def permissive(at):
        return SplitPatterns.mater_function(at, 1, SplitPatterns.LARGE_NUMBER)

    @staticmethod
    def greedy(at):
        return SplitPatterns.mater_function(at, SplitPatterns.LARGE_NUMBER, SplitPatterns.LARGE_NUMBER)

    @staticmethod
    def super_greedy(at):
        return re.compile(f".+{at}.+")

    @staticmethod
    def test_all(at, test_str):
        exclusions = ["__", "test_all", "mater_function"]
        valid = [func for func in dir(SplitPatterns)
                 if callable(getattr(SplitPatterns, func))
                 and not any(func.startswith(exclude) for exclude in exclusions)]

        for func in valid:
            print(func, re.findall(getattr(SplitPatterns, func)(at), test_str))


def get_split(inp, pattern: Literal['restrictive', 'normal', 'permissive', 'greedy', 'super_greedy'], at):
    """
    splits the inp into ChainStatement(str, OrStatement(str, ...), str ...)
    :param inp:
    :param pattern:
    :param at:
    :return:
    """
    out = []
    last_end = 0
    pattern = getattr(SplitPatterns, pattern)(at)
    temp = re.finditer(pattern, inp)
    for match in temp:
        out.append(inp[last_end:match.span()[0]])
        last_end = match.span()[1]
        out.append(OrStatement(
                *re.split(f"{at}", match.group(0))))

# x=^[*[^['he', *['im', '']*, *['you', '']*]^, '']*]^

    out.append(inp[last_end:])
    return ChainStatement(*out)
