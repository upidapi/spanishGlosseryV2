def get_pointer_data(pointer, data):
    scope = data
    for part in pointer:
        # might be unnecessary
        if scope == '':
            return ''
        else:
            scope = scope[part]
    return scope


def get_sub_starts(pointer, data):
    if pointer is None:
        return []
    else:
        scope = get_pointer_data(pointer, data)

        if type(scope) is str:
            if len(scope) == 0:
                # same thing as checking if scope == ''
                # to be able to skip over empty parts in or statements
                # if it's empty just go to the next part
                return get_next_open_scope(pointer, data)
            elif len(scope) == 1:
                return [pointer]
            else:
                return [pointer + [0]]

        # continue
        elif type(scope) in (list, tuple):
            all_starts = []

            for i in range(len(scope)):
                all_starts += get_sub_starts(pointer + [i], data)

            return all_starts

        else:
            raise 'invalid data'


def get_next_open_scope(pointer, data):
    # there is no next scope (you're at the top scope)
    if not pointer:
        return None
    else:
        pointer_pos = pointer[-1]
        scope = get_pointer_data(pointer[:-1], data)

        if scope == '' or (pointer_pos + 1) == len(scope):
            return get_next_open_scope(pointer[:-1], data)
        else:
            # gets the next non-empty part
            for i in range(pointer_pos + 1, len(scope)):
                next_pos = pointer[:-1] + [i]
                next_sub_starts = get_sub_starts(next_pos, data)
                if next_sub_starts:
                    return next_sub_starts

            return []


def get_all_possibilities(pointers, data):
    all_possibilities = []
    for pointer in pointers:
        all_possibilities += get_next_open_scope(pointer, data)

    return all_possibilities


def get_possible(char, pointers, data):
    all_possibilities = get_all_possibilities(pointers, data)
    possibilities = []

    for possibility in all_possibilities:
        possibility_char = get_pointer_data(possibility, data)
        if char == possibility_char:
            possibilities.append(possibility)

    return possibilities


def check_correct(inp, answers):
    # the check correct always finds next possibility's, so we have to start before the first answer
    answers = tuple(['o'] + list(answers))

    pointers = [[0, 0]]
    for char in inp:
        pointers += get_possible(char, pointers, answers)

        # if there is no possibility it's right
        if not pointers:
            return False

    return True


data = (['är ', ''], '', 'blå')

print(check_correct('blå', data))

# print(get_next_open_scope([0, 0], ('a', ['', '', '2'], 'asd')))
