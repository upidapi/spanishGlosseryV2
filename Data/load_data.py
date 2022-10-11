import json
from Data import SelectFilesMyOwn


def load_data(files: list):
    full_data = []
    for file in files:
        with open(file) as jsonFile:
            full_data += json.load(jsonFile)
            jsonFile.close()

    return full_data


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


def load_clean_data():
    files = SelectFilesMyOwn.ask_for_files(r"..\Data\books")

    all_data = load_data(files)

    for i, pair in enumerate(all_data):
        for j, word in enumerate(pair):
            # todo add the clean args to load_clean_data
            all_data[i][j] = clean(word,
                                   split_keys=(';',),
                                   remove_keys=('ung.',),
                                   remove_between_keys=(('(', ')'), ('/', '/')))

    return find_alternative_translations(all_data)


def load_raw_data():
    def _get_data(file):
        # gets the New
        with open(file) as jsonFile:
            json_object = json.load(jsonFile)
            jsonFile.close()

        return json_object

    data_1 = _get_data(r'../Data/other_data/lan1_data.json')
    data_2 = _get_data(r'../Data/other_data/lan2_data.json')

    return data_1, data_2
