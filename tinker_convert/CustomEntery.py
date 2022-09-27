import tkinter as tk
from tkinter import font
from tinker_convert.helper_funcs import get_mods

bg_color = '#f0f0f0'


def init(global_root, global_font):
    global root, tk_font, font_height

    root = global_root
    tk_font = global_font

    widget = tk.Label(root, text="My String")
    widget.pack()
    font_height = font.Font(font=widget['font']).metrics('linespace')
    widget.destroy()


class TextInput:
    mode = 0
    instances = []

    # helper funcs
    def get_width(self, tolerance=11):
        text = self.tk_text.get()

        return tk_font.measure(text) + tolerance

    @classmethod
    def find_focus(cls):
        focus = root.focus_get()
        for instance in cls.instances:
            if instance.entry == focus:
                return instance

    # call funcs
    @staticmethod
    def new_word():
        x, y = root.winfo_pointerxy()
        x -= root.winfo_rootx()
        y -= root.winfo_rooty()
        y -= font_height // 2

        TextInput('', x, y, 'normal')

    @staticmethod
    def move(_):
        self = TextInput.find_focus()

        x, y = root.winfo_pointerxy()
        x -= root.winfo_rootx()
        y -= root.winfo_rooty()
        y -= font_height // 2

        if 0 <= x and 0 <= y:
            entry_data = self.entry.place_info()

            self.entry.grid_forget()
            self.entry.place(x=x, y=y, width=entry_data['width'])

    def update_hit_box(self, tolerance=11):
        width = self.get_width(tolerance)
        entry_data = self.entry.place_info()

        self.entry.grid_forget()
        self.entry.place(x=entry_data['x'], y=entry_data['y'], width=width)

    def save(self, root_focus=True):
        self.saved_text = self.tk_text.get()

        entry_data = self.entry.place_info()
        x, y = entry_data['x'], entry_data['y']
        width = self.get_width(2)

        self.saved_pos = (x, y)

        self.entry.grid_forget()
        self.entry.place(x=x, y=y, width=width)

        if root_focus:
            root.focus()

    def focus_extra(self):
        self.entry.config(fg='#ff0000')

    def revert_changes(self, root_focus=True):
        # Remove changes
        self.tk_text.set(self.saved_text)

        x, y = self.saved_pos
        width = self.get_width(2)

        self.entry.grid_forget()
        self.entry.place(x=x, y=y, width=width)

        if TextInput.mode == 0:
            self.entry.config(state="readonly")
        else:
            self.entry.config(state="normal")

        self.entry.config(fg='#000000')

        if root_focus:
            root.focus()

        if self.tk_text.get() == "":
            self.entry.destroy()

    def delete(self, event):
        if 'ctrl' in get_mods(event):
            self.entry.destroy()
            TextInput.instances.remove(self)

    def split(self, event):
        if 'ctrl' in get_mods(event):
            cursor_pos = self.entry.index(tk.INSERT)

            bef_cursor = self.tk_text.get()[:cursor_pos]
            aft_cursor = self.tk_text.get()[cursor_pos:]

            if bef_cursor != '' and aft_cursor != '':
                self.tk_text.set(bef_cursor)
                self.update_hit_box()
                self.save()

                x, y = int(self.entry.place_info()['width']) + 5 + int(self.saved_pos[0]), int(self.saved_pos[1])
                split_text = TextInput(aft_cursor, x, y)
                split_text.revert_changes()

                self.entry.focus()

    def __init__(self, text, x, y, mater_state="readonly"):
        TextInput.instances.append(self)

        self.saved_pos = (x, y)
        self.saved_text = text
        self.tk_text = tk.StringVar(root, text)

        self.entry = tk.Entry(root,
                              readonlybackground=bg_color,
                              bg=bg_color,
                              borderwidth=0,
                              highlightthickness=0,
                              textvariable=self.tk_text,
                              font=tk_font)

        if mater_state == "readonly":
            self.entry.config(state="readonly")
        elif mater_state == "normal":
            self.entry.config(state="normal")

        self.entry.place(x=x, y=y)
        self.entry.focus()
        self.update_hit_box(2)

        # binds things
        self.entry.bind('<KeyPress>', lambda _: self.update_hit_box())
        self.entry.bind('<KeyRelease>', lambda _: self.update_hit_box())

        self.entry.bind('<Return>', lambda _: self.save())
        self.entry.bind('<Escape>', lambda _: self.revert_changes())
        self.entry.bind('<FocusOut>', lambda _: self.revert_changes(False))
        self.entry.bind('<FocusIn>', lambda _: self.focus_extra())

        self.entry.bind('<s>', lambda event: self.split(event))
        self.entry.bind('<Delete>', lambda event: self.delete(event))
