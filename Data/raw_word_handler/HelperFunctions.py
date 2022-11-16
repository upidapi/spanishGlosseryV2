def get_pointer_data(pointer, data):
    scope = data
    for part in pointer:
        # might be unnecessary
        if scope == '':
            return ''
        else:
            scope = scope[part]
    return scope


def set_pointer_data(new_data, pointer, data):
    full_data = new_data

    for i in list(range(len(pointer)))[::-1]:
        step_up_data = get_pointer_data(pointer[:i], data)
        step_up_data[pointer[i]] = full_data
        full_data = step_up_data

    return full_data


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
                return get_next_open_scopes(pointer, data)
                # return []
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


def get_next_open_scopes(pointer, data):
    # there is no next scope (you're at the top scope)
    if not pointer:
        return None
    else:
        pointer_pos = pointer[-1]
        scope = get_pointer_data(pointer[:-1], data)

        if scope == '' or (pointer_pos + 1) == len(scope):
            return get_next_open_scopes(pointer[:-1], data)
        else:
            # gets the next non-empty part
            for i in range(pointer_pos + 1, len(scope)):
                next_pos = pointer[:-1] + [i]
                next_sub_starts = get_sub_starts(next_pos, data)
                if next_sub_starts:
                    return next_sub_starts

            return []


def get_next_scope(pointer, data):
    # there is no next scope (you're at the top scope)
    if not pointer:
        return None
    else:
        pointer_pos = pointer[-1]
        scope = get_pointer_data(pointer[:-1], data)

        if scope == '' or (pointer_pos + 1) == len(scope):
            return get_next_open_scopes(pointer[:-1], data)
        else:
            # gets the next non-empty part
            for i in range(pointer_pos + 1, len(scope)):
                next_pos = pointer[:-1] + [i]
                next_sub_starts = get_sub_starts(next_pos, data)
                if next_sub_starts:
                    return next_sub_starts

            return []


def get_start_points(data):
    temp_list = ('o', data)
    possibilities = get_next_open_scopes([0, 0], temp_list)
    # remove the 'o' from the pointer
    return [possible[1:] for possible in possibilities]


def map_to_all(func, data, pointer=None):
    if pointer is None:
        pointers = get_start_points(data)
    else:
        pointers = get_next_open_scopes(pointer, data)

    for pointer in pointers:
        pointer_data = get_pointer_data(pointer, data)
        if type(pointer_data) is str:
            print(pointer, get_pointer_data(pointer, data))
            # set_pointer_data(func(pointer), pointer, data)
        else:
            map_to_all(func, data, pointer)


print(get_next_open_scopes([0, 0], ('0', [('ji', 'wut'), 'hge'])))
map_to_all(print, [('1', ('2', '3'), ['nah']), 'hge'])