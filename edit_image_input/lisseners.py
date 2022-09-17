from general_funcs import *
from data.funcs import Handler
import time

line_data = Handler()


class EditText:
    last_edit_time = time.time()
    pointer_pos = 0
    text = ''

    @staticmethod
    def change_text(frame_events):
        for event in frame_events:
            if event.type == pg.KEYDOWN:
                EditText.last_edit_time = time.time()

                if event.key == pg.K_RIGHT:
                    if EditText.pointer_pos < len(EditText.text):
                        EditText.pointer_pos -= 1

                elif event.key == pg.K_LEFT:
                    if 0 < EditText.pointer_pos:
                        EditText.pointer_pos -= 1

                else:
                    pos = EditText.pointer_pos
                    last_element = len(EditText.text)
                    # text before the pointer
                    bef_pointer = EditText.text[0:pos]
                    # text after the pointer
                    aft_pointer = EditText.text[pos:last_element]

                    if event.key == pg.K_BACKSPACE:
                        if 0 < EditText.pointer_pos:
                            EditText.pointer_pos -= 1
                            EditText.text = bef_pointer[0:-1] + aft_pointer

                    else:
                        allowed_chars = '1234567890!?,./\\'
                        char = event.unicode
                        if char.isalpha() or (len(char) and char in allowed_chars):
                            EditText.text = bef_pointer + char + aft_pointer

                        EditText.pointer_pos += 1

    @staticmethod
    def get_text():
        return EditText.text

    @staticmethod
    def set_text(text):
        EditText.text = text
        EditText.pointer_pos = len(text)

    @staticmethod
    def get_pointer():
        return EditText.pointer_pos

    @staticmethod
    def get_pointer_pos():
        return EditText.pointer_pos

    @staticmethod
    def time_since_last_edit():
        return time.time() - EditText.last_edit_time


def check_over_word():
    pos = pg.mouse.get_pos()
    for index, line in enumerate(line_data):  # might cause problems
        x1, y1, x2, y2 = wh_to_chords((line['x'], line['y'], line['width'], line['height']))

        if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
            return index
