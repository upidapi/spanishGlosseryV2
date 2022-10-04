import FixRawInput
import Quiz
from Data import load_data, new_image

import tkinter as tk


class QuizGui:
    @staticmethod
    def setup():
        pass

def tes():
    pass

def main():
    root = tk.Tk()
    width = '200'
    height = '100'
    root.geometry(f"{width}x{height}")

    # todo change to place
    center_frame = tk.Frame(root)
    center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    text_label = tk.Label(center_frame, text='fuck you')
    text_label.grid(column=0, row=0)

    to_quiz = tk.Button(center_frame, text='Quiz', command=QuizGui.setup)
    to_quiz.grid(column=0, row=1)

    to_fix = tk.Button(center_frame, text='FixRawInput', command=QuizGui.setup)
    to_fix.grid(column=0, row=2, sticky='NW')

    root.mainloop()
    # # todo this is supposed to be a gui
    # select = {
    #     "type": "FixRawInput",  # Quiz or FixRawInput
    #     "data": "LoadData",  # LoadData or Image (only for FixRawInput)
    # }
    # languishes = ('spa', 'swe')
    #
    # if select["type"] == "Quiz":
    #     Quiz.main.__init__()
    #
    # elif select["type"] == "FixRawInput":
    #     if select["data"] == "LoadData":
    #         data = load_data.load_raw_data()
    #
    #         FixRawInput.main.__init__(data)
    #
    #     elif select["data"] == "Image":
    #         # data = new_image(r"C:\Users\videw\Downloads\spa_images\IMG_2494.jpg", languishes)
    #         data = new_image(r"C:\Users\vide.wallstrom\Downloads\MicrosoftTeams-image", languishes)
    #
    #         FixRawInput.main.__init__(data)


if __name__ == "__main__":
    main()
