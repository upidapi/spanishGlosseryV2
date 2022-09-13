import requests
import json
from PIL import Image
from general_funcs import *


# noinspection PyTypeChecker
class DataClass:
    instances = []

    # get modify or delete data from the master data in a pythonic way
    def __init__(self):
        DataClass.instances.append(self)

        # gets the data
        with open("sample.json") as jsonFile:
            json_object = json.load(jsonFile)
            jsonFile.close()

        self.data = json_object

    def set_data(self):
        for obj in DataClass.instances:
            obj.data = self.data

    # format:
    # data['all']         -> the whole list
    # data[i: index]      -> line[i]
    # data[i: index, key] -> line[i][key]

    def __getitem__(self, key: str | int | tuple[int, str]):
        if key == 'all':
            return self.data

        elif type(key) is int:
            return self.data[key]

        elif len(key) == 2:
            return self.data[key[0]][key[1]]

    def __delitem__(self, key: str | int | tuple[int, str]):
        if key == 'all':
            del self.data

        elif type(key) is int:
            del self.data[key]

        elif len(key) == 2:
            del self.data[key[0]][key[1]]

        # changes the data in the other classes
        DataClass.set_data(self)

    def __setitem__(self, key: str | int | tuple[int, str], value):
        if key == 'all':
            self.data = value

        elif type(key) is int:
            self.data[key] = value

        elif len(key) == 2:
            self.data[key[0]][key[1]] = value

        # changes the data in the other classes
        DataClass.set_data(self)

    def __len__(self):
        return len(self.data)

    def append(self, x):
        self.data.append(x)

        # changes the data in the other classes
        DataClass.set_data(self)

    def save_text_from_image(self, image):
        raw_data = new_image(image)
        self.data = raw_data
        save_to_jason(self.data)


def save_to_jason(data):
    # converts python-array to json-document with indent 4
    json_object = json.dumps(data, indent=4)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


def get_bounding_box_data(line):
    line_pos = get_line_bounding_box(line)

    line_data = {
        'text': line['LineText'],

        'x': line_pos[0],
        'y': line_pos[1],
        'width': line_pos[2],
        'height': line_pos[3]
    }

    return line_data


def _clean_up_data(dirty_data):
    """
    converts the raw return data into a better format

    :param dirty_data: the raw json data
    :return: a cleaner version of the data
    """
    clean_data = []

    # data format
    # [
    #     {
    #         'text': 'the lines text',
    #
    #         'x': 'x position (int)',
    #         'y': 'y position (int)',
    #         'width': 'width (int)',
    #         'height': 'height (int)'
    #     },
    #
    #     ...
    # ]

    for line in dirty_data["ParsedResults"][0]["TextOverlay"]["Lines"]:

        line_data = get_bounding_box_data(line)

        clean_data.append(line_data)

    return clean_data


def get_data_from_image(filename, language='eng'):
    """
    OCR.space API requests with local file.

    :param filename: Your file path & name.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    api_key = "K85003833988957"

    payload = {'isOverlayRequired': True,
               'apikey': api_key,
               'language': language,
               'scale': True
               }

    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    # decode
    return_data = r.content.decode()
    # from json-str to python-array
    return_data = json.loads(return_data)
    return return_data


def new_image(select_image="spa_text_glossary_perfect"):
    test_images = {
        "eng_text_page": r"C:\Users\videw\Downloads\book page.jpg",
        "spa_text_glossary_rotated": r"C:\Users\videw\Downloads\IMG_2439.jpg",
        "spa_text_glossary_perfect": r"C:\Users\videw\Downloads\IMG_2438.jpg",
        "spa_text_glossary_imperfect": r"C:\Users\videw\Downloads\IMG_2421.png"
    }

    image_dir = test_images[select_image] if select_image in test_images else select_image
    image = Image.open(image_dir)
    image.thumbnail((1000, 1000))

    image.save('selected_image.jpg')
    json_data = get_data_from_image('selected_image.jpg', language='spa')
    # cleans up the data and saves it into the data class
    return _clean_up_data(json_data)

