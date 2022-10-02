import tkfilebrowser
import json


def save_data(data):
    selected_directories = tkfilebrowser.askopenfilename(initialdir=r"../Data/words/", title='select')

    # converts python-array to json-document with indent 4
    json_object = json.dumps(data, indent=4)
    with open(selected_directories, "w") as outfile:
        outfile.write(json_object)
