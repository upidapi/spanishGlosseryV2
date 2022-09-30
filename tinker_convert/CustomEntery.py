import tkinter as tk
from tinker_convert.helper_funcs import get_mods
from tinker_convert.data.Data import get

# todo strip saved text from spaces

class Handler:
    switch = False
    mode = 0

    # helper funcs
    @staticmethod
    def find_focus():
        focus = root.focus_get()
        for instance in TextEntry.instances:
            if instance.entry == focus:
                return instance

    # call funcs
    @staticmethod
    def next_mode(event):
        if 'ctrl' in get_mods(event):
            Handler.mode += 1

            if Handler.mode == 1:
                for instance in TextEntry.instances:
                    instance.entry.config(state='normal')

                root.title('edit words')

    @staticmethod
    def new_word():
        x, y = root.winfo_pointerxy()
        x -= root.winfo_rootx()
        y -= root.winfo_rooty()
        y -= font_height // 2

        TextEntry(text='', x=x, y=y, allow_write=True)

    @staticmethod
    def move(_):
        self = Handler.find_focus()

        if self is not None:
            x, y = root.winfo_pointerxy()
            x -= root.winfo_rootx()
            y -= root.winfo_rooty()
            y -= font_height // 2

            if 0 <= x and 0 <= y:
                entry_data = self.entry.place_info()

                self.entry.grid_forget()
                self.entry.place(x=x, y=y, width=entry_data['width'])

    @staticmethod
    def switch_text(event):
        if 'ctrl' in get_mods(event):
            Handler.switch = not Handler.switch
            # switches the text and other_text for all instances
            for instance in TextEntry.instances:
                text_main = instance.saved_text
                text_switch = instance.other_text

                instance.tk_text.set(text_switch)
                instance.saved_text = text_switch
                instance.other_text = text_main

                instance.update_hit_box()

    # other
    @staticmethod
    def get_data():
        full_data = []
        # gets the data from all the instances
        for instance in TextEntry.instances:
            text_main = instance.tk_text.get()
            text_translation = instance.other_text
            raw_entry_data = instance.entry.place_info()
            x, y = raw_entry_data['x'], raw_entry_data['y']

            if Handler.switch:
                text_main, text_translation = text_translation, text_main

            data = {
                'text': {'main': text_main, 'translation': text_translation},
                'x': x,
                'y': y,
                'height': font_height,
            }

            full_data.append(data)

    @staticmethod
    def populate():
        data = get()

        for d1, d2 in zip(*data):
            text_1, text_2 = d1['text'], d2['text']
            x, y = d1['x'], d1['y']

            TextEntry(text=text_1, x=x, y=y, text_other=text_2)

    def __init__(self, global_root, global_font):
        global root, tk_font, font_height, bg_color

        bg_color = '#f0f0f0'

        root = global_root
        tk_font = global_font

        widget = tk.Label(root, text="My String")
        widget.pack()
        font_height = tk.font.Font(font=widget['font']).metrics('linespace')
        widget.destroy()

        Handler.populate()

        root.bind('<Button-3>', lambda event: Handler.move(event))
        root.bind('<Button-2>', lambda event: Handler.new_word())
        root.bind('<w>', lambda event: Handler.switch_text(event))
        root.bind('<Return>', lambda event: Handler.next_mode(event))

        root.focus()


