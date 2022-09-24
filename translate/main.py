from translate.FadeText import Fade
import tkinter as tk
from translate.Words import Words


# class Words:
#     all = full_data.get('multiple')
#     selected = {}  # all selected words
#     current = {}  # all words left
#     right = {}
#     wrong = {}
#
#     current_word = ()
#
#     @staticmethod
#     def nothing_left():
#         """
#         called when you have done all the words
#         """
#         pass
#
#     @staticmethod
#     def next_word(first=False):
#         if not first:
#             del Words.current[Words.selected[0]]
#
#         options = list(Words.current.items())
#
#         if len(options) == 0:
#             Words.nothing_left()
#         else:
#             Words.selected = random.choice(options)
#             translate_text.set(Words.selected[0])
#
#     @staticmethod
#     def get_new_words(select):
#         if select == 'wrong':
#             Words.current = Words.wrong.copy()
#         if select == 'right':
#             Words.current = Words.right.copy()
#         if select == 'same':
#             Words.current = Words.selected.copy()
#         if select == 'lan1':
#             Words.current = Words.all[0].copy()
#             Words.selected = Words.all[0].copy()
#         if select == 'lan2':
#             Words.current = Words.all[1].copy()
#             Words.selected = Words.all[1].copy()
#
#         Words.right = {}
#         Words.wrong = {}
#
#         Words.next_word(True)
#
#     @staticmethod
#     def check_correct(word):
#         if word in Words.selected[1]:
#             # right
#             Words.right[Words.selected[0]] = Words.selected[1]
#             wrong_text_var.set('Correct!')
#             wrong_text_fade.change(start=(0, 255, 0), end=(240, 240, 240), time=1)
#         else:
#             # wrong
#             Words.wrong[Words.selected[0]] = Words.selected[1]
#             wrong_text_var.set(' / '.join(Words.selected[1]))
#             wrong_text_fade.change(start=(255, 0, 0), end=(240, 240, 240), time=3)
#
#         Words.next_word()

class FullWords(Words):
    @staticmethod
    def right_answer():
        wrong_text_var.set('Correct!')
        wrong_text_fade.change(start=(0, 255, 0), end=(240, 240, 240), time=1)

    @staticmethod
    def wrong_answer(text):
        wrong_text_var.set(' / '.join(text))
        wrong_text_fade.change(start=(255, 0, 0), end=(240, 240, 240), time=3)

    @staticmethod
    def set_translate_text(text):
        translate_text.set(text)


def check_word(_):
    FullWords.check_correct(input_text.get())
    input_text.set("")


def replace(char):
    replace_from_to = (('§', '¿'),)

    for rep in replace_from_to:
        if char.char == rep[0]:
            text = input_text.get()
            position = input_field.index(tk.INSERT)

            input_text.set(text[:position] + rep[1] + text[position:])

            # Changing position of cursor one character right
            input_field.icursor(position + 1)

            return "break"


# window
root = tk.Tk()
root.geometry("600x400")
default_bg = root.cget('bg')
# root.configure(bg='#ffffff')

# translation entry
input_text = tk.StringVar(root)
input_field = tk.Entry(root, textvariable=input_text, font=("Times New Roman", 40, "bold"), justify='center')
input_field.pack()
input_field.bind('<Return>', check_word)
input_field.bind('<KeyPress>', replace)

# show word to be translated
translate_text = tk.StringVar(root)
translate_word_text = tk.Label(root, textvariable=translate_text, font=("Times New Roman", 40, "bold"))
translate_word_text.pack()

# shows the right translation if you typed it wrong
wrong_text_var = tk.StringVar(root)
wrong_text = tk.Label(root, textvariable=wrong_text_var, font=("Times New Roman", 40, "bold"))
wrong_text_fade = Fade(frame_obj=root, text_obj=wrong_text, time=3, gradiant='exponential')
wrong_text.pack()

# setup
FullWords.get_new_words('lan2')

root.mainloop()
