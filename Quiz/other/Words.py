import random
from typing import Literal

from Data import get_translate_data
from Quiz.other import end_screen


class WordData:
    def __init__(self, languishes):
        self.languishes = languishes

        self.right_answer = None
        self.wrong_answer = None
        self.set_translate_text = None

        self.all = get_translate_data()
        self.selected = []  # all selected words
        self.current = []  # all words left
        self.right = []
        self.wrong = []

        self.retry = False  # is true when you retry to type a word
        self.current_word = {'word': None, 'translation': None}

    def setup(self, right_answer, wrong_answer, set_translate_text):
        self.right_answer = right_answer
        self.wrong_answer = wrong_answer
        self.set_translate_text = set_translate_text

    def nothing_left(self):
        end_screen(self, self.languishes)

    # the cls is used so that the abstract methods gets called
    def next_word(self, first=False):
        if not first:
            self.current.remove(self.current_word)

        if len(self.current) == 0:
            self.nothing_left()
        else:
            self.current_word = random.choice(self.current)
            self.set_translate_text(self.current_word['word'])

    def get_new_words(self, select: Literal['wrong', 'right', 'same', 'lan1', 'lan2']):
        # this is never None
        new_data = None

        if select == 'wrong':
            new_data = self.wrong
        elif select == 'right':
            new_data = self.right
        elif select == 'same':
            new_data = self.selected
        elif select == 'lan1':
            new_data = self.all[0]
        elif select == 'lan2':
            new_data = self.all[1]

        # makes it possible to load the same data as last time
        self.selected = new_data.copy()
        self.current = new_data.copy()
        self.right = []
        self.wrong = []

    def check_correct(self, word):
        if word in self.current_word['translation']:
            # right
            if not self.retry:
                self.right.append(self.current_word)
            self.retry = False

            self.right_answer()

            self.next_word()  # force user to type it right before continuing

        else:
            # wrong
            self.wrong_answer(self.current_word['translation'])

            if not self.retry:
                self.wrong.append(self.current_word)
            self.retry = True
        # self.next_word()
