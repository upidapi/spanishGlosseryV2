import requests
import json
from PIL import Image
from general_funcs import *


# format:
# lan_1_word  lan_2_word     lan_1_word  lan_2_word
# lan_1_word  lan_2_word     lan_1_word  lan_2_word
# lan_1_word  lan_2_word     lan_1_word  lan_2_word
lan_1 = 'spa'
lan_2 = 'swe'


# noinspection PyTypeChecker
class DataClass:
    instances = []

    # get modify or delete data from the master data in a pythonic way
    def __init__(self):
        DataClass.instances.append(self)

        # gets the data
        self.data1 = load_data_from_json('lan1_data.json')
        self.data2 = load_data_from_json('lan2_data.json')

    def set_data(self):
        for obj in DataClass.instances:
            obj.data1 = self.data1
            obj.data2 = self.data2

    def switch_data(self):
        (self.data1, self.data2) = (self.data2, self.data1)
        DataClass.set_data(self)

    # format:
    # data['all']         -> the whole list
    # data[i: index]      -> line[i]
    # data[i: index, key] -> line[i][key]

    def get_data2(self):
        return self.data2

    def __getitem__(self, key: str | int | tuple[int, str]):
        if key == 'all':
            return self.data1

        elif type(key) is int:
            return self.data1[key]

        elif len(key) == 2:
            return self.data1[key[0]][key[1]]

    def __delitem__(self, key: str | int | tuple[int, str]):
        if key == 'all':
            del self.data1
            del self.data2

        elif type(key) is int:
            del self.data1[key]
            del self.data2[key]

        elif len(key) == 2:
            del self.data1[key[0]][key[1]]
            del self.data2[key[0]][key[1]]

        # changes the data in the other classes
        DataClass.set_data(self)

    def __setitem__(self, key: str | int | tuple[int, str], value):
        if key == 'all':
            self.data1 = value
            self.data2 = value

        elif type(key) is int:
            self.data1[key] = value
            self.data2[key] = value

        elif len(key) == 2:
            self.data1[key[0]][key[1]] = value
            self.data2[key[0]][key[1]] = value

        # changes the data in the other classes
        DataClass.set_data(self)

    def __len__(self):
        return len(self.data1)

    def append(self, x):
        self.data1.append(x)
        self.data2.append(x)

        # changes the data in the other classes
        DataClass.set_data(self)


def load_data_from_json(file):
    # gets the data
    with open(file) as jsonFile:
        json_object = json.load(jsonFile)
        jsonFile.close()

    return json_object


def save_to_jason(data, file):
    # converts python-array to json-document with indent 4
    json_object = json.dumps(data, indent=4)
    with open(file, "w") as outfile:
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


def get_existence(item, lis):
    for word in lis:
        # full match
        if item['x'] == word['x'] and \
                item['y'] == word['y'] and \
                item['width'] == word['width'] and \
                item['height'] == word['height']:
            return None

    for word in lis:
        # start match
        if item['x'] == word['x'] and \
                item['y'] == word['y'] and \
                item['height'] == word['height']:
            # sets the word to the longest
            if item['width'] < word['width']:
                return word

            # if you can't set it now prevent it from appending it
            return None

        # end match
        elif item['x'] + item['width'] == word['x'] + word['width'] and \
                item['y'] == word['y'] and \
                item['height'] == word['height']:
            # sets the word to the longest
            if item['width'] < word['width']:
                return word

            # if you can't set it now prevent it from appending it
            return None

    return 'NaN'


def get_missing_words(lan1, lan2):
    for i, word in enumerate(lan1):
        ret = get_existence(word, lan2)
        if ret is not None:
            if ret == 'NaN':
                lan2.append(word)
            else:
                lan1[i] = ret

    for i, word in enumerate(lan2):
        ret = get_existence(word, lan1)
        if ret is not None:
            if ret == 'NaN':
                lan1.append(word)
            else:
                lan2[i] = ret

    return lan1, lan2


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


def new_image(select_image="spa_text_glossary_perfect", lan=('spa', 'swe')):
    files = ["lan1_data.json", "lan2_data.json"]
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

    # gets the data and cleans up the data format
    clean_data = []
    for i in range(2):
        json_data = get_data_from_image('selected_image.jpg', language=lan[i])
        clean_data.append(_clean_up_data(json_data))

    # add some missing words
    fixed_data = get_missing_words(*clean_data)

    # sorts the data so that we can use the index
    for i in range(2):
        fixed_data[i].sort(key=lambda x: x['y'])
        save_to_jason(fixed_data[i], files[i])

    return fixed_data

