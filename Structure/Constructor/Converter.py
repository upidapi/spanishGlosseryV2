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


def super_option_func_map(inp, options, foo: callable):
    """
    maps all options to foo which is mapped to inp
    also re.escapes() all options
    """
    for option in options:
        # sanitise options so that regex doesn't mishandle the "option"
        if type(option) is str:
            option = re.escape(option)
        elif type(option) is tuple:
            temp_list = []
            for part in option:
                if type(part) is str:
                    temp_list.append(re.escape(part))
                else:
                    temp_list.append(part)
            option = tuple(temp_list)

        def option_func(x):
            return foo(x, option)
        map_to_all(option_func, inp)


# todo add "any" support
#  eg "hello ... im blue"
#  would accept "hello ", {any combination of characters}, " im blue"
#  might use notation ("hello ", any, " im blue")
#  candidates => "...", "x"

# is done to do add replace support
#  (args: "o, -a, -as, -os", ["o", "a", "os", "as"])
#  eg bienvenido, -a, -as, -os =>
#  ("bienvenid", ["o", "a", "os", "as"])
#  candidates => "a, -n", "o, -a", "o, -a, -as, -os"

# todo make it so you never have to type mre than one space in a row
#  eg "  " => " "

def convert(inp: str):
    # todo make optionals, super_splits etc changeable

    optionals = ("/ue/", "/ie/", "/de/", "...")  # the "..." is temporary
    super_splits = (";",)
    or_splits = ("/", ",")
    between_optionals = (("(", ")"),)
    replaces = ((
                   "a, -n",
                   OrStatement("a", "n")),
                (
                   "o, -a, -as, -os",
                   OrStatement("o", "a", "os", "as")),
                (
                   "o, -a",
                   OrStatement("o", "a")),
                )

    inp = inp.lower()
    inp = ChainStatement(inp)

    # splits the input into parts at all "super_greedy"
    super_option_func_map(inp, super_splits, lambda x, option: get_split(inp[x], 'super_greedy', option))
    # replaces everything in replace
    super_option_func_map(inp, replaces, lambda x, option: replace(inp[x], option[0], option[1]))
    # makes all "optionals" optional
    super_option_func_map(inp, optionals, lambda x, option: make_optional(inp[x], option))
    # makes OrStatements at all "normal"
    super_option_func_map(inp, or_splits, lambda x, option: get_split(inp[x], 'permissive', option))
    # makes all between "between_optionals" optional
    super_option_func_map(inp, between_optionals, lambda x, option: make_between_optional(inp[x], option))

    return simplify(inp)


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
