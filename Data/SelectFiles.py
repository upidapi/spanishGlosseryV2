import tkfilebrowser
import os


def get_sub_files(directory):
    if os.path.isfile(directory):
        return [directory.replace(os.getcwd() + '\\', '').replace('\\', '/')]
    else:
        files = []
        for sub_dir in os.listdir(directory):
            files += get_sub_files(os.path.join(directory, sub_dir))

        return files


def get_dir_files(directory):
    if isinstance(directory, tuple):
        files = []
        for sub_dir in directory:
            files += get_sub_files(sub_dir)

        return files

    elif directory is not None:
        return [directory.split('\\')[-1]]

    else:
        return []


# temporary implementation
# todo might want to do something to prevent an error if directory is empty/contains another directory
# todo implement a custom file selector
def ask_select(initial_dir, amount='multiple'):
    if amount == 'multiple':
        selected_directories = tkfilebrowser.askopenfilenames(initialdir=initial_dir, title='select')
        return get_dir_files(selected_directories)

    elif amount == 'singular':
        selected_directories = tkfilebrowser.askopenfilename(initialdir=initial_dir, title='select')
        return get_dir_files(selected_directories)[0]
