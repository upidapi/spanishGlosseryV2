import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image

from tinker_convert.CustomEntery import Handler, TextEntry
from tinker_convert.helper_funcs import get_mods


def next_mode(event):
    global mode
    if 'ctrl' in get_mods(event):
        mode += 1

        if mode == 1:
            for instance in TextEntry.instances:
                instance.entry.config(state='normal')
            root.title('edit words')


def main():
    global root
    root = tk.Tk()
    tk_font = font.Font(family='DejaVu Sans Mono', size=10)

    # background image
    path = r"C:\Users\videw\PycharmProjects\spanishGlosseryV2\edit_image_input\data\selected_image.jpg"
    raw_img = Image.open(path)
    w, h = raw_img.size
    tk_image = ImageTk.PhotoImage(raw_img)
    label1 = tk.Label(root, image=tk_image)
    label1.place(x=0, y=0)

    # window setup
    root.geometry(f"{w}x{h}")
    root.title('split/move/add/delete words')

    handler = Handler(global_root=root, global_font=tk_font, tk_image=tk_image)

    root.mainloop()


if __name__ == '__main__':
    main()
