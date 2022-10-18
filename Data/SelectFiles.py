import tkinter as tk
import os

# todo add option to add/delete book/chapter/part from file browser
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


def get_im_dirs(root_dir):
    sub_dirs = []
    for file in os.listdir(root_dir):
        d = os.path.join(root_dir, file)
        sub_dirs.append(d)
    return sub_dirs


class SuperPart:
    def __init__(self, parent, file):
        self.file = file

        self.indent_width = 0

        self.children = []
        self.parent = parent
        self.show_children = False
        self.selected = False

        if self.parent is not None:
            self.parent.children.append(self)

        text = os.path.basename(os.path.normpath(file))
        self.bar = tk.Button(root,
                             text=text,
                             command=self.hide,
                             background="#f0f0f0")

        # noinspection PyUnresolvedReferences
        if multiple:  # the last in line is the handler
            # if you're allowed to select multiple make selection possible (right-click)
            self.bar.bind("<Button-3>", self.select)
        else:
            # if you're only allowed to select one bind selection button to middle-click
            self.bar.bind("<Button-2>", lambda _: return_x(self.file))

    @property
    def raw_name(self):
        """
        :return: the parents children (siblings)
        """
        return os.path.basename(os.path.normpath(self.file))

    @property
    def siblings(self):
        """
        :return: the parents children (siblings)
        """
        if self.parent is None:
            return []
        else:
            return self.parent.children

    @property
    def super_parents(self):
        """
        :return: all parents (including self at index 0)
        """
        if self.parent is None:
            return []
        else:
            return [self] + self.parent.super_parents

    @property
    def super_children(self):
        """
        :return: all children (including self at index 0)
        """
        children_below = [self]
        for child in self.children:
            children_below += child.super_children
        return children_below

    @property
    def shown_children(self):
        """
        :return: the shown children (and theirs recursively)
        """
        children_below = [self]
        if self.show_children:
            for child in self.children:
                children_below += child.shown_children
        return children_below

    def get_total_indentation(self):
        """
        :return: the total indentation of self and parents
        """
        total_indentation = 0
        for parent in self.super_parents:
            total_indentation += parent.indent_width
        return total_indentation

    def get_total_index(self):
        """
        :return: the total amount of shown parts before self
        """
        to_parent = 0
        for sibling_before in self.siblings:
            if sibling_before == self:
                break

            to_parent += len(sibling_before.shown_children)

        if isinstance(self.parent, Book):
            return to_parent
        else:
            return to_parent + self.parent.get_total_index() + 1

    # high level functions
    def place(self):
        """
        places self att right position
        """
        if self.parent.show_children:
            height = 30
            x = self.get_total_indentation()
            y = self.get_total_index() * height

            self.bar.place(x=x, y=y)
        else:
            self.bar.place_forget()

    def hide(self):
        """
        (un)hides all children
        """
        if self.show_children:
            for child in self.super_children:
                child.show_children = False
        else:
            self.show_children = True

        handler.place_all()

    def select(self, _):
        """
        (un)selects all children
        """
        change_to = not self.selected
        color = {True: "#c0c0c0", False: "#f0f0f0"}[change_to]
        for child in self.super_children:
            child.selected = change_to
            child.bar.config(background=color)


class DataPart(SuperPart):
    """
    The last part in the line containing the file (with the data)
    """
    def __init__(self, parent, file):
        super().__init__(parent, file)

        self.indent_width = 20


class ContainerPart(SuperPart):
    """
    Contains ContainerPart(s) / DataPart(s)
    """
    def __init__(self, parent, file):
        super().__init__(parent, file)

        self.indent_width = 20
        self.drop_down_show()

    def drop_down_show(self):
        drop_symbol = {True: '˅', False: '˃'}[self.show_children]
        self.bar.config(text=f"{drop_symbol} {self.raw_name}")

    def hide(self):
        """
        (un)hides all children
        """
        if self.show_children:
            for child in self.super_children:
                child.show_children = False
        else:
            self.show_children = True

        self.drop_down_show()
        handler.place_all()

    def make_structure(self):
        for path in get_im_dirs(self.file):
            if path.endswith(".json"):
                DataPart(self, path)
            else:
                ContainerPart(self, path).make_structure()


class Book(SuperPart):
    """
    Is the handler / head of the parts (this is not shown)
    """

    def __init__(self):
        # todo you have to be able to select book it has to be ./Data/books/(book_name)
        super().__init__(None, r"..\Data\books\dos semanas en julio")

        if multiple:
            root.bind('<Return>', lambda _: root.destroy())

        self.indent_width = 0
        self.show_children = True

    def get_data_files(self):
        config_file = os.path.join(self.file, 'config.json')
        data_parts = []
        for child in self.children:
            data_parts += child.super_children

        data_files = []
        for part in data_parts:
            if part.file.endswith(".json") and part.selected:
                data_files.append(part.file)

        return {"config_file": config_file, "data_files": data_files}

    def place_all(self):
        for child in self.super_children[1:]:
            child.place()

    def make_structure(self):
        for path in get_im_dirs(self.file):
            if os.path.basename(os.path.normpath(path)) != 'config.json':
                ContainerPart(self, path).make_structure()


def ask_for_files2():
    global root, multiple, handler
    root = tk.Tk()
    root.geometry("300x300")
    root.title('select file(s) (return)')

    multiple = True
    handler = Book()
    handler.make_structure()
    handler.place_all()

    root.mainloop()

    return handler.get_data_files()


def return_x(x):
    global return_value
    root.destroy()
    return_value = x


def ask_for_file2():
    global root, multiple, handler, selected, return_value

    root = tk.Tk()
    root.geometry("300x300")
    root.title('select file (middle click)')

    return_value = None
    multiple = False
    handler = Book()
    handler.make_structure()
    handler.place_all()

    root.mainloop()

    return return_value


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


def make_tree(root_dir, parent=None, step=0):
    # todo when imported and called the directory is somehow not a directory
    # what?

    folder = os.path.basename(os.path.normpath(root_dir))
    # print('  ' * step, folder)

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
    print(ask_for_file2())
