import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image

root = tk.Tk()

bg_color = '#f0f0f0'
tk_font = font.Font(family='DejaVu Sans Mono', size=10)

widget = tk.Label(root, text="My String")
widget.pack()
font_height = font.Font(font=widget['font']).metrics('linespace')
widget.destroy()

mode = 0


def get_mods(event):
    s = event.state

    # Manual way to get the modifiers
    ctrl = (s & 0x4) != 0
    alt = (s & 0x8) != 0 or (s & 0x80) != 0
    shift = (s & 0x1) != 0

    mods = []
    if ctrl:
        mods.append('ctrl')
    if alt:
        mods.append('alt')
    if shift:
        mods.append('shift')

    return mods


class TextInput:
    instances = []
    focus = root.focus_get()

    def get_width(self, tolerance=11):
        text = self.tk_text.get()

        return tk_font.measure(text) + tolerance

    def update_hit_box(self, tolerance=11):
        width = self.get_width(tolerance)
        entry_data = self.entry.place_info()

        self.entry.grid_forget()
        self.entry.place(x=entry_data['x'], y=entry_data['y'], width=width)

    def enter(self, root_focus=True):
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

    def un_focus(self, root_focus=True):
        # Remove changes
        self.tk_text.set(self.saved_text)

        x, y = self.saved_pos
        width = self.get_width(2)

        self.entry.grid_forget()
        self.entry.place(x=x, y=y, width=width)

        if mode == 0:
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
                self.enter()

                x, y = int(self.entry.place_info()['width']) + 5 + int(self.saved_pos[0]), int(self.saved_pos[1])
                print(self.saved_pos, x, y)
                split_text = TextInput(aft_cursor, x, y)
                split_text.un_focus()

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

        self.entry.bind('<s>', lambda event: self.split(event))
        self.entry.bind('<Delete>', lambda event: self.delete(event))

        self.entry.bind('<KeyPress>', lambda _: self.update_hit_box())
        self.entry.bind('<KeyRelease>', lambda _: self.update_hit_box())

        self.entry.bind('<Return>', lambda _: self.enter())
        self.entry.bind('<Escape>', lambda _: self.un_focus())
        self.entry.bind('<FocusOut>', lambda _: self.un_focus(False))
        self.entry.bind('<FocusIn>', lambda _: self.focus_extra())


def new_word(event):
    x, y = root.winfo_pointerxy()
    x -= root.winfo_rootx()
    y -= root.winfo_rooty()
    y -= font_height // 2

    TextInput('', x, y, 'normal')


def move(_):
    focus = root.focus_get()
    for instance in TextInput.instances:
        if instance.entry == focus:
            # gives the absolute root pos instead of pos at the widget you're over
            x, y = root.winfo_pointerxy()
            x -= root.winfo_rootx()
            y -= root.winfo_rooty()
            y -= font_height // 2

            if 0 <= x and 0 <= y:
                entry_data = instance.entry.place_info()

                instance.entry.grid_forget()
                instance.entry.place(x=x, y=y, width=entry_data['width'])


def next_mode(event):
    global mode
    if 'ctrl' in get_mods(event):
        mode += 1

        if mode == 1:
            for instance in TextInput.instances:
                instance.entry.config(state='normal')
            root.title('edit words')


def main():
    path = r"C:\Users\videw\PycharmProjects\spanishGlosseryV2\translate\selected_image.jpg"
    raw_img = Image.open(path)
    w, h = raw_img.size
    tk_image = ImageTk.PhotoImage(raw_img)

    root.geometry(f"{w}x{h}")

    label1 = tk.Label(root, image=tk_image)
    label1.place(x=0, y=0)

    root.title('split/move/add/delete words')

    root.bind('<Button-3>', lambda event: move(event))
    root.bind('<Button-2>', lambda event: new_word(event))
    root.bind('<Return>', lambda event: next_mode(event))

    TextInput('show1', 20, 20)
    TextInput('show2', 50, 50)
    TextInput('show3', 80, 80)

    root.focus()

    root.mainloop()


if __name__ == '__main__':
    main()
