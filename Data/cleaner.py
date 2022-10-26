def split_str_list(word_list: list[str], key: str):
    # if type(word_list) is str:
    #     word_list = [word_list]

    split_word = []
    for word in word_list:
        split_word += word.split(key)

    return split_word


def clean(word, split_keys: tuple, remove_keys: tuple, remove_between_keys: tuple):
    """
    cleans up and splits the word

    :param word: the word to be cleaned
    :param split_keys: splits the words at all split_keys
    :param remove_keys: removes all instances of the remove_keys
    :param remove_between_keys:
    :return: the clean word(s) in a list
    """

    # adds to optional if the amount of characters between start key and end key is less than remove_ken
    word_list = [word]
    for key in split_keys:
        word_list = split_str_list(word_list, key)

    # removes all instances of the remove_keys
    for key in remove_keys:
        word = word.replace(key, '')

    # removes anything between key[0] and key[1]
    for key in remove_between_keys:
        new_word = ""
        remove = False
        for letter in word:
            if letter == key[0]:
                remove = True
            elif letter == key[1]:
                remove = False
            elif not remove:
                new_word += letter
        word = new_word
    # splits the words at all split_keys
    word = [word]
    split_word = []
    for key in split_keys:
        for part in word:
            split_word += part.split(key)
        word += split_word
    word = word[1:]

    # removes the trailing and leading spaces
    for i, part in enumerate(word):
        word[i] = part.strip()

    return word


def get_add_part(text, option):
    part_data = []
    if text:
        part_data = [{
            'text': text,
            'type': option
        }]
    return part_data


def find_optionals(word: list[dict] | list,
                   regex_match_expression: str,
                   match_remove_slice: slice = slice(None, None)):
    import re

    """
    :param word: a list of parts of a word
    :param regex_match_expression: a regex str to try to match to
    :return: finds and sections the text into optional or necessary parts
    """

    # adds to optional if the amount of characters between start key and end key is less than remove_ken
    for i, part in enumerate(word):

        text = part['text']
        matches = re.finditer(regex_match_expression, text)

        split_words = []
        next_start = 0
        for match in matches:
            start = match.span()[0]

            # text part before match
            split_words += get_add_part(
                text=text[next_start:start],
                option=part['type']  # defaults to "parent's" type
            )

            # match text part
            split_words += get_add_part(
                text=match.group(0)[match_remove_slice],
                option='optional'
            )

            next_start = match.span()[1]

        # text part after last match
        split_words += get_add_part(
            text=text[next_start:len(text)],
            option=part['type']  # defaults to "parent's" type
        )

        # the i+1 is so that the current part doesn't get added
        word = word[:i] + split_words + word[(i + 1):]

    return word


def get_scope(pointer, parts):
    pointer_parent = pointer[:-1]
    current_parent = parts
    for thing in pointer_parent:
        current_parent = current_parent[thing]

    return current_parent


def get_after_self(self, parts):
    self_parent = self[:-1]
    self_parent_data = get_scope(self, parts)
    points_after_self = list(range(self[-1] + 1, len(self_parent_data)))
    return [self_parent + [x] for x in points_after_self]


def get_possibilities(pointer, parts):
    super_parent_pos = pointer[:-3]
    super_parent_pointer = pointer[-3]
    parent_pos = pointer[:-2]
    parent_pointer = pointer[-2]
    self_pos = pointer[:-1]
    self_pointer = pointer[-1]

    # ...[0] will case problems in edge cases
    possibilities = [get_after_self(pointer, parts)[0]]

    # if pointer is not last position in its scope
    if self_pointer != len(get_scope(pointer, parts)):
        if parent_pointer == 'bef':
            scope = get_scope(self_pos, parts)
            if scope['mid'] is not None:
                possibilities += [parent_pos + ['mid', 0]]
            if scope['aft'] is not None:
                possibilities += [parent_pos + ['aft', 0]]

        elif parent_pointer == 'mid':
            possibilities += get_after_self(parent_pos + ['aft', 0], parts)

        elif parent_pointer == 'aft':
            possibilities += get_after_self(parent_pos + ['aft', 0], parts)

    # if pointer is at last position in its scope
    # or if there is no other possibilities
    if self_pointer == len(get_scope(pointer, parts)) - 1 or \
            len(possibilities) == 0:
        # might cause problems
        next_part = get_scope(super_parent_pos, parts)[super_parent_pointer + 1]
        if next_part is None:
            return []
        possibilities += next_part

    return possibilities


def convert_to_text(possibilities, parts):
    return [get_scope(possibility, parts)[possibility[-1]] for possibility in possibilities]


pae = [
    {
        'bef': ['hi', 'im', 'blue'],
        'mid': ['red'],
        'aft': ['green',  'man']
    },
    None
]

print(convert_to_text(get_possibilities([0, 'bef', 0], pae), pae))

# def temp_name():
#
#     pointer = []
#     parts = [{'bef': [], 'mid': [], 'aft': []}]
#     inp = 'hej', 'en', 'hur', 'anka'
#
#     for word in inp:
#         # get next pointer pos
#         pointer = [0, 'bef', 0]
#
#         super_parent_pos = pointer[:-3]
#         super_parent_pointer = pointer[-3]
#         parent_pos = pointer[:-2]
#         parent_pointer = pointer[-2]
#         self_pointer = pointer[-1]
#
#         possibilities = get_after_self(self_pointer, parts)
#
#         # if pointer is not last position in its scope
#         if self_pointer != len(get_scope(pointer, parts)):
#             if parent_pointer == 'bef':
#                 possibilities += parent_pos + ['mid', 0]
#                 possibilities += parent_pos + ['aft', 0]
#
#             elif parent_pointer == 'mid':
#                 possibilities += get_after_self(parent_pos + ['aft', 0], parts)
#
#             elif parent_pointer == 'eft':
#                 possibilities += get_after_self(parent_pos + ['aft', 0], parts)
#
#         # if pointer is at last position in its scope
#         # or if there is no other possibilities
#         if self_pointer == len(get_scope(pointer, parts)) or \
#            len(possibilities) == 0:
#             # might cause problems
#             next_part = get_scope(super_parent_pos, parts)[super_parent_pointer + 1]
#             if next_part is None:
#                 return None
#             possibilities += next_part


def main():
    pass
    # word = [{'text': 'el nahe /de/', 'type': None}]
    #
    # word = find_optionals(word, '/.{,2}/', slice(1, -1))
    # print(word)
    #
    # word = find_optionals(word, 'el')
    # print(word)


if __name__ == '__main__':
    main()
