from Structure.TranslationStructure import \
    get_split, \
    make_between_optional, \
    simplify

from Structure.Helpers import map_to_all, ChainStatement


def convert(inp):
    optionals = ("/ue/", "/ie/")
    super_splits = (";",)
    or_splits = ("/",)
    between_optionals = (("\(", "\)"),)

    inp = ChainStatement(inp)

    # makes all "optionals" optional
    for option in optionals:
        def foo(x):
            # todo implement replace
            return inp[x]
        map_to_all(foo, inp)

    # splits the input into parts at all "super_greedy"
    for option in super_splits:
        def foo(x):
            return get_split(inp[x], 'super_greedy', option)
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


print(convert("(he(im)(you))"))
print(convert("hello (he( im)( you)) wa; likes"))
print(convert("hello (he( im)( you)) wa /ue/; likes /ie/"))
