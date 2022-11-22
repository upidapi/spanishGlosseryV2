"""removes unnecessary parts of the structure"""
from Data.raw_word_handler.Helpers import ChainStatement, OrStatement


def one_len_unpack(structure, changed_structure):
    # unpacks unnecessary 1 len statements
    if type(structure) in (ChainStatement, OrStatement):
        temp_list = []
        for part in structure:
            if type(part) in (ChainStatement, OrStatement) and len(part) <= 1:
                # full data
                temp_list += part[[]]
                changed_structure = True
            else:
                temp_list.append(part)
        if type(structure) is ChainStatement:
            structure = ChainStatement(*temp_list)
        if type(structure) is OrStatement:
            structure = OrStatement(*temp_list)

    return structure, changed_structure


def or_combine(structure, changed_structure):
    # combines multiple or statements into one
    if type(structure) is OrStatement:
        temp_list = []
        for part in structure:
            if type(part) is OrStatement:
                temp_list += part[[]]
                changed_structure = True
            else:
                temp_list.append(part)
        return OrStatement(*temp_list), changed_structure
    return structure, changed_structure


def de_chain(structure, changed_structure):
    # remove unnecessary chain statements
    if type(structure) is ChainStatement:
        temp_list = []
        for part in structure:
            if type(part) is ChainStatement:
                # full data
                temp_list += part[[]]
                changed_structure = True
            else:
                temp_list.append(part)
        structure = ChainStatement(*temp_list)
    return structure, changed_structure


def chain_part_combine(structure, changed_structure):
    # merges strs and chain statements when two or more are in a row
    def combine_parts(parts):
        if 2 <= len(streak):
            if type(parts[0]) is ChainStatement:
                return ChainStatement(*[thing for part in parts for thing in part])
            if type(parts[0]) is str:
                return ["".join(parts)]
        else:
            return streak

    if type(structure) is ChainStatement:
        temp_list = []
        streak = []
        streak_type = type(None)
        for part in structure:
            if isinstance(part, streak_type):
                streak.append(part)
                changed_structure = True
            else:
                if type(part) in (ChainStatement, str):
                    streak_type = type(part)
                else:
                    streak_type = type(None)

                temp_list += combine_parts(streak)

                streak = [part]
        temp_list += combine_parts(streak)

        return ChainStatement(*temp_list), changed_structure
    return structure, changed_structure


def space_removal(structure, changed_structure):
    if type(structure) is ChainStatement:
        structure = ChainStatement(*[part for part in structure if part != ""])
    return structure, changed_structure


def duplicate_remove(structure, changed_structure):
    if type(structure) is OrStatement:
        temp_list = []
        for part in structure:
            # todo this doesn't work, it's just a temporary implementation
            #  you cant compare content of two "custom_pointer_list"s
            if part not in temp_list:
                temp_list.append(part)
    return structure, changed_structure


def clean(structure):
    if type(structure) is str:
        return structure

    changed_structure = False
    structure, changed_structure = one_len_unpack(structure, changed_structure)  # X
    structure, changed_structure = or_combine(structure, changed_structure)  # X
    structure, changed_structure = de_chain(structure, changed_structure)  # X
    structure, changed_structure = chain_part_combine(structure, changed_structure)  # X
    structure, changed_structure = space_removal(structure, changed_structure)

    # structure, changed_structure = duplicate_remove(structure, changed_structure)

    if changed_structure:
        return clean(structure)

    for i in range(len(structure)):
        structure[i] = clean(structure[i])

    return structure


# print(de_chain(ChainStatement("abc", ChainStatement("d", "e", "f"), "ghj"), False))
# # (^['abc', 'd', 'e', 'f', 'ghj']^, True)

# print(chain_part_combine(ChainStatement(
#     ChainStatement("watsh"),
#     ChainStatement("tha"),
#     "false",
#     "sd",
#     ChainStatement("watsh"),
#     ChainStatement("tha"),
#     "wut",
#     OrStatement("hell"),
#     OrStatement("no")
# ), False))
# # (^['watsh', 'tha', 'falsesd', 'watsh', 'tha', 'wut', *['hell']*, *['no']*]^, True)

# print(one_len_unpack(ChainStatement(
#     "h",
#     OrStatement('2'),
#     "hello",
#     ChainStatement("as", "asd"),
#     ChainStatement("asd")
# ), False))
# # (^['h', '2', 'hello', ^['as', 'asd']^, 'asd']^, True)

# print(or_combine(OrStatement(OrStatement("2", "3", "4"), OrStatement("as", "a")), False))
# # (*['2', '3', '4', 'as', 'a']*, True)

# print(space_removal(ChainStatement("ad", "", "", "lals", ChainStatement('sda', 'asd')), False))
# # (^['ad', 'lals', ^['sda', 'asd']^]^, False)

# data = ChainStatement("hello",
#                       ChainStatement("blue"),
#                       OrStatement("nah", "that",
#                                   OrStatement("cant", "be")),
#                       "is it",
#                       "",
#                       "",
#                       "ahsdj",
#                       OrStatement('s'),
#                       "asd",
#                       "de")
# print(clean(data))
# # ^['helloblue', *['nah', 'that', 'cant', 'be']*, 'is itahsdjsasdde']^

