from Data.raw_word_handler.TranslationStructure import \
    get_split, \
    make_between_optional, \
    SplitPatterns
from Data.raw_word_handler.Helpers import map_to_all, ChainStatement

inp = ChainStatement("(el/la) moto es verde/rojo (ue); im blue xd")
# print(get_split(inp, ))
y = lambda x: get_split(inp[x], 'super_greedy', ';')
map_to_all(y, inp)
print(inp)

y = lambda x: make_between_optional(inp[x], ('\(', '\)'))
map_to_all(y, inp)
print(inp)

y = lambda x: get_split(inp[x], 'normal', '/')
map_to_all(y, inp)
print(inp)
