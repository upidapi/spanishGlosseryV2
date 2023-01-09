"""
makes a structure that the check_correct.py can use to check if a word was spelled right

to do this it uses the following parts
    ChainStatement() => () => chain statement
        # used manly to chain 'or statements' and 'text statements'

        (a, b, c)
        if you're at 'a' you have to go to next 'b'
        you always have to go to the next index

    OrStatement() => [] => or statement
        (x, [a, b, c], y)
        if you're at 'x' you have to go to 'a', 'b' or 'c'
        if you're at 'a', 'b' or 'c' you have to go to y

        when entering you can go to any index (in the list) when entering
        when exiting you have to go to after the list

using these we can also create
    optionals => ['optional text', '']
        a part that doesn't have to be typed but can be (if you start you can't end)

    or => ['text 1', 'text 2']
        an or statement (se more above)

    full_sheet => (['text 1', ''], 'text 2', ['text 3', 'text 4'], 'text 4') # (e.g)
                   ^^^^^^^^^^^^^^  ^^^^^^^
                      optional
"""
import re

from Structure.Constructor import \
    get_split, \
    make_between_optional, \
    simplify, \
    make_optional, \
    replace

from Structure.Helpers import map_to_all, ChainStatement, OrStatement

# todo add "any" support
#  eg "hello ... im blue"
#  would accept "hello ", {any combination of characters}, " im blue"
#  might use notation ("hello ", any, " im blue")
#  candidates => "...", "x"

# todo make it so you never have to type mre than one space in a row
#  eg "  " => " "


def tuple_re_escape(options):
    escaped = []
    for option in options:
        # sanitise options so that regex doesn't mishandle the "option"
        if type(option) is str:
            escaped.append(re.escape(option))
        elif type(option) in (tuple, OrStatement, ChainStatement):
            escaped.append(tuple_re_escape(option))
        else:
            raise TypeError(f"invalid options ({option})")
    return escaped


def list_func_map(inp, temp: tuple[tuple[callable, tuple], ...]):
    """
    maps all options to foo which is mapped to inp
    """
    for part in temp:
        func = part[0]
        options = part[1]
        options = tuple_re_escape(options)

        for option in options:
            def option_func(x):
                return func(inp[x], option)

            map_to_all(option_func, inp)


class TempName:
    @staticmethod
    def between_greedy(x, option):
        # splits the input into parts at all "super_greedy"
        return get_split(x, 'super_greedy', option)

    @staticmethod
    def between_optional(x, option):
        # makes all between "between_optionals" optional
        return make_between_optional(x, option)

    @staticmethod
    def replace(x, option):
        # replaces everything in replace
        return replace(x, option[0], option[1])

    @staticmethod
    def optional(x, option):
        # makes all "optionals" optional
        return make_optional(x, option)

    @staticmethod
    def between_permissive(x, option):
        # makes OrStatements at all "normal"
        return get_split(x, 'permissive', option)


def convert(inp: str, blueprint):
    # todo make optionals, super_splits etc changeable

    inp = inp.lower()
    inp = ChainStatement(inp)

    # todo add a gui based system for adding and ordering the "TempName" things
    # blueprint ex =>
    # (
    #     (TempName.between_greedy, (";",)),
    #     (TempName.between_optional, (("(", ")"),)),
    #     (TempName.between_permissive, ("/",)),
    #     (TempName.replace, (("a, -n", OrStatement("a", "n")),
    #                         ("o, -a, -as, -os", OrStatement("o", "a", "os", "as")),
    #                         ("o, -a", OrStatement("o", "a")),)),
    #     (TempName.optional, ("/ue/", "/ie/", "/de/", "... ", "de")),
    #     (TempName.between_permissive, (",",)),
    # )

    list_func_map(inp, blueprint)

    return simplify(inp)


# tests
# print(convert("(he(im)(you))"))
# print(convert("hello (he( im)( you)) wa; likes"))
# print(convert("abc /ue/; likes /ie/"))
# print(convert("hello/hi; likes"))
# convert("hello/hi; likes").multi_line_print()
# data = json_load([('abc ', ['/ue/', '']), (' likes ', ['/ie/', ''])])
# print(data)
# data = convert("abc /ue/; likes /ie/")
# print(data)
# data.multi_line_print()
# print(data.json_dump())
# print(convert("hello/hi (he( im)( you)) wa /ue/; likes /ie/"))
# convert("hello/hi (he( im)( you)) wa /ue/; likes /ie/").multi_line_print()
