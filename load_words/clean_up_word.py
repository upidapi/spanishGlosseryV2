class RemoveBetween:
    """
    removes everything between a and b including a and b
    """
    instances = []

    def __init__(self, a: str, b: str):
        self.a = a
        self.b = b
        RemoveBetween.instances.append(self)

    def logic(self, word: str):
        new_word = ""
        remove = False
        for letter in word:
            if letter == self.a:
                remove = True
            elif letter == self.b:
                remove = False
            elif not remove:
                new_word += letter
        return new_word


class RemoveX:
    """
    removes instances of x
    """
    instances = []

    def __init__(self, remove: str):
        self.remove = remove
        RemoveX.instances.append(self)

    def logic(self, word: str):
        return word.replace(self.remove, '')


class Split:
    """
    splits the word at x
    x=; 'abc;def' -> 'abc', 'def'
    """
    instances = []

    def __init__(self, split: str):
        self.split = split
        Split.instances.append(self)

    def logic(self, word: str):
        return word.split(self.split)


def clean(word):
    word = [word]
    split_word = []
    for instance in Split.instances:
        for part in word:
            split_word += instance.logic(part)
        word += split_word
    word = split_word

    for instance in RemoveX.instances:
        for i, part in enumerate(word):
            word[i] = instance.logic(part)

    for instance in RemoveBetween.instances:
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
