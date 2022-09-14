from general_funcs import *
from data import DataClass
import time

line_data = DataClass()


class Text:
    text = ''
    # the pointer is where you add/remove characters when you type (is inserted at index pointer)
    pointer_pos = 0
    time_since_last_edit = time.time()

    # noinspection SpellCheckingInspection
    @staticmethod
    def save_text_input(frame_event):
        for event in frame_event:
            if event.type == pg.KEYDOWN:
                after_pointer = Text.text[Text.pointer_pos: len(Text.text)]
                before_pointer = Text.text[0:Text.pointer_pos]

                # change pointer pos
                if event.key == pg.K_RIGHT:
                    Text.pointer_pos = min(Text.pointer_pos + 1, len(Text.text))

                if event.key == pg.K_LEFT:
                    Text.pointer_pos = max(Text.pointer_pos - 1, 0)

                # Check for backspace
                if event.key == pg.K_BACKSPACE:
                    Text.time_since_last_edit = time.time()

                    # get text input from 0 to -1 i.e. end.
                    Text.text = before_pointer[:-1] + after_pointer
                    Text.pointer_pos -= 1

                # Unicode standard is used for string
                else:
                    character = event.unicode
                    # noinspection SpellCheckingInspection
                    allowed_characters = '1234567890abcdefghijklmnopqrstuvwxyzåäöñè ,.()!?'
                    # if the len is not 1 then it's a func key
                    if character in allowed_characters and len(character) == 1:
                        Text.time_since_last_edit = time.time()

                        Text.text = before_pointer + event.unicode + after_pointer
                        Text.pointer_pos += 1

    @staticmethod
    def since_last_edit():
        return time.time() - Text.time_since_last_edit

    @staticmethod
    def get_text():
        return Text.text

    @staticmethod
    def get_pointer_pos():
        return Text.pointer_pos

    @staticmethod
    def set_text(text=''):
        Text.pointer_pos = len(text)
        Text.text = text


class Mouse:
    @staticmethod
    def check_over_word():
        pos = pg.mouse.get_pos()
        for index, line in enumerate(line_data):  # might cause problems
            x1, y1, x2, y2 = wh_to_chords((line['x'], line['y'], line['width'], line['height']))

            if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
                return index
