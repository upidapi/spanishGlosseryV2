import tkfilebrowser
import os
import json


class RawData:
    @staticmethod
    def get_sub_files(directory):
        if os.path.isfile(directory):
            return [directory.replace(os.getcwd() + '\\', '').replace('\\', '/')]
        else:
            files = []
            for sub_dir in os.listdir(directory):
                files += RawData.get_sub_files(os.path.join(directory, sub_dir))

            return files

    @staticmethod
    def get_dir_files(directory):
        if isinstance(directory, tuple):
            files = []
            for sub_dir in directory:
                files += RawData.get_sub_files(sub_dir)

            return files

        elif directory is not None:
            return [directory.split('\\')[-1]]

        else:
            return []

    @staticmethod
    def get_files(select='multiple'):
        selected_directories = None

        if select == 'multiple':
            selected_directories = tkfilebrowser.askopendirnames(initialdir=r"../load_words/words/", title='select')
        elif select == 'singular':
            selected_directories = tkfilebrowser.askopenfilename(initialdir=r"../load_words/words/", title='select')

        return RawData.get_dir_files(selected_directories)

    @staticmethod
    def load_data(files: list):
        full_data = []
        for file in files:
            with open(file) as jsonFile:
                full_data += json.load(jsonFile)
                jsonFile.close()

        return full_data

    @staticmethod
    def get(select):
        return RawData.load_data(RawData.get_files(select))


class Word:
    class RemoveBetween:
        """
        removes everything between a and b including a and b
        """
        instances = []

        def __init__(self, a: str, b: str):
            self.a = a
            self.b = b
            Word.RemoveBetween.instances.append(self)

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
            Word.RemoveX.instances.append(self)

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
            Word.Split.instances.append(self)

        def logic(self, word: str):
            return word.split(self.split)

    @staticmethod
    def clean(word):
        word = [word]
        split_word = []
        for instance in Word.Split.instances:
            for part in word:
                split_word += instance.logic(part)
            word += split_word
        word = split_word

        for instance in Word.RemoveX.instances:
            for i, part in enumerate(word):
                word[i] = instance.logic(part)

        for instance in Word.RemoveBetween.instances:
            for i, part in enumerate(word):
                word[i] = instance.logic(part)

        for i, part in enumerate(word):
            word[i] = part.strip()

        return word

    @staticmethod
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


def get_data(select):
    # example parameters
    Word.Split(';')
    Word.RemoveBetween('(', ')')
    Word.RemoveBetween('/', '/')
    Word.RemoveX('ung.')

    all_data = RawData.get(select)
    for i, pair in enumerate(all_data):
        for j, word in enumerate(pair):
            all_data[i][j] = Word.clean(word)

    return Word.find_alternative_translations(all_data)


print(get_data('multiple'), 'ds')
