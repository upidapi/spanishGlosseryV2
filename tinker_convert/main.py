import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image

from tinker_convert.CustomEntery import init, TextInput
from tinker_convert.helper_funcs import get_mods


def next_mode(event):
    global mode
    if 'ctrl' in get_mods(event):
        mode += 1

        if mode == 1:
            for instance in TextInput.instances:
                instance.entry.config(state='normal')
            root.title('edit words')


def main():
    global root
    root = tk.Tk()

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
    init(global_root=root, global_font=font)

    # binds a few things
    root.bind('<Button-3>', lambda event: TextInput.move(event))
    root.bind('<Button-2>', lambda event: TextInput.new_word())
    root.bind('<Return>', lambda event: next_mode(event))

    # debug things
    TextInput('show1', 20, 20)
    TextInput('show2', 50, 50)
    TextInput('show3', 80, 80)

    root.mainloop()


if __name__ == '__main__':
    main()
