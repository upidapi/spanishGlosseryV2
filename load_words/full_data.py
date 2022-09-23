from load_words import filter
from load_words.file_data import load_data, get_files


def clean(word):
    word = [word]
    split_word = []
    for instance in filter.Split.instances:
        for part in word:
            split_word += instance.logic(part)
        word += split_word
    word = split_word

    for instance in filter.RemoveX.instances:
        for i, part in enumerate(word):
            word[i] = instance.logic(part)

    for instance in filter.RemoveBetween.instances:
        for i, part in enumerate(word):
            word[i] = instance.logic(part)

    for i, part in enumerate(word):
        word[i] = part.strip()

    return word


def find_alternative_translations(data: list):
    w1_to_w2 = {}
    w2_to_w1 = {}

    for translation in data:
        for word in translation[0]:
            if word not in w1_to_w2:
                w1_to_w2[word] = translation[1]
            else:
                w1_to_w2[word] += translation[1]

        for word in translation[1]:
            if word not in w2_to_w1:
                w2_to_w1[word] = translation[0]
            else:
                w2_to_w1[word] += translation[0]

    return w1_to_w2, w2_to_w1


def get(select):
    # example parameters
    # filter.Split(';')
    # filter.RemoveBetween('(', ')')
    # filter.RemoveBetween('/', '/')
    # filter.RemoveX('ung.')

    all_data = load_data(get_files(select))
    for i, pair in enumerate(all_data):
        for j, word in enumerate(pair):
            all_data[i][j] = clean(word)

    return find_alternative_translations(all_data)
