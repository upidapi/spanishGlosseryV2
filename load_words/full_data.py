from load_words.file_data import load_data, get_files


def clean(word, split_keys: tuple, remove_keys: tuple, remove_between_keys: tuple):
    """
    cleans up and splits the word

    :param word: the word to be cleaned
    :param split_keys: splits the words at all split_keys
    :param remove_keys: removes all instances of the remove_keys
    :param remove_between_keys:
    :return: the clean word(s) in a list
    """
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


def find_alternative_translations(data: list):
    w1_to_w2 = {}
    w2_to_w1 = {}

    for translation in data:
        for word in translation[0]:
            if word in w1_to_w2:
                w1_to_w2[word] += translation[1]
            else:
                # the join(list) is to prevent multiple possible translations become multiple 'words'
                w1_to_w2[' / '.join(translation[0])] = translation[1]

        for word in translation[1]:
            if word in w2_to_w1:
                w2_to_w1[word] += translation[0]
            else:
                w2_to_w1[' / '.join(translation[1])] = translation[0]

    return w1_to_w2, w2_to_w1


def get(select):
    all_data = load_data(get_files(select))
    for i, pair in enumerate(all_data):
        for j, word in enumerate(pair):
            all_data[i][j] = clean(word,
                                   split_keys=(';',),
                                   remove_keys=('ung.',),
                                   remove_between_keys=(('(', ')'), ('/', '/')))

    return find_alternative_translations(all_data)
