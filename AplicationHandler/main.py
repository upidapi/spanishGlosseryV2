import FixRawInput
import Quiz
from Data import load_data, new_image
import tkinter as tk


class CallFuncs:
    @staticmethod
    def load_new_image():
        new_image("../Data/other_data/selected_image.jpg", languishes)

        FixRawInput.main.__init__()


class WindowSetup:
    @staticmethod
    def base(*, width: int, height: int, title: str = ''):
        """
        clears and sets up the root for a new setup
        """

        for element in root.winfo_children():
            element.destroy()

        root.geometry(f"{str(width)}x{str(height)}")
        root.title(title)

    @staticmethod
    def quiz():
        WindowSetup.base(width=230, height=100)

        text_label = tk.Label(root, text='what method')
        text_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        flashcards = tk.Button(root, text='flashcards', command=lambda: print('flashcards'))
        flashcards.place(relx=0.2, rely=0.6, anchor=tk.CENTER)

        memory = tk.Button(root, text='memory', command=lambda: print('memory'))
        memory.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        translate = tk.Button(root, text='translate', command=lambda: Quiz.main.__init__())
        translate.place(relx=0.8, rely=0.6, anchor=tk.CENTER)

    @staticmethod
    def new_part():
        # todo remove this, it's mostly for debug purposes
        # todo fix this, add load image/load old data
        WindowSetup.base(width=230, height=100)

        text_label = tk.Label(root, text='select data')
        text_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        load_image = tk.Button(root, text='load image', command=CallFuncs.load_new_image)
        load_image.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

        load_old_data = tk.Button(root, text='load old data', command=FixRawInput.main.__init__)
        load_old_data.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

    @staticmethod
    def main():
        WindowSetup.base(width=230, height=100)

        text_label = tk.Label(root, text='what do you want to do')
        text_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        to_quiz = tk.Button(root, text='add new part', command=WindowSetup.new_part)
        to_quiz.place(relx=0.7, rely=0.6, anchor=tk.CENTER)

        new_part = tk.Button(root, text='quiz yourself', command=WindowSetup.quiz)
        new_part.place(relx=0.3, rely=0.6, anchor=tk.CENTER)

    @staticmethod
    def test():
        class CustomFrame:
            def __init__(self, parent, *, frame_color, text, **kwargs):
                self.border = tk.Frame(parent, background=frame_color, highlightthickness=0)
                self.inside = tk.Frame(self.border, **kwargs)
                self.frame_text = tk.Label(text=text)

            def place(self, x, y, width, height):
                fw = 2
                self.border.place(x=x, y=y, width=width, height=height)
                self.inside.place(x=fw, y=fw, width=width - fw * 2, height=height - fw * 2)
                self.frame_text.place(x=x + 10, y=y - 10)

        root.geometry(f"400x400")

        new_part = CustomFrame(root, frame_color="#d0d0d0", text='new part')
        new_part.place(x=10, y=10, width=140, height=80)

        from_image = tk.Button(new_part.inside, text='load data from image')
        from_image.place(x=5, y=10)

        from_old = tk.Button(new_part.inside, text='load data from old')
        from_old.place(x=5, y=40)

        quiz = CustomFrame(root, frame_color="#d0d0d0", text='quiz')
        quiz.place(x=160, y=10, width=80, height=110)

        test1 = tk.Button(quiz.inside, text='flashcards')
        test1.place(x=5, y=10)

        test2 = tk.Button(quiz.inside, text='memory')
        test2.place(x=5, y=40)

        test3 = tk.Button(quiz.inside, text='translate')
        test3.place(x=5, y=70)


def main():
    global root, languishes
    root = tk.Tk()
    languishes = ('spa', 'swe')

    # makes it fill the entire screen
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    WindowSetup.main()

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
    # CallFuncs.load_old_data()
