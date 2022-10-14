from Data import SelectFiles
import json


def save_data(data):
    file = SelectFilesMyOwn.ask_for_file(r"..\Data\books")

    # converts python-array to json-document with indent 4
    json_object = json.dumps(data, indent=4)
    with open(file, "w") as outfile:
        outfile.write(json_object)
