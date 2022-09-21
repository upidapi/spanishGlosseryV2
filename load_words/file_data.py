import os
import tkfilebrowser
import json


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


def get_files(select='multiple'):
    selected_directories = None

    if select == 'multiple':
        selected_directories = tkfilebrowser.askopendirnames(initialdir=r"../load_words_r/words/", title='select')
    elif select == 'singular':
        selected_directories = tkfilebrowser.askopenfilename(initialdir=r"../load_words_r/words/", title='select')

    return get_dir_files(selected_directories)


def load_data(files: list):
    full_data = []
    for file in files:
        with open(file) as jsonFile:
            full_data += json.load(jsonFile)
            jsonFile.close()

    return full_data
