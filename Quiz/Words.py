import random
from abc import ABC, abstractmethod
from Data import load_clean_data


class Words(ABC):
    # todo this should NOT be run imported
    # todo this is the thing that causes errors etc

    @classmethod
    def get_data(cls):
        cls.all = load_clean_data()

    all = {}
    selected = {}  # all selected words
    current = {}  # all words left
    right = {}
    wrong = {}

    current_word = ()

    @staticmethod
    @abstractmethod
    def right_answer():
        # example implementation
        # wrong_text_var.set('Correct!')
        # wrong_text_fade.change(start=(0, 255, 0), end=(240, 240, 240), time=1)
        pass

    @staticmethod
    @abstractmethod
    def wrong_answer(text):
        # example implementation
        # wrong_text_var.set(' / '.join(text))
        # wrong_text_fade.change(start=(255, 0, 0), end=(240, 240, 240), time=3)
        pass

    @staticmethod
    @abstractmethod
    def set_translate_text(text):
        # example implementation
        # translate_text.set(text)
        pass

    @staticmethod
    def nothing_left():
        """
        called when you have done all the words
        """
        pass

    # the cls is used so that the abstract methods gets called
    @classmethod
    def next_word(cls, first=False):
        if not first:
            del cls.current[cls.selected[0]]

        options = list(cls.current.items())

        if len(options) == 0:
            cls.nothing_left()
        else:
            cls.selected = random.choice(options)
            cls.set_translate_text(cls.selected[0])

    @classmethod
    # todo add some select screen to select what type of words to use
    def get_new_words(cls, select):
        if select == 'wrong':
            cls.current = cls.wrong.copy()
        if select == 'right':
            cls.current = cls.right.copy()
        if select == 'same':
            cls.current = cls.selected.copy()
        if select == 'lan1':
            cls.current = cls.all[0].copy()
            cls.selected = cls.all[0].copy()
        if select == 'lan2':
            cls.current = cls.all[1].copy()
            cls.selected = cls.all[1].copy()

        cls.right = {}
        cls.wrong = {}

        cls.next_word(True)

    @classmethod
    def check_correct(cls, word):
        if word in cls.selected[1]:
            # right
            cls.right[cls.selected[0]] = cls.selected[1]
            cls.right_answer()
        else:
            # wrong
            cls.wrong[cls.selected[0]] = cls.selected[1]
            cls.wrong_answer(cls.selected[1])

        cls.next_word()
