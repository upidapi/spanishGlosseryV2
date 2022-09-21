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


def clear():
    Split.instances = []
    RemoveX.instances = []
    RemoveBetween.instances = []
