import tkinter as tk
import os

"""
root = {
    'chapter_1': {
        'part_1': text file path.json

        'part_2': text file path.json

        ...
    },

    'chapter_2': {
        ...
    },

    ...
}
"""


class Part:
    master_parent = None
    selected_files = []

    def __init__(self, text, parent, file=None):
        self.children = []
        self.parent = parent
        self.file = file
        self.selected = False

        if file is None:
            bg = '#f0f0f0'
        else:
            # bg = '#ff0000'
            bg = '#f0f0f0'

            # removes the .json from the name
            # text = text.replace('.json', '')

        if parent is None:
            self.show_children = True
            Part.master_parent = self
        else:
            self.parent.children.append(self)
            self.show_children = False

            self.bar = tk.Button(root,
                                 text=text,
                                 command=self.hide,
                                 background=bg)

            if selected == 'multiple':
                self.bar.bind("<Button-3>", self.select)

            if file is not None and selected == 'singular':
                def return_selected(_):
                    root.destroy()
                    Part.selected_files = self.file

                self.bar.bind("<Button-2>", return_selected)

    def for_all_children(self, function: callable):
        function(self)
        for child in self.children:
            child.for_all_children(function)

    def place_self(self, bar_index, step):
        between_bars = 30
        step_in = 20

        # account for the master parent
        x = step_in * (step - 1) + 10
        y = between_bars * (bar_index - 1) + 10

        self.bar.place(x=x, y=y)

    def place_children(self, total_bef=0, step=0):
        if step != 0:
            self.place_self(total_bef, step)

        total_bef += 1

        if self.show_children:
            for child in self.children:
                total_bef = child.place_children(total_bef, step + 1)

        return total_bef

    @staticmethod
    def place_all():
        for child in root.winfo_children():
            child.place_forget()

        Part.master_parent.place_children(0)

    def hide(self):
        if self.show_children:
            def set_value(child):
                child.show_children = False

            self.for_all_children(set_value)

        else:
            self.show_children = True

        Part.place_all()

    def select(self, _):
        value = not self.selected

        def set_value(child):
            child.selected = value

            if self.selected:
                child.bar.config(background="#c0c0c0")
                if child.file is not None:
                    Part.selected_files.append(child.file)

            else:
                if child.file is None:
                    child.bar.config(background="#f0f0f0")
                else:
                    # child.bar.config(background="#ff0000")
                    child.bar.config(background="#f0f0f0")

                if child.selected:
                    Part.selected_files.remove(child.file)

        self.for_all_children(set_value)

        # print(Part.selected_files)

    # @staticmethod
    # def on_click(click_type):
    #     if click_type


def get_im_dirs(root_dir):
    sub_dirs = []
    for file in os.listdir(root_dir):
        d = os.path.join(root_dir, file)
        sub_dirs.append(d)
    return sub_dirs


def make_tree(root_dir, parent=None, step=0):
    # todo when imported and called the directory is somehow not a directory
    folder = os.path.basename(os.path.normpath(root_dir))
    print('  ' * step, folder)

    if os.path.isdir(root_dir):
        new_parent = Part(text=folder, parent=parent)

        for directory in get_im_dirs(root_dir):
            make_tree(directory, new_parent, step + 1)

    else:
        Part(text=folder, parent=parent, file=root_dir)


def ask_for_file(initial_dir):
    global selected
    selected = 'singular'

    global root
    root = tk.Tk()
    root.geometry("300x300")
    root.title('select file (middle click)')

    make_tree(initial_dir)

    Part.place_all()
    root.mainloop()

    return Part.selected_files


def ask_for_files(initial_dir):
    global selected
    selected = 'multiple'

    global root
    root = tk.Tk()
    root.geometry("300x300")
    root.title('select files (enter)')

    make_tree(initial_dir)
    Part.place_all()

    root.bind('<Return>', lambda _: root.destroy())
    root.mainloop()

    return Part.selected_files


if __name__ == "__main__":
    print(ask_for_file(r"C:\Users\videw\PycharmProjects\spanishGlosseryV2"))