class TextEntry:
    mode = 0
    instances = []

    # helper funcs
    def get_width(self, tolerance=11):
        text = self.tk_text.get()

        return tk_font.measure(text) + tolerance

    # call funcs
    def custom_bind(self, key, func: callable, mod=None, do_extra: callable = None):
        # used to ease the proses of binding things

        def combined_funcs(event):
            if key in get_mods(event) or mod is None:
                func()

            if do_extra is not None:
                do_extra()

        self.entry.bind(key, lambda event: combined_funcs(event))

    def on_key_press(self, event):
        other = ['BackSpace', 'Delete']
        if 0 < Handler.mode or self.allow_write:
            self.update_hit_box()
        else:
            if (event.keysym in other) or (event.char.isprintable() and event.char != ''):
                return 'break'

    def update_hit_box(self, tolerance=11):
        width = self.get_width(tolerance)
        entry_data = self.entry.place_info()

        self.entry.grid_forget()
        self.entry.place(x=entry_data['x'], y=entry_data['y'], width=width)

    def un_focus(self, do_extra: callable = None):
        """
        does all things that have to be done when you un focus

        :param do_extra: will be called after un_focus() is run
        """
        self.allow_write = False

        self.update_hit_box(2)

        if self.tk_text.get() == "":
            self.entry.destroy()

        self.entry.config(fg='#000000')

        if do_extra is not None:
            do_extra()

    def save(self, do_extra: callable = None):
        """
        saves the entry data

        :param do_extra: will be called after save() is run
        """

        self.saved_text = self.tk_text.get()

        entry_data = self.entry.place_info()
        x, y = entry_data['x'], entry_data['y']
        width = self.get_width(2)

        self.saved_pos = (x, y)

        self.entry.grid_forget()
        self.entry.place(x=x, y=y, width=width)

        if do_extra is not None:
            do_extra()

    def revert_changes(self, do_extra):
        """
        reverts all changes on the text entry

        :param do_extra: will be called after revert_changes() is run
        :return:
        """
        # Remove changes
        self.tk_text.set(self.saved_text)

        x, y = self.saved_pos
        width = self.get_width(2)

        self.entry.grid_forget()
        self.entry.place(x=x, y=y, width=width)

        if do_extra is not None:
            do_extra()

    def delete_instance(self, event):
        if 'ctrl' in get_mods(event):
            self.entry.destroy()
            TextEntry.instances.remove(self)
        return self.on_key_press(event)

    def split(self, event):
        if 'ctrl' in get_mods(event):
            cursor_pos = self.entry.index(tk.INSERT)

            text_main, text_translation = self.tk_text.get(), self.other_text
            if Handler.switch:
                text_main, text_translation = text_translation, text_main

            bef_cursor = text_main[:cursor_pos]
            aft_cursor = text_translation[cursor_pos:]

            self.tk_text.set(bef_cursor)
            self.other_text = bef_cursor
            self.save()
            self.un_focus()

            x = int(self.entry.place_info()['width']) + 5 + int(self.saved_pos[0])  # the 5 is to shift it a bit
            y = int(self.saved_pos[1])
            split_text = TextEntry(text=aft_cursor, x=x, y=y, allow_write=True)
            split_text.save()
            split_text.un_focus()

        return self.on_key_press(event)

    def __init__(self, *, text, x, y, text_other=None, allow_write=False):
        global root

        TextEntry.instances.append(self)

        self.allow_write = allow_write
        self.saved_pos = (x, y)
        self.saved_text = text
        self.tk_text = tk.StringVar(root, text)

        if text_other is None:
            self.other_text = text
        else:
            self.other_text = text_other

        self.entry = tk.Entry(
            root,
            readonlybackground=bg_color,
            bg=bg_color,
            borderwidth=0,
            highlightthickness=0,
            textvariable=self.tk_text,
            font=tk_font
        )

        self.entry.place(x=x, y=y)
        self.entry.focus()
        self.update_hit_box(2)

        # binds things
        self.entry.bind('<Return>', lambda _: self.save(lambda: root.focus()))
        self.entry.bind('<Escape>', lambda _: self.revert_changes(lambda: root.focus()))
        self.entry.bind('<FocusOut>', lambda _: self.un_focus())
        self.entry.bind('<FocusIn>', lambda _: self.entry.config(fg='#ff0000'))

        self.entry.bind('<s>', lambda event: self.split(event))
        self.entry.bind('<Delete>', lambda event: self.delete_instance(event))

        self.entry.bind('<KeyRelease>', lambda _: self.update_hit_box())
        self.entry.bind('<KeyPress>', lambda event: self.on_key_press(event))


# class CustomisedEntry(tk.Entry):
#     def __init__(self, master, master_self, **kw):
#         print('asd')
#         super().__init__(master, **kw)
#         self.master_self = master_self
#
#     def insert(self, pos, value):
#         if 0 < Handler.mode or self.master_self.allow_write:
#             super().insert(pos, value)
#             self.master_self.update_hit_box()
#         else:
#             self.config(state='normal')
#             super().insert(pos, value)
#             self.config(state='disabled')
#
#     def delete(self, first, last=None):
#         print(111)
#         if 0 < Handler.mode or self.master_self.allow_write:
#             super().delete(first, last)
#             self.master_self.update_hit_box()
