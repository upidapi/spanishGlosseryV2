from Data import SelectFiles
import json
import os


def save_data(data):
    selected_directory = SelectFiles.ask_select(initial_dir=r"../Data/words/", amount='singular')

    # todo might want to do something to prevent an error if directory is empty/contains another directory
    file = os.listdir(selected_directory)[0]

    # converts python-array to json-document with indent 4
    json_object = json.dumps(data, indent=4)
    with open(file, "w") as outfile:
        outfile.write(json_object)
