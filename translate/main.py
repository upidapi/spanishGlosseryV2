import random
import tkinter as tk
from load_words import filter
import load_words.full_data as full_data


filter.Split(';')
filter.RemoveBetween('(', ')')
filter.RemoveBetween('/', '/')
filter.RemoveX('ung.')

root = tk.Tk()
root.geometry("600x400")


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
            # todo call some func to show that you did it right
        else:
            Words.wrong[Words.selected[0]] = Words.selected[1]
            # todo call some func to show the right translation

        del Words.current[Words.selected[0]]

        Words.selected = random.choice(list(Words.current.items()))


def check_word(_):
    Words.check_correct(input_text.get())

    input_text.set("")


input_text = tk.StringVar()
input_field = tk.Entry(root, textvariable=input_text, font=('calibre', 10, 'normal'))
input_field.bind('<Return>', check_word)
#
# # creating a label for
# # name using widget Label
# name_label = tk.Label(root, text='Username', font=('calibre', 10, 'bold'))
#
# # creating a entry for input
# # name using widget Entry
# name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))
# name_entry.bind('<Return>', goto_next)
#
# # creating a label for password
# passw_label = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))
#
# # creating a entry for password
# passw_entry = tk.Entry(root, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')
# passw_entry.bind('<Return>', submit)
# # creating a button using the widget
# # Button that will call the submit function
# sub_btn = tk.Button(root, text='Submit', command=submit)
#
# # placing the label and entry in
# # the required position using grid
# # method
# name_label.grid(row=0, column=0)
# name_entry.grid(row=0, column=1)
# passw_label.grid(row=1, column=0)
# passw_entry.grid(row=1, column=1)
# sub_btn.grid(row=2, column=1)

# performing an infinite loop
# for the window to display
root.mainloop()
