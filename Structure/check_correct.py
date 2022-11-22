from Helpers import get_pointer_data, get_next_open_scopes


def get_all_possibilities(pointers, data):
    all_possibilities = []
    for pointer in pointers:
        all_possibilities += get_next_open_scopes(pointer, data)

    return all_possibilities


def get_possible(char, pointers, data):
    all_possibilities = get_all_possibilities(pointers, data)
    possibilities = []

    for possibility in all_possibilities:
        possibility_char = get_pointer_data(possibility, data)
        if char == possibility_char:
            possibilities.append(possibility)

    return possibilities


def check_correct(inp, translation_struct):
    # the check correct always finds next possibility's, so we have to start before the first answer
    translation_struct = tuple(['o'] + list(translation_struct))

    pointers = [[0, 0]]
    for char in inp:
        pointers += get_possible(char, pointers, translation_struct)

        # if there is no possibility it's right
        if not pointers:
            return False

    return True


data = (['är ', ''], '', 'blå')

print(check_correct('blå', data))

print(get_next_open_scopes([0, 0], ('a', ['', '', ['2', '123'], '23'], 'asd')))
