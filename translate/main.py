import random
import tkinter as tk
from load_words import filter, full_data

filter.Split(';')
filter.RemoveBetween('(', ')')
filter.RemoveBetween('/', '/')
filter.RemoveX('ung.')


class FadeText:
    def __init__(self, text_obj, time, end_color, start_color=None):
        """
        temp

        :param text_obj: this is the tk.Label that will fade to end_color
        :param time: the time it takes to fade
        :param end_color: the color it fades to
        :param start_color: the color it starts on
        """

        self.text_obj = text_obj
        self.time = time
        self.end_color = end_color
        if start_color is None:
            self.start_color = text_obj.cget("bg")
        else:
            self.start_color = start_color

    amount = 0

    @staticmethod
    def wrong(time_step, new=False):
        if 1 <= Display.amount:
            Display.amount += 1

        else:
            color = int(time_step ** 8)

            if 255 < color:
                color = 255
            else:
                root.after(50, Display.wrong(time_step + 0.05))

            color_hex = '#%02x%02x%02x' % (255, color, color)
            wrong_text.configure(foreground=color_hex)

        if new:
            Display.amount += 1


class Display:
    amount = 0

    @staticmethod
    def wrong(time_step, new=False):
        if 1 <= Display.amount:
            Display.amount += 1

        else:
            color = int(time_step ** 8)

            if 255 < color:
                color = 255
            else:
                root.after(50, Display.wrong(time_step + 0.05))

            color_hex = '#%02x%02x%02x' % (255, color, color)
            wrong_text.configure(foreground=color_hex)

        if new:
            Display.amount += 1

    @staticmethod
    def temp():
        pass


class Words:
    all = full_data.get('multiple')
    selected = {}  # all selected words
    current = {}  # all words left
    right = {}
    wrong = {}

    current_word = ()

    @staticmethod
    def nothing_left():
        """
        called when you have done all the words
        """
        pass

    @staticmethod
    def next_word(first=False):
        if not first:
            del Words.current[Words.selected[0]]

        options = list(Words.current.items())

        if len(options) == 0:
            Words.nothing_left()
        else:
            Words.selected = random.choice(options)

    @staticmethod
    def get_new_words(select):
        if select == 'wrong':
            Words.current = Words.wrong.copy()
        if select == 'right':
            Words.current = Words.right.copy()
        if select == 'same':
            Words.current = Words.selected.copy()
        if select == 'lan1':
            Words.current = Words.all[0].copy()
            Words.selected = Words.all[0].copy()
        if select == 'lan2':
            Words.current = Words.all[1].copy()
            Words.selected = Words.all[1].copy()

        Words.right = {}
        Words.wrong = {}

        Words.next_word(True)

    @staticmethod
    def check_correct(word):
        if word in Words.selected[1]:
            Words.right[Words.selected[0]] = Words.selected[1]
            # todo call some func to show the right translation
        else:
            Words.wrong[Words.selected[0]] = Words.selected[1]
            Display.wrong(0, new=True)

        del Words.current[Words.selected[0]]

        Words.selected = random.choice(list(Words.current.items()))


def check_word(_):
    Words.check_correct(input_text.get())
    input_text.set("")


Words.get_new_words('lan1')

root = tk.Tk()
root.geometry("600x400")

input_text = tk.StringVar(root)

input_field = tk.Entry(root, textvariable=input_text, font=('calibre', 10, 'normal'))

input_field.pack()
input_field.bind('<Return>', check_word)

wrong_text = tk.Label(root, text='test', foreground="#ff0000", font=("Times New Roman", 12, "bold"), bg='#ffffff')
root.configure(bg='#ffffff')
wrong_text.pack()

# test = tk.Button(root, text="test button", command=change)
# test.pack()

root.mainloop()
