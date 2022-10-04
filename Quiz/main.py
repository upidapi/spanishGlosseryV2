from Quiz.FadeText import Fade
import tkinter as tk
from Quiz.Words import Words


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


def main_window_setup():
    global root
    # window
    root = tk.Tk()
    root.geometry("600x400")
    default_bg = root.cget('bg')

    global input_text, input_field
    # translation entry
    input_text = tk.StringVar(root)
    input_field = tk.Entry(root, textvariable=input_text, font=("Times New Roman", 40, "bold"), justify='center')
    input_field.pack()
    input_field.bind('<Return>', check_word)
    input_field.bind('<KeyPress>', replace)

    global translate_text
    # show word to be translated
    translate_text = tk.StringVar(root)
    translate_word_text = tk.Label(root, textvariable=translate_text, font=("Times New Roman", 40, "bold"))
    translate_word_text.pack()

    global wrong_text_var, wrong_text, wrong_text_fade
    # shows the right translation if you typed it wrong
    wrong_text_var = tk.StringVar(root)
    wrong_text = tk.Label(root, textvariable=wrong_text_var, font=("Times New Roman", 40, "bold"))
    wrong_text_fade = Fade(frame_obj=root, text_obj=wrong_text, time=3, gradiant='exponential')
    wrong_text.pack()


def __init__():
    # setup
    main_window_setup()

    FullWords.get_new_words('lan1')

    # noinspection PyUnboundLocalVariable
    root.mainloop()


# if __name__ == '__main__':
#     __init__()
