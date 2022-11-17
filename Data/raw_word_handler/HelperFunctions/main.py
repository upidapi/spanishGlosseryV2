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


# not tested
def get_start_points(data):
    temp_list = ChainStatement('o', *data)
    possibilities = get_next_open([0, 0], temp_list)
    # remove the 'o' from the pointer
    return [possible[1:] for possible in possibilities]


# not tested
def map_to_all(func, data, pointer=None):
    if pointer is None:
        pointers = get_start_points(data)
    else:
        pointers = get_next_open(pointer, data)

    for pointer in pointers:
        pointer_data = get_next_open(pointer, data)
        if type(pointer_data) is str:
            print(pointer, get_next_open(pointer, data))
            # set_pointer_data(func(pointer), pointer, data)
        else:
            map_to_all(func, data, pointer)


def main():
    # todo add tests
    data = ChainStatement('hello', '',
                          OrStatement('Im',
                                      ChainStatement('I', ' ', '', 'am')),
                          OrStatement('red', 'blue'),
                          OrStatement('rn', ''))

    print(get_next_open([0, 2], data))


if __name__ == '__main__':
    main()
