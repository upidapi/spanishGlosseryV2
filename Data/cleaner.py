import re


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
    import re
    word = [{'text': '///el/ test1/tes2 /ue/', 'type': None}]
    for i, part in enumerate(word):

        text = part['text']
        matches = re.finditer('//|/.{,2}/', text)

        split_words = []
        last_end = 0
        for match in matches:
            next_start = match.span(0)

            non_match_text = text[last_end:next_start]
            split_words += get_add_part(non_match_text, None)

            match_text = match.match[1:-1]
            split_words += get_add_part(match_text, 'optional')

            last_end = match.span(1)

        word = word[:i] + split_words + word[i:]


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
        part_data = {
            'text': text,
            'type': option
        }
    return part_data


def main():
    # adds to optional if the amount of characters between start key and end key is less than remove_ken
    import re
    word = [{'text': '///el/ test1/tes2 /ue/', 'type': None}]
    for i, part in enumerate(word):

        text = part['text']
        matches = re.finditer('//|/.{,2}/', text)

        split_words = []
        last_end = 0
        for match in matches:
            next_start = match.span()[0]

            non_match_text = text[last_end:next_start]
            split_words += get_add_part(non_match_text, None)

            match_text = match.match[1:-1]
            split_words += get_add_part(match_text, 'optional')

            last_end = match.span()[0]

        word = word[:i] + split_words + word[i:]

if __name__ == '__main__':
    main()
