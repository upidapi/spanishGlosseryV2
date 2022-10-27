def get_pointer_data(pointer, data):
    scope = data
    for part in pointer:
        if scope == '':
            return ''
        else:
            scope = scope[part]
    return scope


def get_next_open_scope(pointer, data):
    # if the pointer is [] implies that its at the top
    if not pointer:
        return None
    else:
        scope = get_pointer_data(pointer[:-1], data)
        scope_pos = pointer[-1]

        # if we can't go to next
        # if pointer is at the end of it's scope
        if len(scope) - 1 == scope_pos or \
                type(scope) is list:

            # goes a step upp
            return get_next_open_scope(pointer[:-1], data)
        else:
            # the next open scope
            for i in range((scope_pos + 1), len(scope)):
                new_pointer = pointer[:-1] + [scope_pos + 1]
                if get_pointer_data(new_pointer, data):
                    return new_pointer

            # if you can't find next one
            return None


def get_sub_starts(pointer, data):
    if pointer is None:
        return []
    else:
        scope = get_pointer_data(pointer, data)

        if type(scope) is str:
            # if its only one character
            if len(scope) == 1:
                return [pointer]

            return [pointer + [0]]

        elif type(scope) in (list, tuple):
            all_starts = []

            for i in range(len(scope)):
                all_starts += get_sub_starts(pointer + [i], data)

            return all_starts

        else:
            raise 'invalid data'


def get_all_possibilities(pointers, data):
    all_possibilities = []

    for pointer in pointers:
        next_open_scope = get_next_open_scope(pointer, data)
        all_possibilities += get_sub_starts(next_open_scope, data)

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
        # checks if one of the possibilities is ''
        possibilities = get_possible('', pointers, answers)
        pointers = []

        if possibilities:
            pointers += possibilities

        pointers += get_possible(char, pointers, answers)

        # if there is no possibility it's right
        if not pointers:
            return False

    return True


"""
() => chain statement
    # used manly to chain 'or statements' and 'text statements'
    
    (a, b, c) 
    if you're at 'a' you have to go to next 'b'
    you always have to go to the next index

[] => or statement
    (x, [a, b, c], y)
    if you're at 'x' you have to go to 'a', 'b' or 'c'
    if you're at 'a', 'b' or 'c' you have to go to y
    
    when entering you can go to any index (in the list) when entering
    when exiting you have to go to after the list 
"""

data = (['är ', ''], '', 'blå')

print(check_correct('blå', data))


# def get_pointer_data(pointer, data):
#     scope = data
#     for part in pointer:
#         if scope == '':
#             return ''
#         else:
#             scope = scope[part]
#     return scope
#
#
# def get_next_open_scope(pointer, data):
#     # if the pointer is [] implies that its at the top
#     if not pointer:
#         return None
#     else:
#         scope = get_pointer_data(pointer[:-1], data)
#         scope_pos = pointer[-1]
#
#         # if we can't go to next
#         # if pointer is at the end of it's scope
#         if len(scope) - 1 == scope_pos or type(scope) is list:
#             # goes a step upp
#             return get_next_open_scope(pointer[:-1], data)
#         else:
#             # the next open scope
#             return pointer[:-1] + [scope_pos + 1]
#
#
# def get_sub_starts(pointer, data):
#     if pointer is None:
#         return []
#     else:
#         scope = get_pointer_data(pointer, data)
#
#         if type(scope) is str:
#             # if its only one character
#             if len(scope) == 1:
#                 return [pointer]
#
#             return [pointer + [0]]
#
#         elif type(scope) in (list, tuple):
#             all_starts = []
#
#             for i in range(len(scope)):
#                 all_starts += get_sub_starts(pointer + [i], data)
#
#             return all_starts
#
#         else:
#             raise 'invalid data'
#
#
# def get_all_possibilities(pointers, data):
#     all_possibilities = []
#
#     for pointer in pointers:
#         next_open_scope = get_next_open_scope(pointer, data)
#         all_possibilities += get_sub_starts(next_open_scope, data)
#
#     return all_possibilities
#
#
# def get_possible(char, pointers, data):
#     all_possibilities = get_all_possibilities(pointers, data)
#     possibilities = []
#
#     for possibility in all_possibilities:
#         possibility_char = get_pointer_data(possibility, data)
#         if char in possibility_char:
#             possibilities.append(possibility)
#
#     return possibilities
#
#
# def check_correct(inp, answers):
#     # the check correct always finds next possibility's, so we have to start before the first answer
#     answers = tuple(['o'] + list(answers))
#
#     pointers = [[0, 0]]
#     for char in inp:
#         # checks if one of the possibilities is ''
#         possibilities = get_possible('', pointers, data)
#         if possibilities:
#             pointers = possibilities
#
#         pointers = get_possible(char, pointers, data)
#
#         # if there is no possibility it's right
#         if not pointers:
#             return False
#
#     return True
#
#
# """
# () => chain statement
#     # used manly to chain 'or statements' and 'text statements'
#
#     (a, b, c)
#     if you're at 'a' you have to go to next 'b'
#     you always have to go to the next index
#
# [] => or statement
#     (x, [a, b, c], y)
#     if you're at 'x' you have to go to 'a', 'b' or 'c'
#     if you're at 'a', 'b' or 'c' you have to go to y
#
#     when entering you can go to any index (in the list) when entering
#     when exiting you have to go to after the list
# """
#
# data = (['är ', ''], '', 'blå')
#
# print(check_correct('blå', data))



