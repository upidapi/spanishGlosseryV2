from Data.raw_word_handler.HelperFunctions.custom_pointer_list \
    import OrStatement, ChainStatement


def get_sub_possible(pointers: list[list[int]], data):
    possible = []
    for pointer in pointers:
        scope = data[pointer]

        if type(scope) is OrStatement:
            for i in range(len(scope)):
                possible += get_sub_possible([pointer + [i]], data)
        elif len(scope) == 1 and type(scope) is str:
            possible.append(pointer)
        elif not scope:
            # if it's empty get next thing instead
            possible += get_next_open(pointer, data)
        else:
            # continue down
            possible += get_sub_possible([pointer + [0]], data)

    return possible


def get_next_open(pointer, data):
    if not pointer:
        return []
    scope = data[pointer[:-1]]
    # go upp if at last place in scope or OrEscape
    if pointer[-1] == len(scope) - 1 \
            or type(data[pointer]) is OrStatement:
        return get_next_open(pointer[:-1], data)

    next_thing = pointer[:-1] + [pointer[-1] + 1]
    return get_sub_possible([next_thing], data)


# todo add tests
# data = ChainStatement('a', OrStatement(ChainStatement('', 'wc')))
# print(get_next_open([0], data))
