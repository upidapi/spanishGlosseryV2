"""
makes a structure that the check_correct.py can use to check if a word was spelled right

to do this it uses the following parts
    ChainStatement() => [] => chain statement
        # used manly to chain 'or statements' and 'text statements'

        [a, b, c]
        if you're at 'a' you have to go to next 'b'
        you always have to go to the next index

    OrStatement() => {} => or statement
        [x, {a, b, c}, y]
        if you're at 'x' you have to go to 'a', 'b' or 'c'
        if you're at 'a', 'b' or 'c' you have to go to y

        when entering you can go to any index (in the list) when entering
        when exiting you have to go to after the list

using these we can also create
    optionals => {'optional text', ''}
        a part that doesn't have to be typed but can be (if you start you can't end)

    or => {'text 1', 'text 2'}
        an or statement (se more above)

    full_sheet => [{'text 1', ''}, 'text 2', {'text 3', 'text 4'}, 'text 4'] # (e.g)
                   ^^^^^^^^^^^^^^  ^^^^^^^
                      optional
"""


from Structure.Constructor import \
    get_split, \
    make_between_optional, \
    simplify, \
    make_optional

from Structure.Helpers import map_to_all, ChainStatement


def convert(inp):
    optionals = ("/ue/", "/ie/")
    super_splits = (";",)
    or_splits = ("/",)
    between_optionals = (("\(", "\)"),)

    inp = ChainStatement(inp)

    # splits the input into parts at all "super_greedy"
    for option in super_splits:
        def foo(x):
            return get_split(inp[x], 'super_greedy', option)
        map_to_all(foo, inp)

    # makes all "optionals" optional
    for option in optionals:
        def foo(x):
            return make_optional(inp[x], option)
        map_to_all(foo, inp)

    # makes OrStatements at all "normal"
    for option in or_splits:
        def foo(x):
            return get_split(inp[x], 'normal', option)
        map_to_all(foo, inp)

    # makes all between "between_optionals" optional
    for option in between_optionals:
        def foo(x):
            return make_between_optional(inp[x], option)
        map_to_all(foo, inp)

    return simplify(inp)


# print(convert("(he(im)(you))"))
# print(convert("hello (he( im)( you)) wa; likes"))
# print(convert("abc /ue/; likes /ie/"))
# convert("hello/hi; likes").multi_line_print()
# convert("hello/hi (he( im)( you)) wa /ue/; likes /ie/").multi_line_print()
