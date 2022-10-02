import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image

from FixRawInput import TrLines
from FixRawInput import Mode
from FixRawInput import CustomEntery
from FixRawInput.CustomEntery import Handler


def canvas_setup():
    global canvas, tk_image
    # background image
    path = r'..\FixRawInput\data\selected_image.jpg'
    raw_img = Image.open(path)
    tk_image = ImageTk.PhotoImage(raw_img)
    w = tk_image.width()
    h = tk_image.height()

    canvas = tk.Canvas(root, bd=0, highlightthickness=0)
    canvas.create_image(w//2, h//2, image=tk_image)  # the x and y is the center apparently
    canvas.place(x=0, y=0, width=w, height=h)


def entries_setup():
    # adds all the enters
    Handler.populate()
    # to prevent the last added entry from being focused
    root.focus()
    Handler.update_tr_lines()

    # binds
    root.bind('<Button-3>', lambda event: Handler.move(event))
    root.bind('<Button-2>', lambda event: Handler.new_word())
    root.bind('<Return>', lambda event: Mode.next_mode(event))
    root.bind('<q>', lambda event: Handler.merge(event))
    root.bind('<w>', lambda event: Handler.switch_text(event))

    root.bind('<e>', lambda event: Handler.hide(event, False))
    root.bind('<KeyRelease-e>', lambda event: Handler.hide(event, True))


def main():
    global root
    languishes = ('spa', 'swe')

    # from FixRawInput.data import Data
    # Data.new_image(r"C:\Users\videw\Downloads\spa_images\IMG_2496.jpg", languishes)

    root = tk.Tk()
    tk_font = font.Font(family='DejaVu Sans Mono', size=10)

    canvas_setup()
    root.geometry(f"{tk_image.width()}x{tk_image.height()}")

    CustomEntery.__init__(root, tk_font, tk_image, global_languages=('spa', 'swe'))
    TrLines.__init__(global_canvas=canvas, global_tk_image=tk_image)
    Mode.__init__(root, global_languages=languishes)

    entries_setup()
    root.mainloop()


if __name__ == '__main__':
    main()
