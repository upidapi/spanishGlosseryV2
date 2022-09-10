from general_funcs import *
from data import DataClass

line_data = DataClass()


class Text:
    text = ''
    # the pointer is where you add/remove characters when you type (is inserted at index pointer)
    pointer_pos = 0

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

                    # get text input from 0 to -1 i.e. end.
                    Text.text = before_pointer[:-1] + after_pointer
                    Text.pointer_pos -= 1

                # Unicode standard is used for string
                else:
                    character = event.unicode
                    allowed_characters = '1234567890abcdefghijklmnopqrstuvwxyzåäöñè ,.()!?'
                    # if the len is not 1 then it's a func key
                    if character in allowed_characters and len(character) == 1:
                        Text.text = before_pointer + event.unicode + after_pointer
                        Text.pointer_pos += 1

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


class Click:
    listeners = []

    def __init__(self, key, on_click, get_extra_data=None):
        self.get_extra_data = get_extra_data
        self.key = key
        self.on_click = on_click

        Click.listeners.append(self)

    # removes the instance from the instance, so it doesn't get referenced after deletion
    def __del__(self):
        Mouse.listeners.remove(self)

    def check_click(self, frame_event, selected_line):
        for event in frame_event:
            if event.type == pg.KEYDOWN and event.key == self.key and selected_line:
                if self.get_extra_data:
                    self.on_click(selected_line, self.get_extra_data)
                else:
                    self.on_click(selected_line)


class Mouse:
    listeners = []

    def __init__(self, button, on_click):
        self.button = button
        self.on_click = on_click

        Mouse.listeners.append(self)

    # removes the instance from the instance, so it doesn't get referenced after deletion
    def __del__(self):
        Mouse.listeners.remove(self)

    @staticmethod
    def check_over_word():
        pos = pg.mouse.get_pos()
        for index, line in enumerate(line_data):  # might cause problems
            x1, y1, x2, y2 = wh_to_chords((line['x'], line['y'], line['width'], line['height']))

            if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
                return index

    def check_click_word(self, frame_events):
        for event in frame_events:
            # checks if you pressed x mouse button
            if event.type == pg.MOUSEBUTTONDOWN and event.button == self.button:
                pos = pg.mouse.get_pos()
                for index, line in enumerate(line_data):  # might cause problems
                    x1, y1, x2, y2 = wh_to_chords((line['x'], line['y'], line['width'], line['height']))

                    if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
                        if self.on_click.__defaults__ is None:
                            self.on_click()
                        else:
                            self.on_click(index)

    @classmethod
    def listen(cls, frame_events):
        for obj in cls.listeners:
            obj.check_click(frame_events)


def listen(frame_events):
    Text.save_text_input(frame_events)
    Mouse.listen(frame_events)
