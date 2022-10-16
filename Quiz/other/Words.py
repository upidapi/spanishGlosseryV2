import random
from typing import Literal

from Data import load_clean_data
from Quiz.other import end_screen


class WordData:
    # todo this should NOT be run imported
    # todo this is the thing that causes errors etc
    # i see no error here but ill leave it here for now
    
    def __init__(self, languishes):
        self.languishes = languishes

        self.right_answer = None
        self.wrong_answer = None
        self.set_translate_text = None

        self.all = load_clean_data()
        self.selected = {}  # all selected words
        self.current = {}  # all words left
        self.right = {}
        self.wrong = {}

        self.current_word = ()

    def setup(self, right_answer, wrong_answer, set_translate_text):
        self.right_answer = right_answer
        self.wrong_answer = wrong_answer
        self.set_translate_text = set_translate_text

    def nothing_left(self):
        end_screen(self, self.languishes)

    # the cls is used so that the abstract methods gets called
    def next_word(self, first=False):
        if not first:
            del self.current[self.selected[0]]

        options = list(self.current.items())

        if len(options) == 0:
            self.nothing_left()
        else:
            self.selected = random.choice(options)
            self.set_translate_text(self.selected[0])

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
        self.right = {}
        self.wrong = {}

    def check_correct(self, word):
        if word in self.selected[1]:
            # right
            self.right[self.selected[0]] = self.selected[1]
            self.right_answer()
        else:
            # wrong
            self.wrong[self.selected[0]] = self.selected[1]
            self.wrong_answer(self.selected[1])

        self.next_word()
