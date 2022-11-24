import re

from Structure.Helpers import ChainStatement, OrStatement


def replace(inp: str, at: str, to: callable):
    """
    replaces all matches to at (inp) with to(at)
    :param inp: the input
    :param at: regex statement to be matched
    :param to: where "at" is matched it is replaced by to(match)
    """
    out = []
    last_end = 0
    matches = re.finditer(at, inp)
    for match in matches:
        out.append(inp[last_end:match.span()[0]])
        last_end = match.span()[1]
        out.append(to(match.group(0)))

    out.append(inp[last_end:])
    return ChainStatement(*out)


def make_optional(inp: str, at: str):
    """
    :param inp: eg "hello im that .ung"
    :param at: regex statement ex ".ung"
    :return: ChainStatement("hello im that" OrStatement(".ung", ""), "")
    """

    def replace_func(x):
        return OrStatement(x, "")

    return replace(inp, at, replace_func)


