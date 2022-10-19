# todo might want to add option to delete book/chapter/part from file browser
import tkinter as tk

from Data.FileBrowser.Parts import Head, ContainerPart, NewFilePart, DataPart


def add_chapter():
    if isinstance(handler.focused, ContainerPart):
        NewFilePart(handler.focused, ContainerPart)


def add_part():
    if isinstance(handler.focused, ContainerPart):
        NewFilePart(handler.focused, DataPart)


def add_files_button_setup():
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()

    translate = tk.Button(root, text='add part', command=add_part)
    translate.place(x=w-5, y=h-35, anchor=tk.SE)

    memory = tk.Button(root, text='add chapter', command=add_chapter)
    memory.place(x=w-5, y=h-5, anchor=tk.SE)


def ask_for_files():
    global root, handler

    root = tk.Tk()
    root.geometry("300x300")
    root.title('select file(s) (return)')

    handler = Head(root, multiple=True)
    handler.make_structure()
    handler.place_all()

    root.mainloop()

    return handler.get_data_files()


def ask_for_file():
    global root, handler
    root = tk.Tk()
    root.geometry("300x300")
    root.title('select file (middle click)')
    add_files_button_setup()

    handler = Head(root, multiple=False)
    handler.make_structure()
    handler.place_all()

    root.mainloop()

    return handler.focused.file


if __name__ == "__main__":
    print(ask_for_files())
