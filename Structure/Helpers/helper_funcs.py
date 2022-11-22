from Structure.Helpers.custom_pointer_list \
    import OrStatement


def get_parent_type(data, pointer):
    parent_type = type(data[pointer])
    if parent_type is str:
        return get_parent_type(data, pointer[:-1])
    return parent_type


def get_sub_possible(pointer: list[int], data, do_next=True):
    """
    :param pointer: place to get sub_possible
    :param data:
    :param do_next: whether to get_next_open() if it encounters an empty str ""
    :return:
    """

    scope = data[pointer]

    if type(scope) is OrStatement:
        possible = []
        for i in range(len(scope)):
            possible += get_sub_possible(pointer + [i], data, do_next=False)
        return possible
    elif len(scope) == 1 and type(scope) is str:
        return [pointer]
    elif not scope:
        # if it's empty get next thing instead
        if do_next:
            return get_all_next_possible(pointer, data)
        return []
    else:
        # continue down
        return get_sub_possible(pointer + [0], data)


def get_all_next_possible(pointer, data):
    if not pointer:
        return []
    scope = data[pointer[:-1]]
    # go upp if at last place in scope or OrEscape
    if pointer[-1] == len(scope) - 1 \
            or type(data[pointer]) is OrStatement:
        return get_all_next_possible(pointer[:-1], data)

    next_thing = pointer[:-1] + [pointer[-1] + 1]
    return get_sub_possible(next_thing, data)


def get_start_points(data):
    return get_sub_possible([], data)


def map_to_all(func, data, start=None):
    """
    maps func to all objects in data
    :param func: function to be mapped, if the func returns none the item is deleted
    :param data:
    :param start: where to start, defaults to "get_start_points(data)"
    """
    if start is None:
        pointers = get_start_points(data)
    else:
        pointers = get_all_next_possible(start, data)

    for pointer in pointers:
        pointer_data = data[pointer]
        if type(pointer_data) is not str:
            map_to_all(func, data, pointer)
        else:
            # skip the string pos
            new_value = func(pointer[:-1])
            if new_value is not None:
                data[pointer[:-1]] = new_value
            else:
                del data[pointer[:-1]]
                map_to_all(func, data, start)
                break

